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
    'melodic_minor': [0, 2, 3, 5, 7, 9, 11],
    'double_harmonic': [0, 1, 4, 5, 7, 8, 11], # Arabic/Byzantine
    'lydian': [0, 2, 4, 6, 7, 9, 11],
    'lydian_dominant': [0, 2, 4, 6, 7, 9, 10], # Overtone scale
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
    'melodic_minor': 'Jazz Minor (Melodic)',
    'double_harmonic': 'Arabic / Byzantine',
    'lydian': 'Dreamy / Spacey (Lydian)',
    'lydian_dominant': 'Simpsons / Jazz (Lydian Dom)',
    'mixolydian': 'Bluesy / Rock (Mixolydian)',
    'locrian': 'Dark / Tense (Locrian)',
    'pentatonic_major': 'Major Pentatonic',
    'pentatonic_minor': 'Minor Pentatonic',
    'blues': 'The Blues Scale',
}

PROGRESSION_PRESETS = {
    'pop_rock': {'name': 'I - V - vi - IV (Common Pop)', 'degrees': [1, 5, 6, 4], 'qualities': [None, None, 'm', None]},
    'classic_rock': {'name': 'I - IV - V (Classic Rock)', 'degrees': [1, 4, 5], 'qualities': [None, None, None]},
    'doo_wop': {'name': 'I - vi - ii - V (50s / Jazz)', 'degrees': [1, 6, 2, 5], 'qualities': [None, 'm', 'm', None]},
    'classic_res': {'name': 'I - iii - IV - V (Classic Res)', 'degrees': [1, 3, 4, 5], 'qualities': [None, 'm', None, None]},
    'plagal_exp': {'name': 'I - IV - V - IV - I (Plagal)', 'degrees': [1, 4, 5, 4, 1], 'qualities': [None, None, None, None, None]},
    'cadential': {'name': 'I - IV - I - V (Cadential)', 'degrees': [1, 4, 1, 5], 'qualities': [None, None, None, None]},
    'jazz_subdom': {'name': 'I - IV - ii - V (Jazz Subdom)', 'degrees': [1, 4, 2, 5], 'qualities': [None, None, 'm', None]},
    'storyteller': {'name': 'I - IV - vi - V (Storyteller)', 'degrees': [1, 4, 6, 5], 'qualities': [None, None, 'm', None]},
    'pachelbel': {'name': 'I-V-vi-iii-IV-I-IV-V (Canon)', 'degrees': [1, 5, 6, 3, 4, 1, 4, 5], 'qualities': [None, None, 'm', 'm', None, None, None, None]},
    'jazz_standard': {'name': 'ii - V - I (Jazz Standard)', 'degrees': [2, 5, 1], 'qualities': ['m', '', '']},
    'minor_narrative': {'name': 'i - iv - v - i (Minor Narrative)', 'degrees': [1, 4, 5, 1], 'qualities': ['m', 'm', 'm', 'm']},
    'minor_plagal': {'name': 'i - iv - i (Minor Plagal)', 'degrees': [1, 4, 1], 'qualities': ['m', 'm', 'm']},
    'minor_build': {'name': 'i - iv - v (Minor Build-up)', 'degrees': [1, 4, 5], 'qualities': ['m', 'm', 'm']},
    'dark_uplifting': {'name': 'i - VI - VII (Dark Uplifting)', 'degrees': [1, 6, 7], 'qualities': ['m', '', '']},
    'suspense_loop': {'name': 'i-VII-VI-VII (Suspense Loop)', 'degrees': [1, 7, 6, 7], 'qualities': ['m', '', '', '']},
    'dark_ballad': {'name': 'i - iv - VII (Dark Ballad)', 'degrees': [1, 4, 7], 'qualities': ['m', 'm', '']},
    'minor_epic': {'name': 'i - VI - III - VII (Minor Epic)', 'degrees': [1, 6, 3, 7], 'qualities': ['m', '', '', '']},
    'andalusian': {'name': 'i-bVII-bVI-V (Andalusian)', 'degrees': [1, 7, 6, 5], 'qualities': ['m', '', '', '']},
    'trap': {'name': 'i - bVI - i - v (Trap)', 'degrees': [1, 6, 1, 5], 'qualities': ['m', '', 'm', 'm']},
    'secondary_dom': {'name': 'IV - V - III - vi (Sec. Dom)', 'degrees': [4, 5, 3, 6], 'qualities': [None, None, '', 'm']},
    'res_to_minor': {'name': 'VI - VII - i - i (Res to Minor)', 'degrees': [6, 7, 1, 1], 'qualities': ['', '', 'm', 'm']},
    'minor_res': {'name': 'ii - v - i (Minor Resolution)', 'degrees': [2, 5, 1], 'qualities': ['m', 'm', 'm']},
    'circle': {'name': 'Circle of 5ths (I-V-II-VI-III)', 'degrees': [1, 5, 2, 6, 3], 'qualities': [None, None, 'm', 'm', 'm']},
}

CHORD_TYPES = {
    'major': [0, 4, 7], 'minor': [0, 3, 7], '7': [0, 4, 7, 10],
    'maj7': [0, 4, 7, 11], 'm7': [0, 3, 7, 10], 'dim': [0, 3, 6], 'aug': [0, 4, 8],
    'm7b5': [0, 3, 6, 10]
}

def normalize_note(note: str) -> str:
    note = note.capitalize()
    flat_map = {'Db': 'C#', 'Eb': 'D#', 'Gb': 'F#', 'Ab': 'G#', 'Bb': 'A#'}
    return flat_map.get(note, note)

def get_chord_notes(root: str, chord_type: str = 'major') -> List[str]:
    root = normalize_note(root)
    if root not in NOTES: return []
    root_idx = NOTES.index(root)
    # Handle m7b5 specifically
    if chord_type.lower() == 'm7b5':
        pattern = [0, 3, 6, 10]
    else:
        pattern = CHORD_TYPES.get(chord_type.lower(), CHORD_TYPES['major'])
    return [NOTES[(root_idx + i) % 12] for i in pattern]

def get_notes_in_scale(root: str, scale_type: str) -> List[str]:
    root = normalize_note(root)
    if root not in NOTES: return []
    start_idx = NOTES.index(root)
    pattern = SCALES.get(scale_type.lower(), SCALES['major'])
    return [NOTES[(start_idx + i) % 12] for i in pattern]

def detect_key_and_mood(progression: List[str]) -> Tuple[str, str]:
    if not progression: return 'C', 'major'
    all_used_notes = set()
    for chord in progression:
        root = chord[:2] if len(chord) > 1 and chord[1] in ['#', 'b'] else chord[0]
        suffix = chord[len(root):].lower()
        # Basic mapping for detection
        c_type = 'minor' if 'm' in suffix else 'major'
        if 'dim' in suffix: c_type = 'dim'
        elif 'aug' in suffix: c_type = 'aug'
        all_used_notes.update(get_chord_notes(root, c_type))
        
    best_root, best_scale, highest_score = 'C', 'major', -1
    for root in NOTES:
        for s_type in SCALES.keys():
            scale_notes = set(get_notes_in_scale(root, s_type))
            score = len(all_used_notes.intersection(scale_notes))
            first_root = progression[0][:2] if len(progression[0]) > 1 and progression[0][1] in ['#', 'b'] else progression[0][0]
            if normalize_note(first_root) == root: score += 1.5
            if score > highest_score:
                highest_score = score
                best_root, best_scale = root, s_type
    return best_root, best_scale

def get_chord_from_degree(key_root: str, key_type: str, degree: int, quality_override: Optional[str] = None) -> str:
    """
    Calculates the chord for a degree by strictly following the scale steps.
    No hardcoded fallbacks for 7-note scales.
    """
    key_root = normalize_note(key_root)
    root_idx = NOTES.index(key_root)
    scale_steps = SCALES.get(key_type.lower(), SCALES['major'])
    
    # Calculate Chord Root by walking the scale steps
    if len(scale_steps) == 7:
        # degree 1-7 maps to index 0-6
        d_idx = (degree - 1) % 7
        interval = scale_steps[d_idx]
    else:
        # Fallback for Pentatonic/Blues (using major as a skeleton)
        major_skeleton = [0, 2, 4, 5, 7, 9, 11]
        interval = major_skeleton[(degree - 1) % 7]
        
    chord_root = NOTES[(root_idx + interval) % 12]
    
    # 1. Respect Preset Override (Harmonic Borrowing)
    if quality_override is not None:
        return f"{chord_root}{quality_override}"
        
    # 2. Mathematical Triad Building (1-3-5)
    if len(scale_steps) == 7:
        d_idx = degree - 1
        chord_root_offset = scale_steps[d_idx]
        
        third_idx = (d_idx + 2) % 7
        fifth_idx = (d_idx + 4) % 7
        
        t_off = scale_steps[third_idx]
        if third_idx < d_idx: t_off += 12
        
        f_off = scale_steps[fifth_idx]
        if fifth_idx < d_idx: f_off += 12
        
        t_int = t_off - chord_root_offset
        f_int = f_off - chord_root_offset
        
        suffix = ""
        if t_int == 3: # minor
            suffix = "m" if f_int == 7 else "dim"
        elif t_int == 4: # major
            suffix = "" if f_int == 7 else "aug"
        elif t_int == 2: suffix = "sus2"
        elif t_int == 5: suffix = "sus4"
            
        return f"{chord_root}{suffix}"

    return chord_root

STANDARD_VOICINGS = {
    'C': [None, 3, 2, 0, 1, 0], 'A': [None, 0, 2, 2, 2, 0], 'G': [3, 2, 0, 0, 0, 3],
    'E': [0, 2, 2, 1, 0, 0], 'D': [None, None, 0, 2, 3, 2], 'F': [1, 3, 3, 2, 1, 1],
    'Am': [None, 0, 2, 2, 1, 0], 'Dm': [None, None, 0, 2, 3, 1], 'Em': [0, 2, 2, 0, 0, 0],
    'F#m': [2, 4, 4, 2, 2, 2], 'Bm': [None, 2, 4, 4, 3, 2], 'B7': [None, 2, 1, 2, 0, 2],
    'G#dim': [None, None, 0, 1, 0, 1], 'F#dim': [None, None, 4, 2, 1, None]
}

MOVABLE_VOICINGS = {
    'major': [
        {'name': 'E-Shape', 'frets': [0, 2, 2, 1, 0, 0], 'root_string': 0},
        {'name': 'A-Shape', 'frets': [None, 0, 2, 2, 2, 0], 'root_string': 1},
        {'name': 'D-Shape', 'frets': [None, None, 0, 2, 3, 2], 'root_string': 2},
        {'name': 'G-Shape', 'frets': [3, 2, 0, 0, 0, 3], 'root_string': 0},
        {'name': 'C-Shape', 'frets': [None, 3, 2, 0, 1, 0], 'root_string': 1},
    ],
    'minor': [
        {'name': 'Em-Shape', 'frets': [0, 2, 2, 0, 0, 0], 'root_string': 0},
        {'name': 'Am-Shape', 'frets': [None, 0, 2, 2, 1, 0], 'root_string': 1},
        {'name': 'Dm-Shape', 'frets': [None, None, 0, 2, 3, 1], 'root_string': 2},
        {'name': 'Gm-Shape', 'frets': [3, 1, 0, 0, 0, 3], 'root_string': 0},
        {'name': 'Cm-Shape', 'frets': [None, 3, 1, 0, 1, None], 'root_string': 1},
    ],
    '7': [
        {'name': 'E7-Shape', 'frets': [0, 2, 0, 1, 0, 0], 'root_string': 0},
        {'name': 'A7-Shape', 'frets': [None, 0, 2, 0, 2, 0], 'root_string': 1},
        {'name': 'D7-Shape', 'frets': [None, None, 0, 2, 1, 2], 'root_string': 2},
        {'name': 'B7-Shape', 'frets': [None, 2, 1, 2, 0, 2], 'root_string': 1},
    ],
    'maj7': [
        {'name': 'Emaj7-Shape', 'frets': [0, 2, 1, 1, 0, 0], 'root_string': 0},
        {'name': 'Amaj7-Shape', 'frets': [None, 0, 2, 1, 2, 0], 'root_string': 1},
        {'name': 'Dmaj7-Shape', 'frets': [None, None, 0, 2, 2, 2], 'root_string': 2},
        {'name': 'Cmaj7-Shape', 'frets': [None, 3, 2, 0, 0, 0], 'root_string': 1},
    ],
    'm7': [
        {'name': 'Em7-Shape', 'frets': [0, 2, 0, 0, 0, 0], 'root_string': 0},
        {'name': 'Am7-Shape', 'frets': [None, 0, 2, 0, 1, 0], 'root_string': 1},
        {'name': 'Dm7-Shape', 'frets': [None, None, 0, 2, 1, 1], 'root_string': 2},
    ]
}

def get_standard_voicing(name: str):
 return STANDARD_VOICINGS.get(name)
STRINGS = ['E', 'A', 'D', 'G', 'B', 'E']

def get_nashville_number(key_root: str, key_type: str, chord_name: str) -> str:
    """
    Calculates a "Theory Correct" Roman Numeral for any chord in any scale.
    Handles accidentals (bII, #IV) and casing (I vs i) dynamically.
    """
    key_root = normalize_note(key_root)
    root_idx = NOTES.index(key_root)
    
    # 1. Parse the incoming chord
    c_root = normalize_note(chord_name[:2] if len(chord_name) > 1 and chord_name[1] in ['#', 'b'] else chord_name[0])
    suffix = chord_name[len(c_root):].lower()
    
    # 2. Calculate interval relative to key root (0-11)
    c_idx = NOTES.index(c_root)
    interval = (c_idx - root_idx) % 12
    
    # 3. Map interval to Degree + Accidental relative to MAJOR
    # (The standard benchmark for Roman Numeral analysis)
    major_map = {
        0: ("", "I"),   1: ("b", "II"), 2: ("", "II"),  3: ("b", "III"),
        4: ("", "III"), 5: ("", "IV"),  6: ("#", "IV"), 7: ("", "V"),
        8: ("b", "VI"), 9: ("", "VI"),  10: ("b", "VII"), 11: ("", "VII")
    }
    
    acc, roman = major_map.get(interval, ("", "?"))
    
    # 4. Determine Casing based on Chord Quality
    is_minor = 'm' in suffix and 'maj' not in suffix
    is_dim = 'dim' in suffix or 'o' in suffix
    is_aug = 'aug' in suffix or '+' in suffix
    
    final_roman = roman.lower() if is_minor or is_dim else roman
    
    # 5. Add quality markers
    quality = ""
    if is_dim: quality = "dim"
    elif is_aug: quality = "+"
    elif '7' in suffix: quality = "7"
    elif 'sus' in suffix: quality = suffix # keep sus2/sus4 literal
    
    return f"{acc}{final_roman}{quality}"

def get_note_at_fret(open_note: str, fret: int) -> str:
    return NOTES[(NOTES.index(open_note.upper()) + fret) % 12]
