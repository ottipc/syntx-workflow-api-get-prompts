📘 LOG-REFERENCE — Vollständige, technische Analyse aller Log-Felder

(Copy/Paste-ready für README.md)

⸻

🧠 1. GPT-Meta-Prompt-Logs (gpt_prompts.jsonl)

Diese Datei speichert alle Interaktionen mit GPT, die Meta-Prompts erzeugen.

Jede Zeile = ein vollständiger Durchlauf.

⸻

🧩 Tabellenübersicht aller Felder

Feld	Typ	Bedeutung	Was du daraus lernen kannst	Good/Bad
timestamp	ISO-String	Zeitpunkt der Anfrage	Reihenfolge, Performance, Clusterbildung	Neutral
model	String	Benutztes GPT-Modell	Qualitätsvergleich, Kostenanalyse	Neutral
prompt_in	String	Ursprünglicher User-Input	Themenanalyse, User-Pfade	Neutral
prompt_out	String	GPT-generierter Meta-Prompt	Qualität, Struktur, Länge	Je strukturierter → desto besser
error	String/null	Fehlerart	Debugging, Policy-Hits	Fehler ≠ tot, aber relevant
success	Boolean	Hat GPT geantwortet?	Systemstabilität	true = gut
duration_ms	int	Dauer der GPT-Response	Performance, Model-Latenz	< 8000ms optimal
retry_count	int	Neuversuche	Instabilität, Throttling	0 optimal


⸻

🔍 Detailanalyse zu jedem Feld

🕒 timestamp

Was du daraus lesen kannst:
	•	Welche Themen wann abgefragt werden
	•	Welche Uhrzeiten problematisch sind (OpenAI-Lags)
	•	Batch-Verhalten
	•	Peak-Last-Zeiten

🤖 model

Wichtig für:
	•	Vergleich der Meta-Prompt-Qualität
	•	Kostenkontrolle: 4o billig, Opus teuer
	•	Änderung des Systemverhaltens über Zeit

🧠 prompt_in

Interpretation:
	•	Welche Themen schwierig oder komplex sind
	•	Nützlich für Heatmaps
	•	Erkennbar: “Bei Thema X macht GPT Fehler oder zickt herum.”

📤 prompt_out

Das eigentliche Gold.

Du kannst hier:
	•	GPT-Qualität tracken
	•	Backtracking (“Warum wurde der SYNTX-Score schlecht?”)
	•	Tokenlänge analysieren
	•	Stil-Inkonsistenzen erkennen
	•	Bias-Analyse durchführen

⚠️ error

Das zeigt dir:
	•	Policy-Eingriffe
	•	Rate-Limits
	•	Netzwerkausfälle
	•	Model-Müdigkeit (ja, das passiert!)

Sehr nützlich für:
	•	Stabilitätsanalyse
	•	Cronjob-Resilienz

✔️ success

Nur ein Boolean, aber entscheidend:
	•	true → wie erwartet
	•	false → Fail (wird retryed, je nach Script)

Wenn du über Zeit viele false siehst →
Infrastructure Problem oder Policy-Update.

⏱️ duration_ms

Der härteste technische Diagnoseträger.

Weil du daraus erkennst:
	•	Model-Stabilität
	•	Systemlast
	•	Netzwerklatenz
	•	Zukunftsoptimierung (“Brauchen wir caching?”)
	•	Vergleich Performance GPT-4-mini vs 4o vs Opus

🔁 retry_count

Zeigt dir:
	•	wie oft OpenAI dich blockt
	•	ob du throttle-sensitive Bereiche hast
	•	ob Cronjobs zu schnell laufen
	•	ob du Sleep-Timers erhöhen musst

⸻

📘 2. SYNTX-Kalibrierungslogs (syntex_logs.jsonl)

Hier liegt die Hauptforschung.
Jeder Eintrag = ein kompletter SYNTX-Durchlauf:

GPT → Wrapper → Llama → Parser → Score


⸻

🧩 Tabellenübersicht aller Felder

Feld	Typ	Bedeutung	Wichtige Ableitungen	Good/Bad
timestamp	ISO-String	Zeitpunkt	Driftanalyse, Cluster	Neutral
topic	String	Ausgangsthema	Inhaltlicher Kontext	Neutral
model	String	Verwendetes Modell	Vergleich der Modelle	Neutral
meta_prompt	String	GPT-Ausgabe	Qualitätskontrolle	Je klarer, desto besser
wrapped_prompt	String	Finaler Prompt	Wrapper-Debugging	Muss sauber strukturiert sein
raw_response	String	Llama-Rohantwort	Modelverhalten, Emergenz	Variiert
parsed	Object	Parser-Ausgabe	Vollständigkeit der Struktur	6/6 Pflicht
score	int	SYNTX-Quality Score	Messung struktureller Intelligenz	95–100 ideal
duration_ms	int	Laufzeit	Hinweis auf Serverpower	10–20k gut
retry_count	int	Versuche	Instabilität	0 ideal


⸻

🔍 Tiefenanalyse aller Felder

📌 topic

Das Thema, das durch die Pipeline geschickt wurde.

Daraus kannst du ableiten:
	•	Welche Themen schwerer sind
	•	Wie Meta-Prompts über Themen hinweg variieren
	•	Ob SYNTX bei sensibilen Themen anders reagiert
	•	Ob Emergenz (eigene Codes, neue Skalen) an bestimmte Themen gebunden ist

⸻

📌 meta_prompt

Das ist GPT’s „Storyline“.

Wichtig, weil:
	•	Einfluss auf SYNTX-Score
	•	Einfluss auf Drift
	•	Einfluss auf Emergenz
	•	Du kannst Fehlerbestrahlung machen („warum MN-12 statt MN-04?“)

⸻

📌 wrapped_prompt

Das ist das komplette fertige Konstrukt:
	•	Header
	•	Strukturmarker
	•	Slots
	•	GPT-Content

Daraus erkennst du:
	•	Tokenverbrauch
	•	AI-Verständnis des Wrappers
	•	ob der Model-Kontext korrekt gesetzt wurde
	•	ob Syntaxfehler im Wrapper sind

Wenn der Wrapper Fehler hat → Score sinkt.

⸻

📌 raw_response

Das ungefilterte Modellverhalten.

Extrem wichtig für:
	•	echten Drift
	•	Emergenz
	•	Musterveränderungen
	•	Stabilität
	•	Sprachqualität
	•	Regelkonformität
	•	Debugging des Parsers

Hier erkennst du:
	•	Warum ein Feld fehlt
	•	Warum Score sinkt
	•	Warum Llama neue Codes erfindet
	•	Ob eine Terminologie zu komplex war

⸻

📌 parsed

Die vollständig extrahierten 6 Felder.

parsed[“drift”]

Zeigt COHERENCE:
	•	stabil
	•	instabil
	•	kippt
	•	abrupt

Hier erkennst du:
	•	ob das Modell klare Logik hat
	•	ob das Thema schwierig war
	•	ob der Wrapper kohärent ist

parsed[“hintergrund_muster”]

Zeigt Systemlogik:
	•	Rückzug
	•	Überforderung
	•	Selbstschutz
	•	Prioritätswechsel

Daraus lernst du:
	•	wie das Modell Beziehungen/Felddarstellung bewertet
	•	wie tief die Analytik reicht

parsed[“druck”]

Zeigt:
	•	Belastung
	•	Erwartungsintensität
	•	systemische Dynamiken

parsed[“tiefe”]

Zeigt:
	•	oberflächlich
	•	mittlere Komplexität
	•	tiefpsychologisch

parsed[“wirkung”]

Zeigt:
	•	Sender/Empfänger
	•	Wirkungsstrom

parsed[“klartext”]

Das destillierte „Was passiert hier?“

⸻

📌 score

Der wichtigste Messwert.

Score setzt sich zusammen aus:

Bereich	Gewicht	Bedeutung
Strukturtreue	33%	Hat es alle Marker respektiert?
Feld-Vollständigkeit	34%	6/6 Felder?
Semantische Passung	33%	Sind die Inhalte relevant?

Interpretation:
	•	98–100 → Modell versteht Frame
	•	90–97 → leichte Abweichung
	•	80–89 → semantisches Rutschen
	•	<80 → Frame nicht gehalten
	•	<50 → Notfall, Wrapper falsch/Modell driftet

⸻

📌 duration_ms

Dein Server-Health-Indikator.

Interpretation:

Zeit	Bedeutung
< 25s	Sehr gut
25–40s	Stabil auf Mittelhardware
40–70s	Überlastung
> 70s	Server kann nicht mehr

Wenn du 504er hast →
Hardwareproblem, kein Codeproblem.

⸻

📌 retry_count

Wenn > 0:
	•	Timeout
	•	504
	•	Modell ist erstickt
	•	Sleep-Time zu gering
	•	CPU zu klein
	•	zu viele parallele Requests

⸻

🧭 Was du alles aus diesen Logs ablesen kannst (TrueRaw, vollständig)

🔥 1. Wrapper-Stabilität

Wenn Scores fallen → Wrapper verbessern.

🔥 2. Modellintelligenz

Emergenz wie neue Mechanismus-Codes → in raw_response sichtbar.

🔥 3. Systemdrift

Wenn parsed-Felder seltsam gefüllt sind → Modell hat Drift.

🔥 4. Latenzmonitoring

duration_ms zeigt:
„Brauchen wir 64GB? Brauchen wir schneller?“

🔥 5. Qualitätskorrelation

Welche Themen → beste Scores.

🔥 6. Meta-Prompt-Qualität

Je klarer GPT liefert → desto besser SYNTX.

🔥 7. Full Pipeline Health

Wenn GPT + Wrapper + Llama gut → Score 95+.

🔥 8. Batchverhalten

Bei Batch 3,5,10 → erkennst du:
„Wird der Server warm?“

🔥 9. Debugging

error + retry_count = Debug-Waffe.

🔥 10. Veränderung über Zeit

Du kannst visualisieren:

Score(t)
Duration(t)
Model Drift(t)
Emergenz(t)


⸻



