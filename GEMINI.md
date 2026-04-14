# ChordDumper Project Specifications

## Overview
ChordDumper is a Python-based utility designed to transform music theory data (chords, scales, and progressions) stored in Excel spreadsheets into visual aids. It currently generates SVG diagrams and HTML reports intended for browser-based printing to PDF.

## Core Features
- **Data Source:** Reads from `chords9.xlsx` with three mandatory tabs: `chords`, `favs` (progressions), and `scales`.
- **Diagram Generation:** Uses `svgwrite` to create vector-based guitar chord and scale diagrams.
- **HTML Reporting:** Aggregates diagrams into categorized HTML files (`chords.html`, `favs.html`, `scales.html`) with intelligent page-break logic for printing.
- **Verification System:** Highlights unverified data (where `VERIFIED=0`) in pink for easy identification.

## Technical Stack
- **Language:** Python 3.12+
- **Theory Engine:** `theory_engine.py` (Calculates scales, modes, and chord intervals mathematically)
- **Data Handling:** `openpyxl` (Excel), `collections.OrderedDict`, `json`
- **Graphics:** `svgwrite` (SVG generation)
- **CLI:** `getopt`, `colorama`
- **Output:** HTML/SVG (Web-viewable)

## Project Skills

### 1. Music Theory Solver (`theory_engine.py`)
This component acts as the "brain" of the project. It can:
- **Generate Scales:** Input a Root (e.g., "A") and a Mode (e.g., "Dorian") to receive a list of notes.
- **Construct Chords:** Calculate notes for Major, Minor, 7th, Maj7, and other extensions on the fly.
- **Fretboard Mapping:** Translate note names into (string, fret) coordinates for any position on the guitar neck.
- **Mode Matching:** Suggest compatible scales for a given chord or progression (e.g., Am7 in G Major -> A Dorian).

## Operational Guidelines (API & Rate Limits)

### 1. Handling 429 Errors (Rate Limits)
- **Proactive Warning:** If the agent detects a 429 error (Too Many Requests), it must immediately stop and notify the user in plain text: "⚠️ RATE LIMIT DETECTED (429) - PAUSING FOR 15-30 SECONDS."
- **Backoff:** Wait at least 15 seconds before retrying any tool calls.
- **Visibility:** User should set `/config set ui.errorVerbosity "full"` to see recoverable errors in the CLI.

### 2. Context Efficiency
- **Batching:** Always combine research (reading) and execution (writing/editing) into single turns whenever possible to preserve API quota.
- **Session Reset:** Periodically restart the CLI session to clear the conversation history and reduce the token cost per turn.
- **Ignore Rules:** Maintain a strict `.geminiignore` (ignoring `Scripts/`, `Lib/`, `Include/`, `__pycache__/`) to prevent wasted context scanning.

## Proposed Enhancements

### 1. Application Framework
To provide a more interactive experience, we can move from a CLI-only tool to:
- **Flask (Recommended):** Ideal for a web-based dashboard where you can select specific scales/chords and generate a PDF on the fly. Easier to style with modern CSS.
- **PyQt5:** Better for a standalone desktop application with a native feel.

### 2. PDF Generation
Instead of relying on browser printing, we can integrate:
- **ReportLab:** A powerful library for generating complex PDFs directly from Python.
- **WeasyPrint:** Excellent for converting HTML/CSS (like the current output) directly into high-quality PDFs.

### 3. Music Theory Content
- **Scales:** Expand beyond Major/Minor to include Modes (Dorian, Phrygian, etc.), Pentatonic, and Blues scales.
- **Chords:** Add more voicings, extensions (7ths, 9ths, 13ths), and inversions.
- **Theory Integration:** Add text sections explaining the relationship between the chosen scales and the chords in a progression.

## Planned Roadmap
- [ ] **Phase 1:** Refactor data loading to a more robust `ChordProvider` class.
- [ ] **Phase 2:** Implement a Flask-based UI for browsing the database.
- [ ] **Phase 3:** Integrate `WeasyPrint` for "Export to PDF" functionality.
- [ ] **Phase 4:** Expand `chords9.xlsx` with comprehensive theory data.
