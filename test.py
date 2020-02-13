def test_call():
    print("Test success")

def master_call():
    print ("It's master")

def new_test_call():
    print ("On developer branch.")

def branch_changer():
    print ("yo")
    
from bokeh.models import Slider, CustomJS
from bokeh.layouts import row, column
from bokeh.plotting import Figure, output_notebook, show, ColumnDataSource
from bokeh.models.widgets import Button, TextInput

output_notebook()

import numpy as np
from scipy.optimize import root
from sympy.plotting import plot_implicit
import sympy as sp

def iv_data(V_oc=45.9, I_sc = 9.25, R_s=0.32, R_sh=20044, N=0.1):
#     R_s = 0.32
#     R_sh = 20044
#     V_oc = 45.9
    n = 0.9
    N_Cell = 72
    V_t = 25.7e-3
    I_sat = (I_sc - (V_oc - I_sc*R_s)/R_sh)*(np.exp(-V_oc/(n*N_Cell*V_t)));
    I_ph = I_sat * np.exp(V_oc / (n*N_Cell*V_t)) + (V_oc/R_sh);

##print ("V_oc is {}, \n I_sat is {}, \n I_ph is {}".format(V_oc, I_sat, I_ph))
########## 5 parameters are here : n, R_s, R_sh, I_sat, I_ph #############

    I=sp.Symbol('I')
    V=sp.Symbol('V')

    expr = (I-I_ph+I_sat*(sp.exp((V+I*R_s)/(n*N_Cell*V_t))-1)+((V+I*R_s)/R_sh))
    p=plot_implicit(expr, (V,0,50), (I,0,10), show=False)
    data = p[0].get_points()
    data = np.array([(x_int.mid, y_int.mid) for x_int, y_int in data[0]])
    V=[i[0] for i in data]
    I=[i[1] for i in data]
    return dict(x=V,y=I)

def modify_doc(doc):
    
    source = ColumnDataSource(data=iv_data(35, 6, 0.34, 20000, 100))

    plot = Figure(plot_width = 600, plot_height = 600, y_range = (-1, 10), x_range = (0,60))
    plot.xaxis.axis_label = 'Voltage (V)'
    plot.yaxis.axis_label = 'Current (I)'
    plot.scatter('x', 'y', source=source, line_width=3, line_alpha=0.6)
    
    isc_slider = Slider(start = 4, end = 10, value = 6, step = 0.1, title = 'I_sc')
    voc_slider = Slider(start = 10, end = 50, value = 35, step = 1, title = 'V_oc')
    rs_slider = Slider(start = 0.01, end = 5, value = 0.34, step = 0.5, title = 'R_s')
    rsh_slider = Slider(start = 10, end = 1000, value = 100, step = 10, title = 'R_sh')
    n_slider = Slider(start = 25, end = 5000, value = 100, step = 5, title = 'Data Points')
    download_button = Button(label = 'Download data as csv', width = 100)
    
    def get_slider_val():
        return (voc_slider.value ,isc_slider.value, rs_slider.value, rsh_slider.value, n_slider.value)
    
    def update_plot(attrname, old , new):
        V, I, Rs, Rsh, N = get_slider_val()
        source.data = iv_data(V, I, Rs, Rsh, N)
    
    def download():
        print("Not working for now")

    isc_slider.on_change('value', update_plot)
    voc_slider.on_change('value', update_plot)
    rs_slider.on_change('value', update_plot)
    rsh_slider.on_change('value', update_plot)
    n_slider.on_change('value', update_plot)
    download_button.on_click(download)

    
    layout = row(plot, column(isc_slider, voc_slider, rs_slider, rsh_slider, n_slider, download_button),)
    doc.add_root(layout)
show(modify_doc)
