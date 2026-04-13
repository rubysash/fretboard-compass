"""
Workbook Orchestrator.
Combines theory, diagrams, and notes into a printable format.
"""
import logging
from typing import List, Dict, Any
from ..theory import engine, solver
from ..graphics import svg_builder

logger = logging.getLogger(__name__)

class WorkbookService:
    """Orchestrates the creation of a full music theory workbook."""

    def __init__(self, progression: List[str], start_fret: int = 1):
        self.progression = progression
        self.start_fret = start_fret
        self.workbook_data = {
            "progression": progression,
            "start_fret": start_fret,
            "chords": [],
            "scales": []
        }

    def generate_workbook(self) -> Dict[str, Any]:
        """Runs the full pipeline to generate theory and diagrams."""
        logger.info(f"Generating workbook for {self.progression} at position {self.start_fret}")

        # 1. Infer Key
        key_root, key_type = engine.get_key_from_progression(self.progression)

        # 2. Process Chords
        for raw_name in self.progression:
            # Ensure proper casing (e.g. em -> Em)
            chord_name = raw_name.capitalize()
            if len(chord_name) > 1 and chord_name[1] in ['#', 'b']:
                root = chord_name[:2]
                chord_type = chord_name[2:]
            else:
                root = chord_name[0]
                chord_type = chord_name[1:]
            
            if chord_type == 'm': chord_type = 'minor'
            if not chord_type: chord_type = 'major'

            # Get notes and Nashville Number
            notes = engine.get_chord_notes(root, chord_type)
            nashville = engine.get_nashville_number(key_root, key_type, chord_name)
            
            fingerings, states = solver.get_best_chord_fingering(chord_name, notes, self.start_fret)
            svg = svg_builder.generate_chord_svg(chord_name, fingerings, self.start_fret, states=states)
            
            self.workbook_data["chords"].append({
                "name": chord_name,
                "nashville": nashville,
                "svg": svg
            })

        # 3. Process Full Scale (12 Frets Horizontal)
        scale_notes = engine.get_notes_in_scale(key_root, key_type)
        full_scale_positions = solver.find_notes_in_window(scale_notes, start_fret=1, window_size=11) # 1-12
        
        # Cleaner Scale Name
        clean_scale_name = key_root
        if key_type.lower() == 'minor': clean_scale_name = f"{key_root}m"

        full_scale_svg = svg_builder.generate_full_scale_svg(clean_scale_name, full_scale_positions)
        
        self.workbook_data["scales"].append({
            "name": clean_scale_name,
            "svg": full_scale_svg
        })

        return self.workbook_data
