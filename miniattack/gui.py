import math
import matplotlib
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import PySimpleGUI as sg
from os import path
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

matplotlib.use('TkAgg')


def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


def gui(data, itfs=[]):
    if len(itfs) == 0 or len(itfs) >= 8:
        cols = 4
        rowspan = 5
    else:
        cols = 1
        rowspan = 2
    if len(itfs) == 0:
        rows = math.ceil(len(data) / cols) + rowspan
    else:
        rows = math.ceil(len(itfs) / cols) + rowspan
    index = cols * rowspan

    plt.figure(1)
    print(itfs)

    # Show topology image
    imp = path.join(path.dirname(__file__), '..', 'docs', 'topo.jpg')
    imp = path.abspath(imp)
    img = mpimg.imread(imp)
    plt.subplot2grid((rows, cols), (0, 0), rowspan=rowspan, colspan=cols)
    plt.imshow(img)
    plt.axis('off')

    i = index + 1
    for k in sorted(data):
        if len(itfs) > 0 and k not in itfs:
            continue
        plt.subplot(rows, cols, i)
        y = data[k]
        x = [str(t) for t in range(len(y))]
        plt.plot(x, y)
        plt.title(k)
        plt.ylabel('bits/s')
        plt.xticks([])
        i += 1

    fig = plt.gcf()
    fig.set_size_inches(13, 20)
    fig.tight_layout()

    layout = [
        [sg.Column([[sg.Canvas(key='-C1-')]], key='-COL1-', scrollable=True)],
    ]

    window = sg.Window(
        'Mininet Attack Test',
        layout, finalize=True, resizable=True, element_justification='center', font='Helvetica 18', keep_on_top=True, size=(800, 600)
    )

    draw_figure(window['-C1-'].TKCanvas, fig)
    window['-COL1-'].expand(True, True)

    event, values = window.read()
    window.close()
