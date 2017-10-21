"""
Convenience wrapper functions for plotting with Bokeh in Jupyter Notebooks.

Requires Bokeh version 0.12.9.

Note: for Python 3.5, to get ipywidgets.interact to work in function hist(),
pip install widgetsnbextension=2.0.0 instead of a later version.
"""
import warnings
import numpy as np
import pandas as pd

from ipywidgets import interact, widgets
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import DatetimeTickFormatter
from bokeh.io import push_notebook, show, output_notebook

output_notebook()


def hist(df=pd.DataFrame(), colname=''):
    """
    Plots a histogram of values in one column of a Pandas DataFrame object.
    Adds interactive slides for number of bins and nth percentile marker.

    Arguments
    ---------
        df:         a Pandas DataFrame object
        colname:    str, one value from df.columns to histogram

    Sample usage in a Jupyter Notebook cell:

        # add path to where bokeh_wrap/ repo is cloned
        import sys; sys.path.append('/abs/path/to/github/dpshenoy')
        import bokeh_wrap as bw

        df = pd.read_table("data.txt")
        bw.hist(df=df, colname=df.columns[0])
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError(
            'Value passed as arg "df" not a Pandas DataFrame object.')
    if colname not in df.columns:
        raise ValueError('Column '+colname+' not in supplied DataFrame.')
    if not np.issubdtype(df[colname].dtype, np.number):
        raise TypeError('Values of df['+colname+'] are not numeric.')

    vals_to_bin = df[colname].values

    init_n_bins = int(np.sqrt(vals_to_bin.shape[0]))
    counts, edges = np.histogram(vals_to_bin, bins=init_n_bins)
    zeros = np.zeros(counts.shape[0])
    q = 50
    ntile = np.percentile(vals_to_bin, q=q)

    p = figure(plot_height=200, plot_width=600, sizing_mode='scale_width')
    h = p.quad(left=edges[:-1], right=edges[1:],
               top=counts, bottom=zeros, fill_alpha=0.8)
    l = p.line(x=[ntile,ntile], y=[0.,1.2*counts.max()], line_dash='dashed',
               line_width=3, line_color='black')

    p.title.text = 'temporary title' # must create before update() called, for proper placement
    p.xaxis.axis_label = 'binned value of column "'+colname+'"'
    p.xaxis.axis_label_text_font_style = 'normal'
    p.xaxis.axis_label_text_font_size = '12pt'
    p.xaxis.major_label_text_font_size = '12pt'

    p.yaxis.axis_label = '# of values in bin'
    p.yaxis.axis_label_text_font_style = 'normal'
    p.yaxis.axis_label_text_font_size = '12pt'
    p.yaxis.major_label_text_font_size = '12pt'

    # plot border padding
    p.min_border_top = 5
    p.min_border_bottom = 40
    p.min_border_left = 50
    p.min_border_right = 50

    def update(n_bins, nth_percentile):
        c, e = np.histogram(vals_to_bin, bins=n_bins)
        z = np.zeros(c.shape[0])
        newbars = {
            'left': e[:-1],
            'right': e[1:],
            'top': c,
            'bottom': z
        }
        h.data_source.data = newbars

        n = np.percentile(vals_to_bin, q=nth_percentile)
        newperc = {
            'x': [n,n],
            'y': [0.,1.2*c.max()]
        }
        l.data_source.data = newperc

        title = 'bin width = '+str(np.around(e[1]-e[0], decimals=2))
        title += ' for number of bins = '+str(n_bins)
        title += '                 '
        title += str(nth_percentile)+'th percentile = '+str(n)

        p.title.text = title
        p.title.align = "left"
        push_notebook()

    show(p, notebook_handle=True)
    n_bins=widgets.IntSlider(min=1, max=2*init_n_bins, step=1, value=10)
    interact(update, n_bins=n_bins, nth_percentile=(0,100))

def timeplot(df=pd.DataFrame(), timecol='', datacol='', plottype='scatter'):
    """
    Plots a time series of values in one column of a Pandas DataFrame object,
    using timestamp values in another column of the same frame.

    Arguments
    ---------
        df:         a Pandas DataFrame object
        timecol:    str, name of column with timestamp values for x-axis
        datacol:    str, name of column with data values for y-axis
        type:       str, either 'scatter' or 'line'

    Sample usage in a Jupyter Notebook cell:

        # add path to where bokeh_wrap/ repo is cloned
        import sys; sys.path.append('/abs/path/to/github/dpshenoy')
        import bokeh_wrap as bw

        df = pd.read_table("data.txt")
        bw.timeplot(df=df, timecol='date', datacol='amt', type='line')
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError(
            'Value passed as  arg "df" not a Pandas DataFrame object.')
    for colname in (timecol, datacol):
        if colname not in df.columns:
            raise ValueError('Column '+colname+' not in supplied DataFrame.')
    if not np.issubdtype(df[timecol].dtype, np.datetime64):
        raise TypeError('Values of df['+timecol+'] are not numpy.datetime64.')
    if not np.issubdtype(df[datacol].dtype, np.number):
        raise TypeError('Values of df['+datacol+'] are not numeric.')
    if plottype not in ('scatter', 'line'):
        raise ValueError('plottype must be "scatter" or "line" only.')

    df.sort_values(by=timecol, inplace=True)
    source = ColumnDataSource(df)

    tools = ['pan,wheel_zoom,box_zoom,save,reset']

    p = figure(tools=tools, plot_width=900, plot_height=400, 
               sizing_mode='scale_width', x_axis_type="datetime")

    if plottype == 'scatter':
        p.circle(x=timecol, y=datacol, source=source, color='blue', alpha=0.5,
                 size=5)
    else:
        p.line(x=timecol, y=datacol, source=source, color='blue', line_width=2)

    p.xaxis.formatter = DatetimeTickFormatter(
            hours=['%d %b %H:%M'],
            days=["%d %b"],
            months=["%d %m"],
        )
    p.xaxis.axis_label = timecol
    p.xaxis.axis_label_text_font_size = '12pt'
    p.xaxis.axis_label_text_font_style = 'normal'
    p.xaxis.axis_label_standoff = 15

    p.yaxis.axis_label = datacol
    p.yaxis.axis_label_text_font_size = '12pt'
    p.yaxis.axis_label_text_font_style = 'normal'
    p.yaxis.axis_label_standoff = 15

    p.xaxis.major_label_orientation = np.pi / 6.
    p.xaxis.major_label_text_font_size = '12pt'
    p.yaxis.major_label_text_font_size = '12pt'

    p.grid.grid_line_alpha = 0
    p.ygrid.band_fill_color = "grey"
    p.ygrid.band_fill_alpha = 0.2

    p.min_border_top = 20
    p.min_border_bottom = 40
    p.min_border_left = 50
    p.min_border_right = 50

    show(p)
