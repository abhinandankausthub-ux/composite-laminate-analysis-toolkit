import json
import os

CORE_PATH = "data/core_materials.json"
CUSTOM_PATH = "data/custom_materials.json"


def load_json(path):
    if not os.path.exists(path):
        return {}

    with open(path, "r") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def get_all_materials():
    """
    Merge core and custom materials
    """

    core = load_json(CORE_PATH)
    custom = load_json(CUSTOM_PATH)

    materials = {**core, **custom}

    return materials


def add_custom_material(name, properties):
    """
    Add user defined material
    """

    custom = load_json(CUSTOM_PATH)

    custom[name] = properties

    save_json(CUSTOM_PATH, custom)


def delete_custom_material(name):
    """
    Delete only user materials
    """

    custom = load_json(CUSTOM_PATH)

    if name in custom:
        del custom[name]

    save_json(CUSTOM_PATH, custom)


def is_core_material(name):
    core = load_json(CORE_PATH)
    return name in core
