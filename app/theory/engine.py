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
    'phrygian_dominant': [0, 1, 4, 5, 7, 8, 10], 
    'harmonic_minor': [0, 2, 3, 5, 7, 8, 11],
    'lydian': [0, 2, 4, 6, 7, 9, 11],
    'mixolydian': [0, 2, 4, 5, 7, 9, 10],
    'locrian': [0, 1, 3, 5, 6, 8, 10],
    'pentatonic_major': [0, 2, 4, 7, 9],
    'pentatonic_minor': [0, 3, 5, 7, 10],
    'blues': [0, 3, 5, 6, 7, 10],
}

SCALE_METADATA = {
    'major': 'Standard Major',
    'minor': 'Natural Minor',
    'dorian': 'Jazz / Funk (Dorian)',
    'phrygian': 'Standard Spanish (Phrygian)',
    'phrygian_dominant': 'Spanish Gypsy (Phrygian Dom)',
    'harmonic_minor': 'Classical Spanish (Harmonic)',
    'lydian': 'Dreamy / Spacey (Lydian)',
    'mixolydian': 'Bluesy / Rock (Mixolydian)',
    'locrian': 'Dark / Tense (Locrian)',
    'pentatonic_major': 'Major Pentatonic',
    'pentatonic_minor': 'Minor Pentatonic',
    'blues': 'The Blues Scale',
}

PROGRESSION_PRESETS = {
    'pop_rock': {'name': 'I - V - vi - IV (Pop/Rock)', 'degrees': [1, 5, 6, 4]},
    'jazz_ii_v_i': {'name': 'ii - V - I (Standard Jazz)', 'degrees': [2, 5, 1]},
    'blues_12_bar': {'name': 'I - IV - V (12-Bar Blues)', 'degrees': [1, 4, 1, 5, 4, 1]},
    'minor_blues': {'name': 'i - iv - v (Minor Blues)', 'degrees': [1, 4, 5]},
    'flamenco': {'name': 'i - VII - VI - V (Spanish/Flamenco)', 'degrees': [1, 7, 6, 5]},
}

# Standard Voicings (Human Playable)
# String 6 to 1. None=X, 0=O, int=fret
STANDARD_VOICINGS = {
    # Majors
    'C':  [None, 3, 2, 0, 1, 0], 'A': [None, 0, 2, 2, 2, 0], 'G': [3, 2, 0, 0, 0, 3],
    'E':  [0, 2, 2, 1, 0, 0], 'D': [None, None, 0, 2, 3, 2], 'F': [1, 3, 3, 2, 1, 1],
    'B':  [None, 2, 4, 4, 4, 2], 'Bb': [None, 1, 3, 3, 3, 1],
    
    # Minors
    'Am': [None, 0, 2, 2, 1, 0], 'Dm': [None, None, 0, 2, 3, 1], 'Em': [0, 2, 2, 0, 0, 0],
    'F#m': [2, 4, 4, 2, 2, 2], 'Bm': [None, 2, 4, 4, 3, 2], 'Cm': [None, 3, 5, 5, 4, 3],
    'Gm': [3, 5, 5, 3, 3, 3], 'Fm': [1, 3, 3, 1, 1, 1],
    
    # 7ths
    'C7': [None, 3, 2, 3, 1, 0], 'A7': [None, 0, 2, 0, 2, 0], 'G7': [3, 2, 0, 0, 0, 1],
    'E7': [0, 2, 0, 1, 0, 0], 'D7': [None, None, 0, 2, 1, 2], 'B7': [None, 2, 1, 2, 0, 2],
    
    # Diminished (Playable versions)
    'G#dim': [None, None, 0, 1, 0, 1], # Simple D-shape variant
    'F#dim': [None, None, 4, 2, 1, None], # Top-triad
    'Bdim': [None, 2, 3, 4, 3, None],
    'D#dim': [None, None, 1, 2, 1, 2],
}

def normalize_note(note: str) -> str:
    note = note.capitalize()
    flat_map = {'Db': 'C#', 'Eb': 'D#', 'Gb': 'F#', 'Ab': 'G#', 'Bb': 'A#'}
    return flat_map.get(note, note)

def get_chord_from_degree(key_root: str, key_type: str, degree: int) -> str:
    key_root = normalize_note(key_root)
    root_idx = NOTES.index(key_root)
    if 'phrygian' in key_type or 'harmonic' in key_type:
        scale_map = {1: (0, 'm'), 7: (10, ''), 6: (8, ''), 5: (7, '')}
    elif key_type == 'blues':
        scale_map = {1: (0, '7'), 4: (5, '7'), 5: (7, '7')}
    elif 'minor' in key_type:
        scale_map = {1: (0, 'm'), 2: (2, 'dim'), 3: (3, ''), 4: (5, 'm'), 5: (7, 'm'), 6: (8, ''), 7: (10, '')}
    else:
        scale_map = {1: (0, ''), 2: (2, 'm'), 3: (4, 'm'), 4: (5, ''), 5: (7, ''), 6: (9, 'm'), 7: (11, 'dim')}
    
    if degree not in scale_map: return key_root
    interval, suffix = scale_map[degree]
    chord_root = NOTES[(root_idx + interval) % 12]
    return f"{chord_root}{suffix}"

CHORD_TYPES = {
    'major': [0, 4, 7], 'minor': [0, 3, 7], '7': [0, 4, 7, 10],
    'maj7': [0, 4, 7, 11], 'm7': [0, 3, 7, 10], 'dim': [0, 3, 6],
}

def get_notes_in_scale(root: str, scale_type: str) -> List[str]:
    root = normalize_note(root)
    start_idx = NOTES.index(root)
    pattern = SCALES.get(scale_type.lower(), SCALES['major'])
    return [NOTES[(start_idx + i) % 12] for i in pattern]

def get_chord_notes(root: str, chord_type: str = 'major') -> List[str]:
    root = normalize_note(root)
    root_idx = NOTES.index(root)
    pattern = CHORD_TYPES.get(chord_type.lower(), CHORD_TYPES['major'])
    return [NOTES[(root_idx + i) % 12] for i in pattern]

def get_key_from_progression(progression: List[str]) -> Tuple[str, str]:
    if not progression or not progression[0]: return 'C', 'major'
    first = progression[0]
    root = first[:2] if len(first) > 1 and first[1] in ['#', 'b'] else first[0]
    return normalize_note(root), 'minor' if 'm' in first[len(root):] else 'major'

def get_standard_voicing(name: str): return STANDARD_VOICINGS.get(name)
STRINGS = ['E', 'A', 'D', 'G', 'B', 'E']

def get_nashville_number(key_root: str, key_type: str, chord_name: str) -> str:
    kn = normalize_note(key_root)
    sn = get_notes_in_scale(kn, key_type)
    cr = normalize_note(chord_name[:2] if len(chord_name) > 1 and chord_name[1] in ['#', 'b'] else chord_name[0])
    if cr not in sn: return "?"
    idx = sn.index(cr)
    return ['i', 'ii°', 'III', 'iv', 'v', 'VI', 'VII'][idx] if 'minor' in key_type else ['I', 'ii', 'iii', 'IV', 'V', 'vi', 'vii°'][idx]

def get_note_at_fret(open_note: str, fret: int) -> str:
    return NOTES[(NOTES.index(open_note.upper()) + fret) % 12]
