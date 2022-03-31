import svgwrite

def create_svg(filename, width, height, border_width):
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
    dwg = create_svg('test.svg', 100, 100, 10)
    dwg.save()

if __name__ == "__main__":
    main()