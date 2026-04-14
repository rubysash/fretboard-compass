# Scale + Chord Progression: Project Specifications

## Overview
A Flask-based "Positional Music Theory Suite" that mathematically generates and visualizes guitar scales, chords, and progressions. It features a "Theory Detective" for key inference and is optimized for standard 8.5x11 portrait printing.

## Core Files & Purposes

### 1. `app/theory/engine.py` (The Theory Library)
**Purpose:** The central database for musical math.
- **Where to add "Moods":** Update the `SCALES` and `SCALE_METADATA` dictionaries.
- **Where to add "Patterns":** Update the `PROGRESSION_PRESETS` dictionary.
- **Chord Math:** Contains `CHORD_TYPES` and `get_chord_notes`.
- **Key Detection:** Houses the `detect_key_and_mood` (Theory Detective) function.

### 2. `app/theory/solver.py` (The Fretboard Brain)
**Purpose:** Translates raw notes into physical (string, fret) coordinates.
- **Playability Logic:** `get_alternative_fingerings` filters out unplayable stretches.
- **Window Search:** `find_notes_in_window` maps scales across specific neck positions.

### 3. `app/graphics/svg_builder.py` (The Artist)
**Purpose:** Generates raw SVG strings for diagrams.
- **Visual Constants:** Define string spacing (`STRINGS_X`), fret spacing (`FRETS_Y`), and "Nut" thickness.
- **Classes:** `FretboardDiagram` (vertical chords) and `FullNeckDiagram` (horizontal 12-fret scales).

### 4. `app/templates/index.html` (The Dashboard)
**Purpose:** Main UI and Print Configuration.
- **Tooltips:** Contains the floating help system for Steps 1-3 and Start Fret.
- **Print CSS:** The `@media print` section controls the 5-across chord grid and portrait 8.5x11 layout.
- **HTMX Logic:** Handles the live swapping of chord presets and sheet generation.

### 5. `app/services/workbook_service.py` (The Orchestrator)
**Purpose:** Coordinates the pipeline between the Engine, Solver, and Artist.
- **Data Flow:** Packages theory data and SVG strings into a `workbook` object for the templates.

## Expansion Guide

### To add a new Scale (Mood):
1. Open `app/theory/engine.py`.
2. Add the interval pattern to `SCALES` (e.g., `[0, 2, 3, 5, 7, 8, 10]` for Minor).
3. Add a user-friendly name to `SCALE_METADATA`.

### To add a new Progression (Pattern):
1. Open `app/theory/engine.py`.
2. Add an entry to `PROGRESSION_PRESETS` with a name and the list of scale degrees (e.g., `[1, 6, 4, 5]`).

### To adjust Print Layout:
1. Open `app/templates/index.html`.
2. Locate the `@media print` section.
3. Adjust `width: 19%` on `.chord-card` to change the number of columns per row.

## Architecture & Constraints
- **Orientation:** Optimized for **Portrait** (8.5x11).
- **Interactivity:** HTMX handles all backend calls; Base64 encoding allows instant SVG swapping in the browser.
- **Math:** 0-indexed intervals are used throughout (0=Root, 7=Fifth).
