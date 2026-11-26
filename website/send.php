<?php
/*
 * Kontakt- und Bewerbungsformular Malerbetrieb Kötter
 * Verschickt Anfragen per E-Mail. Laeuft auf normalem Webhosting mit PHP 7.4 oder neuer.
 *
 * Schutz:
 *  - Honeypot: ein unsichtbares Feld, das nur Spam-Programme ausfuellen
 *  - Zeitfalle: wer das Formular schneller als in 3 Sekunden abschickt, ist kein Mensch
 *  - Ratenbegrenzung: pro Absender hoechstens 1 Anfrage pro Minute und 5 pro Stunde
 *  - Alle Werte, die in Mail-Kopfzeilen landen, werden von Zeilenumbruechen und
 *    Steuerzeichen befreit (Schutz vor Header-Injection)
 */

declare(strict_types=1);

/* ---------- Einstellungen ---------- */
const EMPFAENGER   = 'info@malerbetrieb-koetter.de';
const ABSENDER     = 'info@malerbetrieb-koetter.de';      // muss beim Webhoster als Postfach existieren, sonst landet die Mail oft im Spam
const ABSENDERNAME = 'Website Malerbetrieb Kötter';
const MIN_SEKUNDEN = 3;
const LIMIT_MINUTE = 1;
const LIMIT_STUNDE = 5;
const DATENORDNER  = __DIR__ . '/formular-daten';

/* Kommt die Nachricht vom Bewerbungsformular (Seite "karriere") oder vom Anfrageformular? */
define('BEWERBUNG', isset($_POST['art']) && $_POST['art'] === 'bewerbung');
define('SEITE', BEWERBUNG ? '/karriere' : '/kontakt');   // Zurueck-Adresse ohne .html, fest vorgegeben

/* ---------- Hilfsfunktionen ---------- */
/** Kötter spricht Kunden und Bewerber mit "Sie" an. */
function t(string $sie, string $du = ''): string
{
    return $sie;
}

function will_json(): bool
{
    return isset($_SERVER['HTTP_ACCEPT']) && strpos((string) $_SERVER['HTTP_ACCEPT'], 'application/json') !== false;
}

function antwort(bool $ok, string $code, string $meldung = '', int $status = 200): void
{
    if (will_json()) {
        http_response_code($status);
        header('Content-Type: application/json; charset=utf-8');
        header('Cache-Control: no-store');
        echo json_encode(['ok' => $ok, 'meldung' => $meldung], JSON_UNESCAPED_UNICODE);
    } else {
        header('Location: ' . SEITE . '?status=' . rawurlencode($code), true, 303);
    }
    exit;
}

/** Text fuer den Mail-Inhalt: Steuerzeichen raus, Zeilenumbrueche erlaubt, Laenge begrenzt. */
function text_feld(string $name, int $max): string
{
    $wert = isset($_POST[$name]) && is_string($_POST[$name]) ? $_POST[$name] : '';
    $wert = str_replace(["\r\n", "\r"], "\n", $wert);
    $wert = preg_replace('/[^\P{C}\n\t]/u', '', $wert) ?? '';
    return mb_substr(trim($wert), 0, $max, 'UTF-8');
}

/** Einzeilige Werte: Zeilenumbrueche und alle Steuerzeichen entfernen. Pflicht fuer alles, was in Kopfzeilen landet. */
function zeile(string $wert, int $max = 200): string
{
    $wert = preg_replace('/[\x00-\x1F\x7F]|\p{C}/u', ' ', $wert) ?? '';
    $wert = preg_replace('/\s+/u', ' ', $wert) ?? '';
    return mb_substr(trim($wert), 0, $max, 'UTF-8');
}

/* ---------- Nur POST zulassen ---------- */
if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    header('Allow: POST');
    antwort(false, 'fehler', 'Ungültige Anfrage.', 405);
}

/* ---------- Honeypot und Zeitfalle ---------- */
$honig = isset($_POST['website']) && is_string($_POST['website']) ? trim($_POST['website']) : '';
$start = isset($_POST['t']) && is_string($_POST['t']) && ctype_digit($_POST['t']) ? (int) $_POST['t'] : 0;
if ($honig !== '' || ($start > 0 && (time() - $start) < MIN_SEKUNDEN)) {
    // Spam-Programmen tun wir so, als waere alles gut gegangen.
    antwort(true, 'ok', '');
}

/* ---------- Eingaben pruefen ---------- */
$name      = zeile(text_feld('name', 120), 120);
$email     = zeile(text_feld('email', 200), 200);
$telefon   = zeile(text_feld('telefon', 60), 60);
$ort       = zeile(text_feld('ort', 120), 120);
$vorhaben  = zeile(text_feld('vorhaben', 60), 60);
$nachricht = text_feld('nachricht', 5000);
$ok_ds     = isset($_POST['datenschutz']) && $_POST['datenschutz'] === 'ja';

$erlaubt = BEWERBUNG
    ? ['Ausbildung Maler und Lackierer', 'Geselle Maler und Lackierer', 'Initiativbewerbung', '']
    : ['Innenarbeiten', 'Tapezieren', 'Fassade', 'Boden', 'Wärmedämmung', 'Sonstiges', ''];
if (!in_array($vorhaben, $erlaubt, true)) {
    $vorhaben = BEWERBUNG ? 'Initiativbewerbung' : 'Sonstiges';
}

$vorhaben_text = $vorhaben;

$email_ok = filter_var($email, FILTER_VALIDATE_EMAIL) !== false;
if ($name === '' || !$email_ok || mb_strlen($nachricht, 'UTF-8') < 5 || !$ok_ds) {
    antwort(false, 'eingabe', t('Bitte füllen Sie Name, E-Mail und Nachricht aus und bestätigen Sie den Datenschutzhinweis.', 'Bitte fülle Name, E-Mail und ein paar Sätze über dich aus und bestätige den Datenschutzhinweis.'), 422);
}

/* ---------- Ratenbegrenzung ---------- */
$ip = (string) ($_SERVER['REMOTE_ADDR'] ?? 'unbekannt');
if (!is_dir(DATENORDNER)) {
    @mkdir(DATENORDNER, 0750, true);
}
// IP wird nur als Hash (unumkehrbare Pruefsumme) gespeichert und nach einer Stunde verworfen.
$datei = DATENORDNER . '/rl-' . hash('sha256', $ip . '|' . __FILE__) . '.json';
$jetzt = time();
$zeiten = [];
$fh = @fopen($datei, 'c+');
if ($fh !== false) {
    flock($fh, LOCK_EX);
    $inhalt = stream_get_contents($fh);
    $alt = json_decode($inhalt !== false ? $inhalt : '', true);
    if (is_array($alt)) {
        foreach ($alt as $z) {
            if (is_int($z) && $z > $jetzt - 3600) {
                $zeiten[] = $z;
            }
        }
    }
    $letzteMinute = count(array_filter($zeiten, static function (int $z) use ($jetzt): bool { return $z > $jetzt - 60; }));
    if ($letzteMinute >= LIMIT_MINUTE || count($zeiten) >= LIMIT_STUNDE) {
        flock($fh, LOCK_UN);
        fclose($fh);
        antwort(false, 'zu-schnell', t('Sie haben gerade schon eine Anfrage geschickt. Bitte warten Sie ein paar Minuten.', 'Du hast gerade schon etwas geschickt. Bitte warte ein paar Minuten.'), 429);
    }
    $zeiten[] = $jetzt;
    ftruncate($fh, 0);
    rewind($fh);
    fwrite($fh, json_encode($zeiten));
    fflush($fh);
    flock($fh, LOCK_UN);
    fclose($fh);
}
// Alte Dateien gelegentlich aufraeumen
if (random_int(1, 20) === 1) {
    foreach ((array) glob(DATENORDNER . '/rl-*.json') as $f) {
        if (is_string($f) && @filemtime($f) < $jetzt - 3600) {
            @unlink($f);
        }
    }
}

/* ---------- Mail bauen ---------- */
$betreff_roh = zeile((BEWERBUNG ? 'Neue Bewerbung: ' : 'Neue Anfrage: ') . ($vorhaben_text !== '' ? $vorhaben_text : 'Website') . ' von ' . $name, 180);
$betreff = mb_encode_mimeheader($betreff_roh, 'UTF-8', 'B', "\r\n");

$inhalt  = BEWERBUNG ? "Neue Bewerbung über die Karriere-Seite der Website\n" : "Neue Anfrage über das Formular auf der Website\n";
$inhalt .= str_repeat('=', 46) . "\n\n";
$inhalt .= "Name:      {$name}\n";
$inhalt .= "E-Mail:    {$email}\n";
$inhalt .= "Telefon:   " . ($telefon !== '' ? $telefon : 'nicht angegeben') . "\n";
$inhalt .= (BEWERBUNG ? "Wohnort:   " : "Ort:       ") . ($ort !== '' ? $ort : 'nicht angegeben') . "\n";
$inhalt .= (BEWERBUNG ? "Stelle:    " : "Vorhaben:  ") . ($vorhaben_text !== '' ? $vorhaben_text : 'nicht angegeben') . "\n\n";
$inhalt .= (BEWERBUNG ? "Über mich:" : "Nachricht:") . "\n{$nachricht}\n\n";
$inhalt .= str_repeat('-', 46) . "\n";
$inhalt .= 'Gesendet am ' . date('d.m.Y \u\m H:i') . " Uhr. Einfach auf diese Mail antworten, um zu reagieren.\n";

// Reply-To: nur die gepruefte Adresse, Name ohne Sonderzeichen und MIME-kodiert
$antwortname = mb_encode_mimeheader(str_replace(['"', '<', '>', ',', ';', ':', '\\'], '', $name), 'UTF-8', 'B', "\r\n");
$kopf = [
    'From: ' . mb_encode_mimeheader(ABSENDERNAME, 'UTF-8', 'B') . ' <' . ABSENDER . '>',
    'Reply-To: ' . $antwortname . ' <' . zeile($email, 200) . '>',
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8',
    'Content-Transfer-Encoding: 8bit',
    'X-Mailer: Koetter-Website',
];

$gesendet = @mail(EMPFAENGER, $betreff, $inhalt, implode("\r\n", $kopf), '-f' . ABSENDER);

if ($gesendet) {
    antwort(true, 'ok', '');
}
antwort(false, 'fehler', 'Das hat leider nicht geklappt. Rufen Sie uns gern an (05462 00000) oder schreiben Sie an info@malerbetrieb-koetter.de.', 500);
