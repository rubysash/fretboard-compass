# Fretboard Compass Project Specifications

## Overview
Fretboard Compass is a high-performance Music Theory Suite for guitarists. It transforms complex theory into printable, "Binder-Ready" practice sheets. It features a mathematical theory engine that calculates diatonic chords across exotic scales and maps them to the fretboard using the CAGED system.

## Core Features
- **Pro Theory Engine:** Dynamically calculates triads and Roman Numerals for 20+ scales, including exotic moods like Byzantine and Spanish Gypsy.
- **Visual Mastery:**
    - **Vertical Chords:** Symmetrical 5-column grid optimized for 8.5x11 Portrait printing.
    - **Horizontal Scales:** 12-fret neck maps with "Diamond Root" markers and "Positional Zoning" (Color-coded zones for Frets 1-4, 5-8, and 9-12).
- **Interactive Library:**
    - **Proven Winners:** A dashboard of 20 timeless chord/scale combinations with play-style tips and sample songs.
    - **Pattern Presets:** 22 standard and advanced progressions synced with professional theory benchmarks.
- **Favorites System:** Save custom combinations with a Title and Description (e.g. "distortion settings", "fingerpicking style"). Persistent JSON storage for custom vibes.
- **Solver Sync:** Entering a manual progression automatically updates the "Note" and "Mood" dropdowns to match the detected theory.
- **Student Ready:** Built-in "One Neighborhood" practice guide and printable drill sheets.

## Technical Stack
- **Version:** v0.1.2
- **Backend:** Flask (Python 3.12+)
- **Frontend:** HTMX (AJAX without JS), Tailwind CSS (Modern Styling)
- **Graphics:** svgwrite (Dynamic vector generation)
- **Infrastructure:** Local development ready; Cloudflare Workers (Edge) roadmap.

## Documentation Standards
- **Emoji Usage:** NEVER use emojis in any output documentation (README.md, GEMINI.md, etc.) except for the README.md which has a sign of the horns (🤘) after the last line "...for guitarists ..."
- application code may use specific music symbols if they are standard and best practice, but not emojies for general header/comment text output, which should always appear as professional output.
- applicaiton code should prefer svg icons from free font awesome resources if needed (the star for favorites), and should avoid smart quotes, em dashes, and other use of emojies not already specified.

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

## Project Architecture
- app/theory/engine.py: The "Brain". Mathematical interval and triad calculation.
- app/theory/solver.py: The "Navigator". Finds optimal fingerings and movable CAGED shapes.
- app/graphics/svg_builder.py: The "Artist". Handles all vector rendering and positional color zoning.
- app/templates/: Pure HTML/HTMX partials for ultra-fast UI swaps.
- favorites/: Local JSON storage for user favorites.

## Strategic Roadmap
- [x] Full CAGED movable voicing support.
- [x] Mathematical triad building for exotic scales.
- [x] "Proven Winners" interactive dashboard.
- [x] Favorites system with Titles and Descriptions.
- [ ] TypeScript port for Cloudflare Workers deployment.
- [ ] Stripe integration for "Pro" tier features.
