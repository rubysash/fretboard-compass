# Fretboard Compass: Music Theory Suite for Guitarists

[![Interface Demo](demo.jpg)](https://github.com/rubysash/fretboard-compass/blob/main/demo.jpg)
[![Presets](demo2.jpg)](https://github.com/rubysash/fretboard-compass/blob/main/demo2.jpg)
[![Printable Sheet](demo3.jpg)](https://github.com/rubysash/fretboard-compass/blob/main/demo3.jpg)

**Fretboard Compass** is a professional-grade Music Theory Suite for guitarists. It transforms complex intervals, exotic scales, and chord progressions into printable, "Binder-Ready" practice materials.

Designed for students and teachers, it takes the guesswork out of the fretboard by mathematically calculating every note and fingering.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.12%2B-blue.svg)
![Flask](https://img.shields.io/badge/framework-Flask-lightgrey.svg)
![HTMX](https://img.shields.io/badge/frontend-HTMX-orange.svg)

---

## Key Features

### Pro Theory Engine
- **Analytical Triad Building:** Dynamically constructs Major, Minor, Diminished, Augmented, and Suspended chords from any 7-note scale.
- **Harmonic Borrowing:** Smart logic for presets (like Flamenco and Jazz) that prioritizes musicality over robotic diatonicism.
- **Dynamic Roman Numerals:** Context-aware Nashville numbering that handles accidentals (bII, #IV) and proper casing (I vs i).

### Visual Fretboard Mastery
- **Positional Zoning:** The neck is divided into three high-contrast color zones (Zone 1: Black, Zone 2: Blue, Zone 3: Purple) to help students master one "neighborhood" at a time.
- **Diamond Roots:** Instant geometric identification of the scale root across the entire 12-fret map.
- **CAGED System:** Automatically finds standard movable shapes for any chord, anywhere on the neck.

### Interactive Discovery
- **Proven Winners:** A dashboard of 20 timeless chord/scale combinations (e.g. "The Anthem," "Cinematic Doom," "12-Bar Shuffle") with play-style tips.
- **Favorites System:** Save your custom "vibes" with Titles and Descriptions (e.g. "bridge pickup settings"). Persistent JSON storage for easy recall.
- **Solver Sync:** Entering a manual progression now automatically updates the Note and Mood dropdowns to match the detected theory.
- **One Neighborhood Guide:** A built-in, printable practice manual for mastering the neck in 30 minutes a day.

---

## Tech Stack

- **Backend:** Python 3.12+ / Flask
- **Frontend:** HTMX (Interactivity), Tailwind CSS (Aesthetics)
- **Graphics:** svgwrite (Vector Diagram Generation)
- **Print:** Optimized CSS @media print for 8.5x11 Portrait symmetry.

---

## Quick Start

### 1. Clone & Setup
```bash
git clone https://github.com/rubysash/fretboard-compass.git
python -m venv fretboard-compass
cd fretboard-compass
Scripts\activate
python -m pip install pip --upgrade pip
python -m pip install -r requirements.txt
```

### 2. Run the Suite
```bash
python run.py
```
Visit http://127.0.0.1:5000 in your browser.

### 3. Generate & Print
1. Click "Proven Winners" to load a classic combination.
2. Hit "Generate Sheet".
3. Use the Fingering Selector on any chord card to match your preferred "Neighborhood".
4. Press "Print" to generate a perfect 8.5x11 practice sheet for your binder.

---

## Roadmap
- [x] Full CAGED movable voicing support.
- [x] Mathematical triad building for exotic scales.
- [x] "Proven Winners" interactive dashboard.
- [x] Favorites system with Titles and Descriptions.
- [ ] TypeScript port for Cloudflare Workers deployment.
- [ ] Stripe integration for "Pro" tier features.

---

## Version Log

### v0.1.2
- **Fixed Favorites Saving:** Wrapped the Save Favorite form in a proper form element to ensure custom titles and descriptions are correctly captured and persisted alongside the theory data.
- **Improved Visuals:** Enhanced the readability of the Favorite cards by adjusting the description font size and leading.

### v0.1.1
- **Solver Sync:** Entering a manual progression now automatically updates the "Note" and "Mood" dropdowns to match the detected theory.
- **Enhanced Favorites:** Added support for custom Titles and Descriptions when saving favorites.
- **Interactive UI:** The Star button now opens an inline form for better context.

### v0.1.0
- Initial professional release of **Fretboard Compass**.
- Implemented **Proven Winners** and **Favorites** systems.
- Added **Positional Zoning** and **Diamond Roots** to SVG engine.
- Integrated **HTMX** for seamless UI updates.
- Established **Binder-Ready** 8.5x11 printing layout.

---

*Created for guitarists who want to spend less time thinking about dots and more time making music.* 🤘
