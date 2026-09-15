from dataclasses import dataclass


@dataclass
class Lane:

    lane_id: str

    polygon: list

    direction: str

    speed_limit: float = 50.0

    stop_line: list = None

    counting_line: list = None


DEFAULT_LANES = [

    Lane(
        lane_id="north",
        polygon=[
            (0, 250),
            (320, 220),
            (320, 720),
            (0, 720)
        ],
        direction="south",
        speed_limit=50,
        stop_line=[
            (30, 300),
            (290, 280)
        ],
        counting_line=[
            (20, 340),
            (300, 320)
        ]
    ),

    Lane(
        lane_id="east",
        polygon=[
            (320, 220),
            (650, 180),
            (650, 720),
            (320, 720)
        ],
        direction="west",
        speed_limit=50,
        stop_line=[
            (350, 280),
            (620, 250)
        ],
        counting_line=[
            (350, 330),
            (620, 300)
        ]
    ),

    Lane(
        lane_id="south",
        polygon=[
            (650, 180),
            (960, 220),
            (960, 720),
            (650, 720)
        ],
        direction="north",
        speed_limit=50,
        stop_line=[
            (680, 250),
            (940, 280)
        ],
        counting_line=[
            (680, 300),
            (940, 330)
        ]
    ),

    Lane(
        lane_id="west",
        polygon=[
            (960, 220),
            (1280, 250),
            (1280, 720),
            (960, 720)
        ],
        direction="east",
        speed_limit=50,
        stop_line=[
            (990, 280),
            (1250, 300)
        ],
        counting_line=[
            (980, 320),
            (1260, 340)
        ]
    )
]