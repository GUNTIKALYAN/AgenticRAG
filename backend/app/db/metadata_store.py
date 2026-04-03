import json
import os


class MetadataStore:

    # def __init__(self, path):
    #     self.path = path

    #     os.makedirs(os.path.dirname(path), exist_ok=True)

    #     if os.path.exists(path):
    #         with open(path, "r", encoding="utf-8") as f:
    #             try:
    #                 self.data = json.load(f)
    #             except:
    #                 self.data = []
    #     else:
    #         self.data = []
    def __init__(self, path):
        self.path = path
        self.data = []  # 🔥 always fresh

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
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2)