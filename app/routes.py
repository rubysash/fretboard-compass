"""
Routing logic for Fretboard Compass.
Handles all web endpoints and HTMX partials.
"""
from flask import Blueprint, render_template, request, jsonify, current_app, make_response
from .services.workbook_service import WorkbookService
from .services.favorites_service import FavoritesService
from .theory import engine

main_bp = Blueprint('main', __name__)
fav_service = FavoritesService()

@main_bp.route('/')
def index():
    """Main dashboard for the Music Theory Suite."""
    return render_template('index.html', 
                           presets=engine.PROGRESSION_PRESETS,
                           notes=engine.NOTES,
                           scales=engine.SCALES.keys(),
                           scale_meta=engine.SCALE_METADATA,
                           version=current_app.config['VERSION'])

@main_bp.route('/get_preset_chords', methods=['GET'])
def get_preset_chords():
    """Returns the chord names for a given preset and key."""
    preset_key = request.args.get('preset')
    key_root = request.args.get('key_root', 'C')
    key_type = request.args.get('scale_type', 'major')
    
    if not preset_key or preset_key not in engine.PROGRESSION_PRESETS:
        return ""
        
    preset_data = engine.PROGRESSION_PRESETS[preset_key]
    degrees = preset_data['degrees']
    qualities = preset_data.get('qualities', [None] * len(degrees))
    
    chords = []
    for d, q in zip(degrees, qualities):
        chords.append(engine.get_chord_from_degree(key_root, key_type, d, quality_override=q))
        
    return " ".join(chords)

@main_bp.route('/instructions', methods=['GET'])
def instructions():
    """Returns the printable practice guide partial."""
    return render_template('partials/instructions.html')

@main_bp.route('/winners', methods=['GET'])
def winners():
    """Returns the Proven Winners selection partial."""
    return render_template('partials/winners.html')

@main_bp.route('/favorites', methods=['GET'])
def list_favorites():
    """Returns the Saved Favorites selection partial."""
    favorites = fav_service.get_all_favorites()
    return render_template('partials/favorites.html', favorites=favorites)

@main_bp.route('/favorites/form', methods=['GET'])
def favorites_form():
    """Returns the small popup form to save a favorite."""
    key_root = request.args.get('key_root', 'C')
    scale_type = request.args.get('scale_type', 'major')
    return render_template('partials/fav_form.html', 
                           default_name=f"{key_root} {scale_type.capitalize()} Vibe")

@main_bp.route('/favorites/save', methods=['POST'])
def save_favorite():
    """Saves current theory setup to favorites."""
    key_root = request.form.get('key_root')
    scale_type = request.form.get('scale_type')
    progression = request.form.get('progression')
    start_fret = request.form.get('start_fret', 1)
    name = request.form.get('fav_name')
    description = request.form.get('fav_description', '')
    
    if not name:
        name = f"{key_root} {scale_type.capitalize()} Vibe"
    
    fav_service.save_favorite(name, key_root, scale_type, progression, start_fret, description=description)
    return f'<div class="text-green-600 font-bold text-xs animate-pulse">Saved to Favorites!</div>'

@main_bp.route('/favorites/delete/<fav_id>', methods=['DELETE'])
def delete_favorite(fav_id):
    """Deletes a saved favorite."""
    fav_service.delete_favorite(fav_id)
    return list_favorites()

@main_bp.route('/generate', methods=['POST'])
def generate():
    """Endpoint for generating diagrams via HTMX."""
    progression_str = request.form.get('progression', '')
    start_fret = int(request.form.get('start_fret', 1))
    scale_type = request.form.get('scale_type')
    key_root = request.form.get('key_root')
    preset = request.form.get('preset')
    
    # If using manual mode, let the service detect the theory
    if not preset:
        key_root = None
        scale_type = None
    
    # If progression is empty, just show the root chord based on dropdowns
    if not progression_str.strip():
        dropdown_root = request.form.get('key_root', 'C')
        dropdown_scale = request.form.get('scale_type', 'major')
        suffix = 'm' if 'minor' in dropdown_scale or 'phrygian' in dropdown_scale else ''
        progression = [f"{dropdown_root}{suffix}"]
        # Force the service to use these for the "blank" sheet
        key_root, scale_type = dropdown_root, dropdown_scale
    else:
        progression = [c.strip() for c in progression_str.split(' ') if c.strip()]
    
    service = WorkbookService(progression, start_fret, scale_type=scale_type, key_root=key_root)
    workbook = service.generate_workbook()
    
    response = make_response(render_template('partials/workbook.html', workbook=workbook))
    
    # If theory was auto-detected, trigger a client-side update of the dropdowns
    if workbook['inferred_theory']['is_detected']:
        import json
        trigger_data = {
            "updateTheory": {
                "root": workbook['inferred_theory']['root'],
                "mood": list(engine.SCALES.keys())[list(engine.SCALE_METADATA.values()).index(workbook['inferred_theory']['mood'])] if workbook['inferred_theory']['mood'] in engine.SCALE_METADATA.values() else "major"
            }
        }
        # Safely find the scale key from the metadata value
        mood_key = "major"
        for k, v in engine.SCALE_METADATA.items():
            if v == workbook['inferred_theory']['mood']:
                mood_key = k
                break
        
        trigger_data["updateTheory"]["mood"] = mood_key
        response.headers['HX-Trigger'] = json.dumps(trigger_data)

    return response
