import svgwrite
import random

from shapely.geometry import Point, LineString

THRESHHOLD_DISTANCE = 15

def generate_paths(width, height, point_count):
    """
    Generate a list of paths with coverage scaling with quantity.
    """
    # Generate border paths for intersections
    paths = [
        LineString([(0,0), (width,0)]),
        LineString([(0,0), (0,height)]),
        LineString([(width,0), (width,height)]),
        LineString([(0,height), (width,height)])
    ]

    for _ in range(point_count):
        x = random.randint(THRESHHOLD_DISTANCE, width-THRESHHOLD_DISTANCE)
        y = random.randint(THRESHHOLD_DISTANCE, height-THRESHHOLD_DISTANCE)
        start = Point(x, y)
        print('Creating lines radiating from {}, {}'.format(start.x, start.y))

        for _ in range(random.randint(2,4)):
            end = None
            attempts = 0
            while attempts < 10:
                attempts += 1
                end = create_collision(start, paths)
                if end is not None:
                    candidate_path = LineString([start, end])
                    if candidate_path.length > 2*THRESHHOLD_DISTANCE:
                        print('Path created after {} attempts'.format(attempts))
                        attempts += 10
                        paths.append(candidate_path)
                        continue

    return paths

def create_collision(start, paths):
    """
    create a collision with a path.
    """
    nearest_collision = None
    nearest_distance = None

    direction_vec = Point(random.uniform(-10000, 10000), random.uniform(-10000, 10000))
    print('\tDirection vector: {}'.format(direction_vec))

    pointy = LineString([start, Point(start.x + direction_vec.x, start.y + direction_vec.y)])
    for path in paths:
        if start.distance(path) < 1:
            continue

        if pointy.intersects(path):
            intersection_point = pointy.intersection(path)
            distance = start.distance(intersection_point)

            if distance < THRESHHOLD_DISTANCE:
                return None

            print('\tCollision with path {} at {}'.format(path, intersection_point))
            if nearest_collision is None:
                nearest_collision = intersection_point
                nearest_distance = distance
            elif distance < nearest_distance:
                print('\t\tNew nearest collision at {}'.format(intersection_point))
                nearest_collision = intersection_point
                nearest_distance = distance
            print('\tNearest collision: {}'.format(intersection_point))

    return nearest_collision


def create_svg(filename, width, height, border_width):
    """
    Create an SVG file with the given properties and border width.
    """
    w = '{}mm'.format(width)
    h = '{}mm'.format(height)
    bw = '{}mm'.format(border_width)
    hw = '{}mm'.format(border_width / 2)
    
    rect_insert = (hw, hw)
    border_size = ('{}mm'.format(width - border_width), '{}mm'.format(height - border_width))

    dwg = svgwrite.Drawing(filename, size=(w, h))
    dwg.add(dwg.rect(
        insert=rect_insert,
        size=border_size,
        fill='none',
        stroke_width=bw,
        stroke='black'
        ))
    return dwg

def main():
    print('Creating test.svg...')
    width = 343
    height = 398
    border_width = 10
    interior_line_width = 5
    dwg = create_svg('test.svg', width, height, border_width)

    for path in generate_paths(width-border_width, height-border_width, 25):
        # print('Adding path {}'.format(path))
        start = ('{}mm'.format(path.coords[0][0]+border_width/2), '{}mm'.format(path.coords[0][1]+border_width/2))
        end = ('{}mm'.format(path.coords[1][0]+border_width/2), '{}mm'.format(path.coords[1][1]+border_width/2))
        stroke_width = '{}mm'.format(interior_line_width)

        dwg.add(dwg.line(start, end, stroke_width=stroke_width, stroke='black'))

    dwg.save()

if __name__ == "__main__":
    main()