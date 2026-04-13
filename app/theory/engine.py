"""
Theory Engine Core.
Handles intervals, scales, and chord construction logic.
"""
import logging
from typing import List, Dict, Optional, Any, Tuple

logger = logging.getLogger(__name__)

# Constants
NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

SCALES = {
    'major': [0, 2, 4, 5, 7, 9, 11],
    'minor': [0, 2, 3, 5, 7, 8, 10],
    'dorian': [0, 2, 3, 5, 7, 9, 10],
    'phrygian': [0, 1, 3, 5, 7, 8, 10],
    'lydian': [0, 2, 4, 6, 7, 9, 11],
    'mixolydian': [0, 2, 4, 5, 7, 9, 10],
    'locrian': [0, 1, 3, 5, 6, 8, 10],
}

CHORD_TYPES = {
    'major': [0, 4, 7],
    'minor': [0, 3, 7],
    '7': [0, 4, 7, 10],
    'maj7': [0, 4, 7, 11],
    'm7': [0, 3, 7, 10],
    'dim': [0, 3, 6],
}

def normalize_note(note: str) -> str:
    """Converts flats to sharps and ensures consistent casing."""
    note = note.capitalize()
    flat_map = {
        'Db': 'C#', 'Eb': 'D#', 'Gb': 'F#', 'Ab': 'G#', 'Bb': 'A#'
    }
    return flat_map.get(note, note)

def get_notes_in_scale(root: str, scale_type: str) -> List[str]:
    """Calculates the notes for a given scale."""
    root = normalize_note(root)
    logger.debug(f"Calculating {root} {scale_type} scale")
    
    if root not in NOTES:
        logger.error(f"Invalid root note: {root}")
        return []
        
    start_idx = NOTES.index(root)
    pattern = SCALES.get(scale_type.lower(), SCALES['major'])
    
    notes = [NOTES[(start_idx + i) % 12] for i in pattern]
    logger.debug(f"Generated notes: {notes}")
    return notes

def get_chord_notes(root: str, chord_type: str = 'major') -> List[str]:
    """Calculates notes for a specific chord type."""
    logger.debug(f"Calculating {root} {chord_type} chord")
    
    root = normalize_note(root)
    if root not in NOTES:
        return []
        
    root_idx = NOTES.index(root)
    pattern = CHORD_TYPES.get(chord_type.lower(), CHORD_TYPES['major'])
    
    notes = [NOTES[(root_idx + i) % 12] for i in pattern]
    logger.debug(f"Generated notes: {notes}")
    return notes

def get_key_from_progression(progression: List[str]) -> Tuple[str, str]:
    """
    Infers the most likely key (Root and Type) from a list of chords.
    Standard: The first chord is often the tonic (root).
    """
    if not progression:
        return 'C', 'major'
        
    first_chord = progression[0]
    
    # Split root from type (e.g. Am -> A, m)
    root = first_chord[0]
    if len(first_chord) > 1 and first_chord[1] in ['#', 'b']:
        root = first_chord[:2]
        chord_type = first_chord[2:]
    else:
        chord_type = first_chord[1:]
        
    is_minor = any(x in chord_type.lower() for x in ['m', 'minor'])
    return normalize_note(root), 'minor' if is_minor else 'major'

# Standard Voicings for common chords (String 6 to 1)
STANDARD_VOICINGS = {
    'C':  [None, 3, 2, 0, 1, 0],
    'A':  [None, 0, 2, 2, 2, 0],
    'G':  [3, 2, 0, 0, 0, 3],
    'E':  [0, 2, 2, 1, 0, 0],
    'D':  [None, None, 0, 2, 3, 2],
    'Am': [None, 0, 2, 2, 1, 0],
    'Dm': [None, None, 0, 2, 3, 1],
    'Em': [0, 2, 2, 0, 0, 0],
    'F':  [1, 3, 3, 2, 1, 1],
    'B':  [None, 2, 4, 4, 4, 2],
    'Bb': [None, 1, 3, 3, 3, 1],
    'F#m': [2, 4, 4, 2, 2, 2],
    'Bm': [None, 2, 4, 4, 3, 2],
    'B7': [None, 2, 1, 2, 0, 2],
    'Bm7': [None, 2, 0, 2, 0, 2],
}

def get_standard_voicing(name: str) -> Optional[List[Any]]:
    """Returns a standard voicing if it exists."""
    return STANDARD_VOICINGS.get(name)

# Standard Guitar Tuning (6th string to 1st string)
STRINGS = ['E', 'A', 'D', 'G', 'B', 'E']

def get_nashville_number(key_root: str, key_type: str, chord_name: str) -> str:
    """
    Returns the Nashville Number (I, ii, etc.) for a chord in a given key.
    """
    key_root = normalize_note(key_root)
    # Basic Major/Minor scale degree maps
    major_degrees = ['I', 'ii', 'iii', 'IV', 'V', 'vi', 'vii°']
    minor_degrees = ['i', 'ii°', 'III', 'iv', 'v', 'VI', 'VII']
    
    # Get notes in the scale to find the index
    scale_notes = get_notes_in_scale(key_root, key_type)
    
    # Extract the chord's root note (e.g., 'Am' -> 'A')
    chord_root = chord_name[0]
    if len(chord_name) > 1 and chord_name[1] in ['#', 'b']:
        chord_root = chord_name[:2]
    chord_root = normalize_note(chord_root)
    
    if chord_root not in scale_notes:
        return "?"
        
    idx = scale_notes.index(chord_root)
    if key_type.lower() == 'minor':
        return minor_degrees[idx]
    return major_degrees[idx]

def get_note_at_fret(open_note: str, fret: int) -> str:
    """Calculates the note at a specific fret on a string."""
    start_idx = NOTES.index(open_note.upper())
    return NOTES[(start_idx + fret) % 12]
