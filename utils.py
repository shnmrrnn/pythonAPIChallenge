import json

def load_cakes():
    try:
        with open('cakes.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_cakes(cakes):
    with open('cakes.json', 'w') as file:
        json.dump(cakes, file, indent=4)

def get_next_id(cakes):
    return max(cake['id'] for cake in cakes) + 1 if cakes else 1