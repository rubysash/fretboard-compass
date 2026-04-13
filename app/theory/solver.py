"""
Positional Solver.
Calculates "Minimum Movement" fingerings for progressions.
"""
import logging
from typing import List, Dict, Tuple, Any
from .engine import STRINGS, NOTES, get_note_at_fret, get_standard_voicing

logger = logging.getLogger(__name__)

def find_notes_in_window(target_notes: List[str], start_fret: int, window_size: int = 4) -> List[Dict]:
    """
    Finds all occurrences of target notes within a specific fret window.
    Always includes fret 0 (open strings) as they are always 'available'.
    """
    logger.debug(f"Searching for {target_notes} between frets {start_fret} and {start_fret + window_size}")
    
    results = []
    for string_idx, open_note in enumerate(STRINGS):
        # Always check open string (fret 0)
        open_string_note = get_note_at_fret(open_note, 0)
        if open_string_note in target_notes:
            results.append({"string": string_idx, "fret": 0, "note": open_string_note})

        # Check window
        for fret in range(start_fret, start_fret + window_size + 1):
            if fret == 0: continue
            current_note = get_note_at_fret(open_note, fret)
            if current_note in target_notes:
                results.append({"string": string_idx, "fret": fret, "note": current_note})
                
    return results

def solve_with_standard_voicing(name: str) -> Tuple[List[Dict], Dict[int, str]]:
    """Tries to use a standard voicing from the database."""
    voicelist = get_standard_voicing(name)
    if not voicelist:
        return None, None
    
    fingering = []
    states = {}
    for s_idx, fret in enumerate(voicelist):
        if fret is None:
            states[s_idx] = 'X'
        elif fret == 0 or fret == 'O':
            states[s_idx] = 'O'
        else:
            fingering.append({"string": s_idx, "fret": fret})
    return fingering, states

def get_best_chord_fingering(chord_name: str, chord_notes: List[str], start_fret: int) -> Tuple[List[Dict], Dict[int, str]]:
    """
    Attempts to find a playable chord voicing.
    Returns: (list of positions, dict of string states {index: 'O'|'X'|None})
    """
    # 1. Try standard voicings if in 1st position
    if start_fret == 1:
        fingering, states = solve_with_standard_voicing(chord_name)
        if fingering is not None:
            logger.info(f"Using standard voicing for {chord_name}")
            return fingering, states

    # 2. Solver fallback
    logger.info(f"Solving voicing for {chord_notes} at position {start_fret}")
    all_possible = find_notes_in_window(chord_notes, start_fret)
    
    fingering = []
    states = {}
    lowest_played_string = -1
    for s_idx in range(6):
        options = [p for p in all_possible if p['string'] == s_idx]
        if options:
            options.sort(key=lambda x: (x['fret'] != 0, x['fret']))
            best = options[0]
            if best['fret'] == 0:
                states[s_idx] = 'O'
            else:
                fingering.append(best)
            if lowest_played_string == -1: lowest_played_string = s_idx
        else:
            states[s_idx] = 'SKIP'

    # Refine states
    played_indices = [p['string'] for p in fingering] + [s for s, v in states.items() if v == 'O']
    highest_played_string = max(played_indices, default=0)

    final_states = {}
    for s_idx in range(6):
        if s_idx in states and states[s_idx] == 'O':
            final_states[s_idx] = 'O'
        elif any(p['string'] == s_idx for p in fingering):
            continue
        else:
            if lowest_played_string != -1 and s_idx > lowest_played_string and s_idx < highest_played_string:
                final_states[s_idx] = 'X'
            elif lowest_played_string != -1 and s_idx < lowest_played_string:
                final_states[s_idx] = None
            else:
                final_states[s_idx] = 'X'
            
    return fingering, final_states
