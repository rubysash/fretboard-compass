# Flask Version Specs: Positional Music Theory Suite

## Overview
A Flask-based web application designed to generate comprehensive "Music Theory Workbooks" for guitarists. It focuses on **Chord Progressions** and the **Scales** that match them, grouped by **Fretboard Position** to minimize neck movement.

## Core Mandate
"Generate high-quality, printable music theory sheets that tell a guitarist *exactly* what chords and scales to play together in a single position on the neck."

## Key Features

### 1. Progression-First Workflow
- **Input:** User defines a chord progression (e.g., `C - Am - F - G`).
- **Analysis:** The system identifies the Key (C Major) and the scale degree of each chord (`I - vi - IV - V`).
- **Scale Solver:** Automatically suggests the correct scale (C Major / A Minor) and specific modes (e.g., F Lydian over the F chord).

### 2. Positional Grouping (The "Minimum Movement" Engine)
- **Fret Window:** User selects a target position (e.g., "5th Position").
- **Smart Solver:** The engine calculates:
  - **Chord Voicings:** Finds the best fingerings for all chords in the progression *strictly within frets 5-9*.
  - **Scale Patterns:** Maps the full scale and specific patterns to that same fret window.
- **Full Neck View:** Generates a full-neck scale diagram for context.

### 3. Interactive Flask Dashboard
- **Progression Builder:** Drag-and-drop or select chords to build a song.
- **Position Selector:** A slider or dropdown to shift the entire theory sheet up/down the neck.
- **Real-time Preview:** See SVG diagrams update instantly as you change keys or positions.

### 4. Pro-Grade PDF Export
- **Layout:** Combines chord charts, scale diagrams, and theory notes into a clean, multi-page PDF.
- **Tooling:** Uses `WeasyPrint` for high-fidelity CSS-to-PDF conversion.

## Technical Architecture (Modular & Scalable)

The project follows a **Separation of Concerns** (SoC) approach, breaking logic into specialized modules to prevent "God Files" and ensure ease of testing.

### **Backend (Python 3.12+)**
- `app/`
    - `__init__.py`: Factory pattern for Flask app initialization.
    - `routes.py`: Lean routing logic (delegates to services).
    - `theory/`
        - `engine.py`: Core music theory math (Intervals, Scales, Chords).
        - `solver.py`: Positional logic (Finds "Minimum Movement" fingerings).
    - `graphics/`
        - `svg_builder.py`: Pure SVG generation logic using `svgwrite`.
        - `templates/`: SVG fragment templates for reusability.
    - `services/`
        - `pdf_service.py`: High-fidelity PDF generation using `WeasyPrint`.
        - `workbook_service.py`: Orchestrates the creation of full theory workbooks.

### **Frontend (Modern Web Standards)**
- **Tailwind CSS v4+:** For utility-first styling without large CSS overhead.
- **HTMX:** For "Interactivity without Javascript Fatigue"—updates diagrams via AJAX.
- **Alpine.js:** For lightweight client-side state (e.g., toggling UI panels).

## Best Practices & Standards (2026)

### 1. Code Quality & Style
- **PEP 8 Compliance:** Strict adherence to Python style guides.
- **Type Hinting:** Mandatory use of Python's `typing` module (e.g., `list[str]`, `dict[str, Any]`) for better IDE support and error catching.
- **Non-Deprecated Libraries:** 
    - Use `pathlib` over `os.path`.
    - Use `pydantic` for data validation (Excel/JSON inputs).
    - Use `WeasyPrint` (Active) over `pdfkit/wkhtmltopdf` (Legacy/Deprecated).

### 2. Documentation Requirements
- **Docstrings:** Every function/class must include a Google-style docstring explaining `Args`, `Returns`, and `Raises`.
- **Self-Documenting Code:** Prioritize expressive variable names over excessive comments.
- **README.md:** Must contain a "Quick Start" for local development and a "Theory Logic" overview.
- **API Specs:** Document internal JSON endpoints used by HTMX.

### 3. Development Workflow
- **Virtual Environments:** Always run within a `venv` or `conda` environment.
- **Modular Testing:** Use `pytest` for the `theory/` module.
- **Local-First Design:** Optimize for low-latency local execution.

### 4. Logging & Debugging Standards
- **Global Configuration:** A `config.py` file must control the `DEBUG` state.
- **Structured Logging:** Use Python's `logging` module to track each stage of the "Solver" and "Graphics" pipelines.
- **Execution Tracing:** Logs must detail:
    - Chord/Scale note calculations.
    - Fretboard position search results.
    - SVG generation parameters.
- **Independent Validation:** Logic should be testable via CLI or logs even without the Flask server running, ensuring the "Brain" is correct before the UI layer is involved.

## Development Roadmap
- [x] **Step 1:** Initial `theory_engine.py` (Basic Math).
- [ ] **Step 2:** Advanced Fretboard Solver (Find chords in specific positions).
- [ ] **Step 3:** Flask Prototype (Basic UI with SVG previews).
- [ ] **Step 4:** PDF Export Integration.
- [ ] **Step 5:** "Theory Insights" (Adding text explaining *why* a scale matches a chord).
