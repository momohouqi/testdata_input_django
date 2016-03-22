from reportlab.platypus import TableStyle, Table, SimpleDocTemplate, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus.paragraph import Paragraph
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.shapes import Drawing
from reportlab.platypus.flowables import Spacer
from reportlab.lib.units import cm


# values will be import
styleSheet = getSampleStyleSheet()
h1_style = styleSheet['Heading1']
h2_style = styleSheet['Heading2']
h2_style.alignment = 1
# h2_style.textColor = colors.lightskyblue
h4_style = styleSheet['Heading4']
h4_style.alignment = 1
h4_style.fontSize = 8
h4_style.fontName = 'Helvetica-Bold'
bt_style = styleSheet['BodyText']


def show_content(content, style_conf):
    return Paragraph(content, style_conf)


def insert_space(length=0.5):
    return Spacer(0, length*cm)


def show_main_table(data, span_list):
    sty_list = [
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.pink),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1.0, colors.black),
            ]
    for start, stop in span_list:
        sty_list.append(('SPAN', (0, start), (0, stop)))
    sty = TableStyle(sty_list)
    t = Table(data,
              # comment the colwidths for auto-size column width
              # colWidths=[36, 36, 36, 36, None, 36, 36, 36, 36, 36],
              rowHeights=None, style=sty)
    return t



def show_conf_table(data, span_list):
    sty_list = [
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.pink),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1.0, colors.black),
            ]
    for start, stop in span_list:
        sty_list.append(('SPAN', (start, 0), (stop, 0)))
    sty = TableStyle(sty_list)
    t = Table(data,
              # comment the colwidths for auto-size column width
              # colWidths=[36, 36, 36, 36, None, 36, 36, 36, 36, 36],
              rowHeights=None, style=sty)
    return t


def show_figure(data, y_max, x_category, legend_category):
    drawing = Drawing(400, 200)
    bc = VerticalBarChart()
    bc.x = 50
    bc.y = 50
    bc.height = 150
    bc.width = 450
    bc.data = data
    bc.strokeColor = colors.black
    bc.valueAxis.valueMin = 0
    bc.valueAxis.valueMax = y_max
    # bc.valueAxis.valueStep = 15
    bc.categoryAxis.labels.boxAnchor = 'ne'
    bc.categoryAxis.labels.dx = len(data[0])
    # bc.categoryAxis.labels.dy = -2
    # bc.categoryAxis.labels.angle = 30
    bc.categoryAxis.categoryNames = x_category
    drawing.add(bc)

    # add legend from here
    swatches = Legend()
    swatches.alignment = 'right'
    swatches.x = 80
    swatches.y = 190
    swatches.deltax = 30
    swatches.dxTextSpace = 10
    swatches.columnMaximum = 1
    color_list = (colors.red, colors.green, colors.blue, colors.pink,
            colors.yellow)
    items = []
    for index, item in enumerate(legend_category):
        items.append((color_list[index], item))
    swatches.colorNamePairs = items
    drawing.add(swatches, 'legend')
    return drawing


def insert_image(image_path, width, height):
    c = Image(image_path, width, height, hAlign='LEFT')
    return c
