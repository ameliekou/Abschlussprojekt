# EKG Data Analysis

Dieses Repository enthält eine Klasse `EKGData`, die verwendet wird, um die Herzfrequenz aus EKG-Daten zu schätzen und zu visualisieren.

## Installation

1. Klone das Repository:
    ```sh
    git clone <https://github.com/ameliekou/Abschlussprojekt>
    ```

2. Erstelle eine virtuelle Umgebung und aktiviere sie:
    ```sh
    python -m venv venv
    source venv/bin/activate  # Auf Windows: venv\Scripts\activate
    ```

3. Installiere die Abhängigkeiten:
    ```sh
    pip install -r requirements.txt
    ```

## Nutzung
öffnen sie ein neues Terminal in der main.py datei und geben sie folgenden Befehl ein:
```sh
   streamlit run main.py
 ```
Mit folgendem Link lässt sich die App öffnen: https://abschlussprojekt.streamlit.app/

## Übersicht
Diese Anwendung dient der Analyse von EKG-Daten und der Berechnung des Body-Mass-Index (BMI). Sie ermöglicht die Auswahl und Anzeige von EKG-Daten für verschiedene Personen, bietet Funktionen zur Visualisierung der Daten und zur Erfassung von Notizen. Darüber hinaus ermöglicht die Anwendung die Berechnung des BMI und die Darstellung der BMI-Kategorien in einem Kuchendiagramm.

## Funktionen

1. EKG-Daten
- Versuchsperson auswählen: Auswahl einer Versuchsperson aus einer Liste.
- Personeninformationen anzeigen: Geburtsdatum, Alter und ID der ausgewählten Person.
- EKG-Daten auswählen: Auswahl der verfügbaren EKG-Daten für die ausgewählte Person.
- EKG-Daten anzeigen: Darstellung der EKG-Daten einschließlich Datum, Dauer, durchschnittliche Herzfrequenz und maximale Herzfrequenz.
- EKG-Daten visualisieren: Darstellung der EKG-Zeitreihe mit anpassbarem Zeitbereich.
- Herzratenvariabilität (HRV) berechnen: Berechnung und Anzeige der Standardabweichung der RR-Intervalle als Maß für die HRV.

2. BMI Rechner
- Gewicht und Größe eingeben: Eingabe des Körpergewichts (in kg) und der Körpergröße (in cm).
- BMI berechnen: Berechnung und Anzeige des BMI.
- BMI-Kategorien anzeigen: Darstellung des BMI-Werts und der zugehörigen Kategorie (Untergewicht,           Normalgewicht, Übergewicht, Adipositas).
- Kuchendiagramm anzeigen: Visualisierung der BMI-Kategorien als Kuchendiagramm.
- Erklärung der BMI-Kategorien: Erklärung der jeweiligen Kategorie und Empfehlungen.

## Kontakt
Bei Fragen oder Problemen wenden Sie sich bitte an tp2941@mci4me.at oder ka7675@mci4me.at.