import json
import os


class MetadataStore:

    def __init__(self, path):
        self.path = path
        self.data = []  

        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    self.data = json.load(f)
            except:
                self.data = []

    def add_batch(self, metadata_list):
        self.data.extend(metadata_list)

    def get(self, idx):
        if 0 <= idx < len(self.data):
            return self.data[idx]
        return None

    def save(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)  # ✅ ADD THIS

        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2)