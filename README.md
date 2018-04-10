# bokeh-wrap
Convenience wrapper using [bokeh][bokeh-home] for plotting interactive histograms and time series data.

## Requirements:

* Python 3
* conda

Easiest to install both via [Anaconda][anaconda-download]

## Usage

Create a virtual environment, activate it, from within it install an IPython kernel using this environment, then start a Jupyter Notebok server:

    $ conda env create -f environment.yml -q
    $ source activate bokeh_wrap
    (bokeh_wrap) $ python -m ipykernel install --user --name bokeh_wrap --display-name "Python bokeh_wrap"
    (bokeh_wrap) $ jupyter notebook

Open notebook **BokehWrapDemo.ipynb** in the Jupyter Notebook GUI, and then choose this environment's kernel as one of the options under **Kernel > Change Kernel**:

![change kernel](https://raw.githubusercontent.com/dpshenoy/bokeh_wrap/master/choose_kernel.png)

[anaconda-download]: https://www.anaconda.com/download/
[bokeh-home]: https://bokeh.pydata.org/en/latest/
