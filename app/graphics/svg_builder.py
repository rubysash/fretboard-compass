"""
SVG Graphics Builder.
Pure SVG generation logic for chord and scale diagrams.
Handles Muted (X), Open (O), and Positional (Fretted) notes.
"""
import logging
import svgwrite
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

# Constants for the diagram layout (Centered in 180px width)
STRINGS_X = [40, 60, 80, 100, 120, 140] # 20px gaps, centered
FRETS_Y = [45, 75, 105, 135, 165, 195] 

SCREEN_WIDTH = 180
SCREEN_HEIGHT = 240

class FretboardDiagram:
    """Handles the creation of a single guitar fretboard SVG."""
    
    def __init__(self, title: str, start_fret: int = 1, string_states: Dict[int, str] = None):
        self.title = title
        self.start_fret = start_fret
        self.string_states = string_states or {}
        self.dwg = svgwrite.Drawing(size=(SCREEN_WIDTH, SCREEN_HEIGHT))
        self.notes_to_draw = []

    def add_note(self, string: int, fret: int, label: str = "", color: str = "black", text_color: str = "white"):
        """Queues a note to be drawn."""
        self.notes_to_draw.append({
            "string": string,
            "fret": fret,
            "label": label,
            "color": color,
            "text_color": text_color
        })

    def render(self) -> str:
        """Draws everything and returns the SVG XML string."""
        # 1. Background
        self.dwg.add(self.dwg.rect(insert=(0, 0), size=(SCREEN_WIDTH, SCREEN_HEIGHT), fill='white'))
        
        # 2. Title
        self.dwg.add(self.dwg.text(self.title, insert=(SCREEN_WIDTH/2, 20),
                                  text_anchor="middle", font_size="18px",
                                  font_family="Arial", font_weight="bold", fill="black"))
        
        # Position Label (e.g., "5 fr")
        if self.start_fret > 1:
            self.dwg.add(self.dwg.text(str(self.start_fret), insert=(10, FRETS_Y[0] + 20),
                                      font_size="16px", font_family="Arial", font_weight="bold", fill="black"))
            self.dwg.add(self.dwg.text("fr", insert=(10, FRETS_Y[0] + 35),
                                      font_size="10px", font_family="Arial", fill="gray"))


        # 4. Frets & Nut
        for i, y in enumerate(FRETS_Y):
            is_nut = (self.start_fret == 1 and i == 0)
            stroke_w = 4 if is_nut else 1
            self.dwg.add(self.dwg.line(start=(STRINGS_X[0], y), end=(STRINGS_X[-1], y),
                                      stroke='black', stroke_width=stroke_w))

        # 5. Strings
        for x in STRINGS_X:
            self.dwg.add(self.dwg.line(start=(x, FRETS_Y[0]), end=(x, FRETS_Y[-1]),
                                      stroke='black', stroke_width=1))

        # 6. Header Status (X, O, or Skip)
        for s_idx in range(6):
            state = self.string_states.get(s_idx)
            x = STRINGS_X[s_idx]
            y = FRETS_Y[0] - 8
            if state == 'X':
                self.dwg.add(self.dwg.text("X", insert=(x, y), text_anchor="middle",
                                          font_size="14px", font_family="Arial", font_weight="bold"))
            elif state == 'O':
                self.dwg.add(self.dwg.circle(center=(x, y - 4), r=5, 
                                            fill='white', stroke='black', stroke_width=1.5))

        # 7. Draw Notes
        for note in self.notes_to_draw:
            x = STRINGS_X[note['string']]
            rel_fret_idx = note['fret'] - self.start_fret
            if rel_fret_idx >= 0 and rel_fret_idx < (len(FRETS_Y) - 1):
                y = FRETS_Y[rel_fret_idx] + (FRETS_Y[rel_fret_idx+1] - FRETS_Y[rel_fret_idx]) / 2
                self.dwg.add(self.dwg.circle(center=(x, y), r=8, 
                                            fill=note['color'], stroke='black', stroke_width=1))
                if note['label']:
                    self.dwg.add(self.dwg.text(note['label'], insert=(x, y + 4),
                                              text_anchor="middle", font_size="10px",
                                              font_family="Arial", font_weight="bold", fill=note['text_color']))

        return self.dwg.tostring()

# Constants for Horizontal Full-Neck (Wide for Landscape)
H_STRINGS_Y = [140, 120, 100, 80, 60, 40] # Low E at 140 (Bottom), High E at 40 (Top)
H_FRETS_X = [50, 125, 200, 275, 350, 425, 500, 575, 650, 725, 800, 875, 950]
H_WIDTH = 1000
H_HEIGHT = 250 # Increased to ensure numbers are NOT clipped

class FullNeckDiagram:
    """Handles 12-fret horizontal neck rendering (Full Width)."""
    def __init__(self, title: str):
        self.title = title
        self.dwg = svgwrite.Drawing(size=(H_WIDTH, H_HEIGHT))
        self._setup_neck()

    def _setup_neck(self):
        # Background
        self.dwg.add(self.dwg.rect(insert=(0, 0), size=(H_WIDTH, H_HEIGHT), fill='white'))
        
        # Title
        self.dwg.add(self.dwg.text(self.title, insert=(H_WIDTH/2, 25), 
                                  text_anchor="middle", font_size="22px", font_weight="bold", font_family="Arial"))
        
        # Strings
        for y in H_STRINGS_Y:
            self.dwg.add(self.dwg.line(start=(H_FRETS_X[0], y), end=(H_FRETS_X[-1], y), stroke='#444444', stroke_width=1))
        
        # Frets & Numbering
        for i, x in enumerate(H_FRETS_X):
            is_nut = (i == 0)
            stroke_w = 6 if is_nut else 2
            # Draw vertical fret line
            self.dwg.add(self.dwg.line(start=(x, H_STRINGS_Y[-1]), end=(x, H_STRINGS_Y[0]), 
                                      stroke='black', stroke_width=stroke_w))
            
            # Fret Numbering (Centered under the space, below the strings)
            if i > 0:
                fret_mid_x = H_FRETS_X[i-1] + (H_FRETS_X[i] - H_FRETS_X[i-1]) / 2
                # Y position 185 is well below the bottom string (Y=140)
                self.dwg.add(self.dwg.text(str(i), insert=(fret_mid_x, 190), 
                                          text_anchor="middle", font_size="18px", fill="black", font_weight="bold", font_family="Arial"))

        # Fret Markers (High Contrast Gray)
        marker_y = (H_STRINGS_Y[2] + H_STRINGS_Y[3]) / 2
        for f in [3, 5, 7, 9]:
            x = H_FRETS_X[f-1] + (H_FRETS_X[f] - H_FRETS_X[f-1])/2
            self.dwg.add(self.dwg.circle(center=(x, marker_y), r=8, fill='#BBBBBB', stroke='#999999', stroke_width=1))
        
        # 12th Fret Double Dots
        x12 = H_FRETS_X[11] + (H_FRETS_X[12] - H_FRETS_X[11])/2
        self.dwg.add(self.dwg.circle(center=(x12, H_STRINGS_Y[1]+10), r=8, fill='#BBBBBB', stroke='#999999'))
        self.dwg.add(self.dwg.circle(center=(x12, H_STRINGS_Y[4]-10), r=8, fill='#BBBBBB', stroke='#999999'))

    def add_note(self, string: int, fret: int, label: str):
        if fret < 0 or fret > 12: return
        # string 0 is Low E in our STRINGS array
        y = H_STRINGS_Y[string]
        if fret == 0:
            x = H_FRETS_X[0] - 15
            self.dwg.add(self.dwg.circle(center=(x, y), r=6, fill='white', stroke='black', stroke_width=2))
        else:
            x = H_FRETS_X[fret-1] + (H_FRETS_X[fret] - H_FRETS_X[fret-1])/2
            self.dwg.add(self.dwg.circle(center=(x, y), r=12, fill='black'))
            self.dwg.add(self.dwg.text(label, insert=(x, y+4), text_anchor="middle", font_size="11px", fill="white", font_weight="bold", font_family="Arial"))

    def render(self) -> str:
        return self.dwg.tostring()

def generate_full_scale_svg(name: str, notes: List[Dict]) -> str:
    diagram = FullNeckDiagram(f"{name} Full Scale")
    for note in notes:
        diagram.add_note(string=note['string'], fret=note['fret'], label=note['note'])
    return diagram.render()

def generate_scale_svg(name: str, notes: List[Dict], start_fret: int) -> str:
    states = {}
    diagram = FretboardDiagram(name, start_fret)
    for note in notes:
        if note['fret'] == 0:
            states[note['string']] = 'O'
        else:
            diagram.add_note(string=note['string'], fret=note['fret'], label=note['note'], color="black", text_color="white")
    diagram.string_states = states
    return diagram.render()

def generate_chord_svg(name: str, fingerings: List[Dict], start_fret: int, states: Dict[int, str] = None) -> str:
    diagram = FretboardDiagram(name, start_fret, string_states=states)
    for pos in fingerings:
        if pos['fret'] > 0:
            diagram.add_note(string=pos['string'], fret=pos['fret'], label="", color="black", text_color="white")
    return diagram.render()
