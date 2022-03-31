import svgwrite

filename = 'test.svg'
weird_blue = svgwrite.rgb(10, 10, 16, '%')

dwg = svgwrite.Drawing(filename, size=('100mm', '100mm'))
dwg.add(dwg.line(('0mm', '0mm'), ('50mm', '100mm'), stroke_width='10mm', stroke=weird_blue))
dwg.add(dwg.line(('100mm', '0mm'), ('50mm', '100mm'), stroke_width='10mm', stroke=weird_blue))
dwg.add(dwg.text('Test', insert=('45mm', '50mm'), fill='red'))
dwg.save()
