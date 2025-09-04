import yaml

data = {
    'train': r'C:\Users\sungh\OneDrive\바탕 화면\study\20250901\roboflow\train',
    'val': r'C:\Users\sungh\OneDrive\바탕 화면\study\20250901\roboflow\valid',
    'nc': 1,
    'names': ['raccoon']
}

with open(r'C:\Users\sungh\OneDrive\바탕 화면\study\20250901\roboflow\data.yaml', 'w') as f:
    yaml.dump(data, f)

with open(r'C:\Users\sungh\OneDrive\바탕 화면\study\20250901\roboflow\data.yaml', 'r') as f:
    aquarium_yaml = yaml.safe_load(f)
    print(aquarium_yaml)