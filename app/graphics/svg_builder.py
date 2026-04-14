"""
SVG Graphics Builder.
Pure SVG generation logic for chord and scale diagrams.
Handles Muted (X), Open (O), and Positional (Fretted) notes.
"""
import logging
import svgwrite
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

# Constants for Chord Diagrams (Slightly smaller for Portrait fitting)
STRINGS_X = [37.5, 52.5, 67.5, 82.5, 97.5, 112.5] # Perfectly centered (37.5px padding)
FRETS_Y = [40, 65, 90, 115, 140, 165] 

SCREEN_WIDTH = 150 # Reduced from 180
SCREEN_HEIGHT = 200 # Reduced from 240

class FretboardDiagram:
    """Handles the creation of a single guitar fretboard SVG."""
    
    def __init__(self, title: str, start_fret: int = 1, string_states: Dict[int, str] = None):
        self.title = title
        self.start_fret = start_fret
        self.string_states = string_states or {}
        self.dwg = svgwrite.Drawing(size=(SCREEN_WIDTH, SCREEN_HEIGHT))
        self.notes_to_draw = []

    def add_note(self, string: int, fret: int, label: str = "", color: str = "black", text_color: str = "white"):
        self.notes_to_draw.append({
            "string": string, "fret": fret, "label": label, "color": color, "text_color": text_color
        })

    def render(self) -> str:
        # 1. Background
        self.dwg.add(self.dwg.rect(insert=(0, 0), size=(SCREEN_WIDTH, SCREEN_HEIGHT), fill='white'))
        
        # 2. Title (The only Chord Name we need)
        self.dwg.add(self.dwg.text(self.title, insert=(SCREEN_WIDTH/2, 22),
                                  text_anchor="middle", font_size="18px",
                                  font_family="Arial", font_weight="bold", fill="black"))
        
        # 3. Position Label
        if self.start_fret > 1:
            self.dwg.add(self.dwg.text(f"{self.start_fret}fr", insert=(5, FRETS_Y[0] + 15),
                                      font_size="12px", font_family="Arial", font_weight="bold", fill="black"))

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

        # 6. Status (X, O)
        for s_idx in range(6):
            state = self.string_states.get(s_idx)
            x = STRINGS_X[s_idx]
            y = FRETS_Y[0] - 6
            if state == 'X':
                self.dwg.add(self.dwg.text("X", insert=(x, y), text_anchor="middle",
                                          font_size="12px", font_family="Arial", font_weight="bold"))
            elif state == 'O':
                self.dwg.add(self.dwg.circle(center=(x, y - 3), r=4, 
                                            fill='white', stroke='black', stroke_width=1))

        # 7. Draw Notes
        for note in self.notes_to_draw:
            x = STRINGS_X[note['string']]
            rel_fret_idx = note['fret'] - self.start_fret
            if rel_fret_idx >= 0 and rel_fret_idx < (len(FRETS_Y) - 1):
                y = FRETS_Y[rel_fret_idx] + (FRETS_Y[rel_fret_idx+1] - FRETS_Y[rel_fret_idx]) / 2
                self.dwg.add(self.dwg.circle(center=(x, y), r=7, fill=note['color']))
                if note['label']:
                    self.dwg.add(self.dwg.text(note['label'], insert=(x, y + 3),
                                              text_anchor="middle", font_size="9px",
                                              font_family="Arial", font_weight="bold", fill=note['text_color']))
        return self.dwg.tostring()

# Constants for Horizontal Full-Neck (Optimized for Portrait Width ~750px)
H_STRINGS_Y = [130, 115, 100, 85, 70, 55] # Compacted
H_FRETS_X = [40, 95, 150, 205, 260, 315, 370, 425, 480, 535, 590, 645, 700]
H_WIDTH = 750
H_HEIGHT = 200

class FullNeckDiagram:
    """Handles 12-fret horizontal neck rendering (Portrait Width)."""
    def __init__(self, title: str):
        self.title = title
        self.dwg = svgwrite.Drawing(size=(H_WIDTH, H_HEIGHT))
        self._setup_neck()

    def _setup_neck(self):
        self.dwg.add(self.dwg.rect(insert=(0, 0), size=(H_WIDTH, H_HEIGHT), fill='white'))
        self.dwg.add(self.dwg.text(self.title, insert=(H_WIDTH/2, 25), 
                                  text_anchor="middle", font_size="18px", font_weight="bold", font_family="Arial"))
        for y in H_STRINGS_Y:
            self.dwg.add(self.dwg.line(start=(H_FRETS_X[0], y), end=(H_FRETS_X[-1], y), stroke='#666', stroke_width=1))
        
        for i, x in enumerate(H_FRETS_X):
            is_nut = (i == 0)
            stroke_w = 5 if is_nut else 1.5
            self.dwg.add(self.dwg.line(start=(x, H_STRINGS_Y[-1]), end=(x, H_STRINGS_Y[0]), stroke='black', stroke_width=stroke_w))
            if i > 0:
                fret_mid_x = H_FRETS_X[i-1] + (H_FRETS_X[i] - H_FRETS_X[i-1]) / 2
                self.dwg.add(self.dwg.text(str(i), insert=(fret_mid_x, 165), 
                                          text_anchor="middle", font_size="14px", fill="#444", font_family="Arial"))

    def add_note(self, string: int, fret: int, label: str):
        if fret < 0 or fret > 12: return
        y = H_STRINGS_Y[string]
        if fret == 0:
            x = H_FRETS_X[0] - 15
            self.dwg.add(self.dwg.circle(center=(x, y), r=8, fill='white', stroke='black', stroke_width=1.5))
            self.dwg.add(self.dwg.text(label, insert=(x, y+3), text_anchor="middle", font_size="8px", fill="black", font_weight="bold"))
        else:
            x = H_FRETS_X[fret-1] + (H_FRETS_X[fret] - H_FRETS_X[fret-1])/2
            self.dwg.add(self.dwg.circle(center=(x, y), r=10, fill='black'))
            self.dwg.add(self.dwg.text(label, insert=(x, y+3), text_anchor="middle", font_size="9px", fill="white", font_weight="bold"))

    def render(self) -> str: return self.dwg.tostring()

def generate_full_scale_svg(name: str, notes: List[Dict]) -> str:
    diagram = FullNeckDiagram(f"{name} Scale")
    for note in notes:
        diagram.add_note(string=note['string'], fret=note['fret'], label=note['note'])
    return diagram.render()

def generate_chord_svg(name: str, fingerings: List[Dict], start_fret: int, states: Dict[int, str] = None) -> str:
    diagram = FretboardDiagram(name, start_fret, string_states=states)
    for pos in fingerings:
        if pos['fret'] > 0:
            diagram.add_note(string=pos['string'], fret=pos['fret'], label="", color="black", text_color="white")
    return diagram.render()
