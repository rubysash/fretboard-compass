"""
Routing logic for ChordDumper.
Handles all web endpoints and HTMX partials.
"""
from flask import Blueprint, render_template, request
from .services.workbook_service import WorkbookService

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Main dashboard for the Music Theory Suite."""
    return render_template('index.html')

@main_bp.route('/generate', methods=['POST'])
def generate():
    """Endpoint for generating diagrams via HTMX."""
    progression_str = request.form.get('progression', 'C Am F G')
    start_fret = int(request.form.get('start_fret', 1))
    
    # Simple split and clean
    progression = [c.strip() for c in progression_str.split(' ') if c.strip()]
    
    service = WorkbookService(progression, start_fret)
    workbook = service.generate_workbook()
    
    return render_template('partials/workbook.html', workbook=workbook)
