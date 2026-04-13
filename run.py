"""
Development Entry Point.
Starts the Flask server in debug mode.
"""
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
