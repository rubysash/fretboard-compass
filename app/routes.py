"""
Routing logic for ChordDumper.
Handles all web endpoints and HTMX partials.
"""
from flask import Blueprint, render_template, request, jsonify
from .services.workbook_service import WorkbookService
from .theory import engine

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Main dashboard for the Music Theory Suite."""
    return render_template('index.html', 
                           presets=engine.PROGRESSION_PRESETS,
                           notes=engine.NOTES,
                           scales=engine.SCALES.keys(),
                           scale_meta=engine.SCALE_METADATA)

@main_bp.route('/get_preset_chords', methods=['GET'])
def get_preset_chords():
    """Returns the chord names for a given preset and key."""
    preset_key = request.args.get('preset')
    key_root = request.args.get('key_root', 'C')
    key_type = request.args.get('scale_type', 'major')
    
    if not preset_key or preset_key not in engine.PROGRESSION_PRESETS:
        return ""
        
    degrees = engine.PROGRESSION_PRESETS[preset_key]['degrees']
    chords = [engine.get_chord_from_degree(key_root, key_type, d) for d in degrees]
    return " ".join(chords)

@main_bp.route('/generate', methods=['POST'])
def generate():
    """Endpoint for generating diagrams via HTMX."""
    progression_str = request.form.get('progression', '')
    start_fret = int(request.form.get('start_fret', 1))
    scale_type = request.form.get('scale_type', 'major')
    key_root = request.form.get('key_root', 'C')
    
    # If progression is empty, just show the root chord
    if not progression_str.strip():
        # Infer suffix from scale type
        suffix = 'm' if 'minor' in scale_type or scale_type == 'blues' else ''
        progression = [f"{key_root}{suffix}"]
    else:
        progression = [c.strip() for c in progression_str.split(' ') if c.strip()]
    
    service = WorkbookService(progression, start_fret, scale_type=scale_type, key_root=key_root)
    workbook = service.generate_workbook()
    
    return render_template('partials/workbook.html', workbook=workbook)
