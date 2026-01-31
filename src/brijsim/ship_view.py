from nicegui import ui

from brijsim.ship.ship import Ship


def ship_view(ship: Ship):
    SVG_WIDTH = 800
    SVG_HEIGHT = 400
    SVG_SCALE = 20.0
    tx = CoordTransform(
        (SVG_WIDTH, SVG_HEIGHT),
        (SVG_WIDTH / 2, SVG_HEIGHT / 2),
        SVG_SCALE,
    )

    content = ""

    for room in ship.rooms:
        ul_x, ul_y = tx(
            (
                room.position.x - room.shape.size.x / 2,
                room.position.y + room.shape.size.y / 2,
            )
        )
        ws, hs = room.shape.size.x * SVG_SCALE, room.shape.size.y * SVG_SCALE
        content += f'<rect x={ul_x} y={ul_y} width={ws} height={hs} fill="#001030" stroke="#0060F0" stroke-width="1" />'

        text_x, text_y = tx((room.global_position.x, room.global_position.y))
        content += f'<text x="{text_x}" y="{text_y}" text="Test" fill="white" text-anchor="middle" dominant-baseline="middle">{room.name}</text>'

        for device in room.devices:
            cx, cy = tx(
                (
                    room.global_position.x + device.global_position.x,
                    room.global_position.y + device.global_position.y,
                )
            )
            content += (
                f'<circle cx="{cx}" cy="{cy}" r=10 stroke="#0060F0" stroke-width="1" />'
            )

    for device in ship.devices:
        cx, cy = tx((device.global_position.x, device.global_position.y))
        content += (
            f'<circle cx="{cx}" cy="{cy}" r=10 stroke="#0060F0" stroke-width="1" />'
        )

    ui.interactive_image(
        size=(SVG_WIDTH, SVG_HEIGHT), content=content, sanitize=False
    ).classes("w-200 bg-black")


class CoordTransform:
    def __init__(
        self,
        svg_size: tuple[float, float],
        world_origin: tuple[float, float],
        world_scale: float,
    ):
        self.svg_size = svg_size
        self.world_origin = world_origin
        self.world_scale = world_scale

    def __call__(self, coord: tuple[float, float]) -> tuple[float, float]:
        tx_coords = (
            coord[0] * self.world_scale + self.world_origin[0],
            self.svg_size[1] - (coord[1] * self.world_scale + self.world_origin[1]),
        )
        return tx_coords
