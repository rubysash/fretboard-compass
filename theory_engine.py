"""
Music Theory Engine for ChordDumper.
Handles the math behind scales, chords, and intervals.
"""

# Intervals in semitones
INTERVALS = {
    'P1': 0, 'm2': 1, 'M2': 2, 'm3': 3, 'M3': 4, 'P4': 5,
    'A4': 6, 'd5': 6, 'P5': 7, 'm6': 8, 'M6': 9, 'm7': 10, 'M7': 11, 'P8': 12
}

# Scale patterns (in semitones from root)
SCALES = {
    'major': [0, 2, 4, 5, 7, 9, 11],
    'minor': [0, 2, 3, 5, 7, 8, 10],
    'dorian': [0, 2, 3, 5, 7, 9, 10],
    'phrygian': [0, 1, 3, 5, 7, 8, 10],
    'lydian': [0, 2, 4, 6, 7, 9, 11],
    'mixolydian': [0, 2, 4, 5, 7, 9, 10],
    'locrian': [0, 1, 3, 5, 6, 8, 10],
    'pentatonic_major': [0, 2, 4, 7, 9],
    'pentatonic_minor': [0, 3, 5, 7, 10],
}

# Note mapping
NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

def get_notes_in_scale(root, scale_type):
    """Returns the notes for a given scale and root."""
    root = root.capitalize()
    if root not in NOTES:
        # Handle flats if needed, but for simplicity sticking to sharps
        flat_map = {'Db': 'C#', 'Eb': 'D#', 'Gb': 'F#', 'Ab': 'G#', 'Bb': 'A#'}
        root = flat_map.get(root, 'C')
    
    start_idx = NOTES.index(root)
    pattern = SCALES.get(scale_type.lower(), SCALES['major'])
    
    scale_notes = []
    for interval in pattern:
        note_idx = (start_idx + interval) % 12
        scale_notes.append(NOTES[note_idx])
    
    return scale_notes

def get_chord_notes(root, chord_type='major'):
    """Calculates notes for basic chord types."""
    chord_patterns = {
        'major': [0, 4, 7],
        'minor': [0, 3, 7],
        '7': [0, 4, 7, 10],
        'maj7': [0, 4, 7, 11],
        'm7': [0, 3, 7, 10],
        'dim': [0, 3, 6],
    }
    
    root_idx = NOTES.index(root.capitalize())
    pattern = chord_patterns.get(chord_type.lower(), chord_patterns['major'])
    
    return [NOTES[(root_idx + i) % 12] for i in pattern]

# Guitar Fretboard Mapping (Standard Tuning)
STRINGS = ['E', 'A', 'D', 'G', 'B', 'E'] # 6 to 1

def get_fret_positions(notes, start_fret=1, num_frets=5):
    """
    Finds where specific notes appear on the fretboard within a window.
    This is the core for generating the 'DOTS' for your SVG.
    """
    positions = []
    for string_idx, open_note in enumerate(STRINGS):
        string_root_idx = NOTES.index(open_note)
        # Check each fret in the window
        for fret in range(start_fret, start_fret + num_frets):
            current_note = NOTES[(string_root_idx + fret) % 12]
            if current_note in notes:
                # We need to map this to your SVG coordinate system
                # (This is just a placeholder for the logic)
                positions.append((string_idx, fret, current_note))
    return positions

if __name__ == "__main__":
    # Test
    print(f"A Minor Scale: {get_notes_in_scale('A', 'minor')}")
    print(f"Am Chord Notes: {get_chord_notes('A', 'minor')}")
    print(f"Positions for Am (Frets 1-5): {get_fret_positions(get_chord_notes('A', 'minor'), 1, 5)}")
