import json,os

class BDD:
    def __init__(self, path):
        self.path = path
        self.load()
    def load(self):
        with open(self.path, 'r', encoding='utf-8') as fichier:
            self.local = json.load(fichier)
    def save(self):
        with open(self.path, 'w', encoding='utf-8') as fichier:
            json.dump(self.local, fichier, indent=4)
    def extract(path):
        with open(path, 'r', encoding='utf-8') as fichier:
            return json.load(fichier)
    def dump(path,content):
        with open(path, 'w', encoding='utf-8') as fichier:
            json.dump(content,fichier,indent=4)