COCO_CLASSES = {

    0: "person",

    1: "bicycle",

    2: "car",

    3: "motorcycle",

    5: "bus",

    7: "truck"
}


FLOWMIND_VEHICLE_TYPES = {

    "bicycle": "TWO_WHEELER",

    "motorcycle": "TWO_WHEELER",

    "car": "CAR",

    "bus": "HEAVY",

    "truck": "HEAVY"
}


def normalize_vehicle_type(
    detected_class: str
):

    return FLOWMIND_VEHICLE_TYPES.get(
        detected_class,
        "OTHER"
    )