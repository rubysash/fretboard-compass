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

    def __init__(self, progression: List[str], start_fret: int = 1, scale_type: str = None, key_root: str = None):
        self.progression = progression
        self.start_fret = start_fret
        self.scale_type = scale_type
        self.key_root = key_root
        self.workbook_data = {
            "progression": progression,
            "start_fret": start_fret,
            "chords": [],
            "scales": []
        }

    def generate_workbook(self) -> Dict[str, Any]:
        """Runs the full pipeline to generate theory and diagrams."""
        logger.info(f"Generating workbook for {self.progression} at position {self.start_fret}")

        # 1. Determine Key Root
        # Use explicit key_root if provided, otherwise infer from first chord
        if self.key_root:
            key_root = engine.normalize_note(self.key_root)
            _, inferred_type = engine.get_key_from_progression(self.progression)
        else:
            key_root, inferred_type = engine.get_key_from_progression(self.progression)
        
        # Use explicit scale_type if provided, otherwise use inferred
        target_scale_type = self.scale_type if self.scale_type else inferred_type

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
            nashville = engine.get_nashville_number(key_root, inferred_type, chord_name)
            
            # Generate multiple options
            alt_options = solver.get_alternative_fingerings(chord_name, notes, self.start_fret)
            processed_options = []
            for opt in alt_options:
                svg = svg_builder.generate_chord_svg(chord_name, opt['fingering'], opt['fret'], states=opt['states'])
                processed_options.append({
                    "style": opt['style'],
                    "svg": svg
                })
            
            self.workbook_data["chords"].append({
                "name": chord_name,
                "nashville": nashville,
                "options": processed_options
            })

        # 3. Process Full Scale (12 Frets Horizontal)
        scale_notes = engine.get_notes_in_scale(key_root, target_scale_type)
        # Search from 0 to 12 to include Nut notes
        full_scale_positions = solver.find_notes_in_window(scale_notes, start_fret=0, window_size=12)
        
        # Cleaner Scale Name
        clean_scale_name = key_root
        if target_scale_type.lower() == 'minor': 
            clean_scale_name = f"{key_root}m"
        elif target_scale_type.lower() == 'blues':
            clean_scale_name = f"{key_root} Blues"
        elif 'pentatonic' in target_scale_type.lower():
            clean_scale_name = f"{key_root} Pent"
        else:
            clean_scale_name = f"{key_root} {target_scale_type.capitalize()}"

        full_scale_svg = svg_builder.generate_full_scale_svg(clean_scale_name, full_scale_positions)
        
        self.workbook_data["scales"].append({
            "name": clean_scale_name,
            "svg": full_scale_svg
        })

        return self.workbook_data
