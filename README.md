# bokeh-wrap
Convenience wrapper using [bokeh][bokeh-home] for plotting interactive histograms and time series data.

## Requirements:

* Python 3
* conda

Easiest to install both via [Anaconda][anaconda-download]

## First Time Usage

Create a virtual environment, activate it, from within it install an IPython kernel using this environment, then start a Jupyter Notebok server:

    $ conda env create -f environment.yml -q
    $ source activate bokeh_wrap
    (bokeh_wrap) $ python -m ipykernel install --user --name bokeh_wrap --display-name "Python bokeh_wrap"
    (bokeh_wrap) $ jupyter notebook

Open notebook **BokehWrapDemo.ipynb** in the Jupyter Notebook GUI, and then choose this environment's kernel as one of the options under **Kernel > Change Kernel**:

![change kernel](https://raw.githubusercontent.com/dpshenoy/bokeh_wrap/master/choose_kernel.png)

Run the notebook. To stop the notebook server, hit **Ctrl+C** twice. To deactivate the virtual environment:

    (bokeh_wrap) $ source deactivate

## Subsequent Usage

For subsequent use, you only need do:

    $ source activate bokeh_wrap
    (bokeh_wrap) $ jupyter notebook

## Cleanup

If you want to remove the virtual environment:

    $ conda remove -n bokeh_wrap --all

If you want to remove the "Python bokeh_wrap" kernel choice from Jupyter notebook, locate the directory containing it and remove that directory. For example:

    $ jupyter kernelspec list | grep bokeh_wrap
    bokeh_wrap    /Users/dinesh.shenoy/Library/Jupyter/kernels/bokeh_wrap
    $ rm -rf /Users/dinesh.shenoy/Library/Jupyter/kernels/bokeh_wrap

[anaconda-download]: https://www.anaconda.com/download/
[bokeh-home]: https://bokeh.pydata.org/en/latest/
