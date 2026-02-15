import json
import os
from typing import List, Dict, Optional

# Resolve relative to project root (../../subsidy/subsidy.json from app/core/)
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_THIS_DIR, "..", "..", ".."))
SUBSIDY_FILE_PATH = os.path.join(_PROJECT_ROOT, "subsidy", "subsidy.json")

class SubsidyService:
    def __init__(self):
        self.file_path = SUBSIDY_FILE_PATH
        self._load_data()

    def _load_data(self):
        """Loads subsidy data from JSON file."""
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        else:
            self.data = {"schemes": []}

    def get_all_schemes(self) -> List[Dict]:
        """Returns all schemes flattened for easier consumption."""
        all_schemes = []
        for category in self.data.get("schemes", []):
            cat_name = category.get("category")
            for scheme in category.get("schemes", []):
                scheme["category"] = cat_name
                all_schemes.append(scheme)
        return all_schemes

    def get_schemes_by_category(self, category: str) -> List[Dict]:
        """Returns schemes for a specific category."""
        for cat in self.data.get("schemes", []):
            if cat.get("category").lower() == category.lower():
                return cat.get("schemes", [])
        return []

    def search_schemes(self, query: str) -> List[Dict]:
        """Search schemes by name or benefit."""
        query = query.lower()
        results = []
        for scheme in self.get_all_schemes():
            if query in scheme.get("name", "").lower() or query in scheme.get("benefit", "").lower():
                results.append(scheme)
        return results

    def add_scheme(self, category_name: str, scheme_details: Dict):
        """Adds a new scheme to a category."""
        category_found = False
        for cat in self.data.get("schemes", []):
            if cat.get("category").lower() == category_name.lower():
                cat["schemes"].append(scheme_details)
                category_found = True
                break
        
        if not category_found:
            # Create new category if not exists
            new_cat = {
                "category": category_name,
                "schemes": [scheme_details]
            }
            self.data["schemes"].append(new_cat)
            
        self._save_data()

    def _save_data(self):
        """Saves data back to JSON."""
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

subsidy_service = SubsidyService()
