import os
import json
import uuid
from pathlib import Path

class FavoritesService:
    def __init__(self, favorites_dir="favorites"):
        self.favorites_dir = Path(favorites_dir)
        if not self.favorites_dir.exists():
            self.favorites_dir.mkdir(parents=True)

    def save_favorite(self, name, key_root, scale_type, progression, start_fret, description=""):
        """Saves a new favorite as a JSON file."""
        fav_id = str(uuid.uuid4())[:8]
        filename = f"{fav_id}.json"
        filepath = self.favorites_dir / filename
        
        data = {
            "id": fav_id,
            "name": name,
            "description": description,
            "key_root": key_root,
            "scale_type": scale_type,
            "progression": progression,
            "start_fret": start_fret
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f)
        
        return data

    def get_all_favorites(self):
        """Returns a list of all saved favorites."""
        favorites = []
        for file in self.favorites_dir.glob("*.json"):
            try:
                with open(file, 'r') as f:
                    favorites.append(json.load(f))
            except Exception:
                continue
        return favorites

    def delete_favorite(self, fav_id):
        """Deletes a favorite by its ID."""
        filepath = self.favorites_dir / f"{fav_id}.json"
        if filepath.exists():
            os.remove(filepath)
            return True
        return False

    def get_favorite(self, fav_id):
        """Retrieves a single favorite."""
        filepath = self.favorites_dir / f"{fav_id}.json"
        if filepath.exists():
            with open(filepath, 'r') as f:
                return json.load(f)
        return None
