import ezdxf
import random
import math

ROOM_TYPES = ["Living Room", "Kitchen", "Bedroom", "Bedroom", "Bathroom", "Toilet"]

def generate_room_sizes(n, min_area, max_area, total_area, include_hall=True):
    hallway_area = 8 if include_hall else 0
    total_for_rooms = total_area - hallway_area
    sizes = []
    remaining = total_for_rooms
    for i in range(n):
        if i == n - 1:
            area = remaining
        else:
            max_allowed = min(max_area, remaining - (n - i - 1) * min_area)
            area = random.uniform(min_area, max_allowed)
        width = round(math.sqrt(area), 2)
        height = round(area / width, 2)
        sizes.append((width, height))
        remaining -= area
    return sizes, hallway_area

def arrange_rooms_with_hallway(sizes, hallway_area):
    hall_width = 1.5
    total_width = 0
    max_room_height = 0
    rooms = []

    # Compute max room width to help with layout
    for w, h in sizes:
        total_width += w + 1
        max_room_height = max(max_room_height, h)

    x_cursor = 0
    y_base = 0

    for i, (w, h) in enumerate(sizes):
        room_type = ROOM_TYPES[i % len(ROOM_TYPES)]
        # Alternate placement above and below hallway
        if i % 2 == 0:
            y = y_base + hall_width + 1  # top
        else:
            y = y_base - h - 1           # bottom

        rooms.append({
            'name': room_type,
            'x': x_cursor,
            'y': y,
            'w': w,
            'h': h
        })
        x_cursor += w + 1

    hallway = {
        'x': 0,
        'y': y_base,
        'w': x_cursor,
        'h': hall_width,
        'name': 'Hallway'
    }

    return rooms, hallway

def draw_floor_plan_dxf(rooms, hallway, filename="floor_plan_with_hall.dxf"):
    doc = ezdxf.new()
    msp = doc.modelspace()

    doc.layers.new(name='WALLS', dxfattribs={'color': 7})
    doc.layers.new(name='DOORS', dxfattribs={'color': 2})
    doc.layers.new(name='WINDOWS', dxfattribs={'color': 4})
    doc.layers.new(name='TEXT', dxfattribs={'color': 3})

    # Draw hallway
    x, y, w, h = hallway['x'], hallway['y'], hallway['w'], hallway['h']
    msp.add_lwpolyline([(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)],
                       dxfattribs={'layer': 'WALLS', 'closed': True})
    msp.add_text(hallway['name'], dxfattribs={'layer': 'TEXT', 'height': 0.4})\
        .set_pos((x + w / 2, y + h / 2), align='CENTER')

    # Draw rooms
    for room in rooms:
        x, y, w, h = room['x'], room['y'], room['w'], room['h']

        msp.add_lwpolyline([
            (x, y), (x + w, y), (x + w, y + h),
            (x, y + h), (x, y)
        ], dxfattribs={'layer': 'WALLS', 'closed': True})

        # Door connecting to hallway (on side near corridor)
        if y > hallway['y']:  # top of hallway
            door_y = hallway['y'] + hallway['h']
        else:  # bottom of hallway
            door_y = hallway['y']

        door_width = min(1.0, w * 0.5)
        door_x = x + (w - door_width) / 2
        msp.add_line((door_x, door_y), (door_x + door_width, door_y), dxfattribs={'layer': 'DOORS'})

        # Window on opposite wall
        if y > hallway['y']:
            win_y = y + h
        else:
            win_y = y
        win_width = min(1.2, w * 0.5)
        win_x = x + (w - win_width) / 2
        msp.add_line((win_x, win_y), (win_x + win_width, win_y), dxfattribs={'layer': 'WINDOWS'})

        # Label
        msp.add_text(room['name'], dxfattribs={'layer': 'TEXT', 'height': 0.4})\
            .set_pos((x + w / 2, y + h / 2), align='CENTER')

    doc.saveas(filename)
    print(f"✅ Floor plan with hallway saved as: {filename}")

def main():
    n_rooms = 6
    min_area = 10
    max_area = 20
    total_area = 90

    sizes, hall_area = generate_room_sizes(n_rooms, min_area, max_area, total_area)
    rooms, hallway = arrange_rooms_with_hallway(sizes, hall_area)
    draw_floor_plan_dxf(rooms, hallway, "floor_plan_with_hall.dxf")

if __name__ == "__main__":
    main()
