

def to_json(obj) -> dict:
    json = {}
    for key, value in obj.__dict__.items():
        if not key.startswith('_'):
            json[key] = value
    return json