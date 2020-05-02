# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.3.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [raw] raw_mimetype="text/restructuredtext"
# .. _ug_basics:
#
# The basics
# ==========


# %% [raw] raw_mimetype="text/restructuredtext"
# .. _ug_intro:
#
# Figures and subplots
# --------------------
#
# ProPlot works by subclassing the matplotlib `~matplotlib.figure.Figure` and
# `~matplotlib.axes.Axes` classes. You can generate grids of proplot
# `~proplot.axes.Axes` axes on a proplot `~proplot.figure.Figure` using the
# `~proplot.ui.subplots` command.
#
# .. code-block:: python
#
#   import proplot as plot fig, axs = plot.subplots(...)
#
# * Just like `matplotlib.pyplot.subplots`, you can use
#   `~proplot.ui.subplots` without arguments to generate a single-axes subplot
#   or with `ncols` or `nrows` to set up simple grids of subplots.
# * Unlike `matplotlib.pyplot.subplots`, you can *also* use
#   `~proplot.ui.subplots` to draw arbitrarily complex grids using a 2D array
#   of integers. Just think of this array as a "picture" of your figure,
#   where each unique integer corresponds to a unique axes and ``0``
#   corresponds to an empty space.
#
# In the below examples, we create subplot grids with `~proplot.ui.subplots`
# and modify the axes using `~proplot.axes.Axes.format` and
# `~proplot.ui.SubplotsContainer`. See the :ref:`formatting guide <ug_format>`
# and the :ref:`subplots container <ug_container>` section for details.

# %%
import proplot as plot
import numpy as np
state = np.random.RandomState(51423)
data = 2 * (state.rand(100, 5) - 0.5).cumsum(axis=0)

# Simple plot
fig, axs = plot.subplots(ncols=2)
axs[0].plot(data, lw=2)
axs[0].format(xticks=20, xtickminor=False)
axs.format(
    suptitle='Simple subplot grid', title='Title',
    xlabel='x axis', ylabel='y axis'
)

# Complex grid
array = [  # the "picture"; 1 == subplot A, 2 == subplot B, etc.
    [1, 1, 2, 2],
    [0, 3, 3, 0],
]
fig, axs = plot.subplots(array, axwidth=1.8)
axs.format(
    abc=True, abcloc='ul', suptitle='Complex subplot grid',
    xlabel='xlabel', ylabel='ylabel'
)
axs[2].plot(data, lw=2)

# Really complex grid
array = [  # the "picture"
    [1, 1, 2],
    [1, 1, 6],
    [3, 4, 4],
    [3, 5, 5],
]
fig, axs = plot.subplots(array, width=5, span=False)
axs.format(
    suptitle='Really complex subplot grid',
    xlabel='xlabel', ylabel='ylabel', abc=True
)
axs[0].plot(data, lw=2)


# %% [raw] raw_mimetype="text/restructuredtext"
# .. _ug_plots:
#
# Plotting data
# -------------
#
# Matplotlib includes two APIs for creating plots: an object-oriented API,
# and a MATLAB-style `~matplotlib.pyplot` API (see matplotlib's
# `API guide <https://matplotlib.org/3.2.1/api/index.html>`__ for details).
# If you are already familiar with the object-oriented API, plotting in
# ProPlot will look exactly the same to you. This is because
# ProPlot's plotting features are a strict *superset* of matplotlib's
# features. Rather than creating a brand new interface, ProPlot simply builds
# upon the existing matplotlib constructs of the `~matplotlib.axes.Axes` and
# the `~matplotlib.figure.Figure`. This means a shallow learning curve for
# the average matplotlib user.
#
# In the below example, we create a 4-panel figure with the familiar matplotlib
# commands `~matplotlib.axes.Axes.plot`, `~matplotlib.axes.Axes.scatter`,
# `~matplotlib.axes.Axes.pcolormesh`, and `~matplotlib.axes.Axes.contourf`.
# See the :ref:`1d plotting <ug_1dplots>` and :ref:`2d plotting <ug_2dplots>`
# sections for details on the plotting features added by ProPlot.


# %%
import proplot as plot
import numpy as np

# Sample data
M, N = 50, 10
state = np.random.RandomState(51423)
data = (state.rand(M, N) - 0.5).cumsum(axis=0)

# Example plots
fig, axs = plot.subplots(ncols=2, nrows=2, share=0)
for offset, marker, linestyle in zip((0, 5), ('+', 'x'), ('-', '--')):
    axs[0].plot(data[:, offset:offset + 5], linewidth=2, linestyle=linestyle)
    axs[1].scatter(data[:, offset:offset + 5], marker=marker)
axs[2].pcolormesh(data, cmap='Greys')
axs[3].contourf(data, cmap='Greys')
axs.format(abc=True, xlabel='xlabel', ylabel='ylabel', suptitle='Quick plotting demo')


# %% [raw] raw_mimetype="text/restructuredtext"
# .. _ug_format:
#
# Formatting plots
# ----------------
#
# Every `~matplotlib.axes.Axes` returned by `~proplot.ui.subplots` has a
# ``format`` method. This is your one-stop-shop for changing axes settings.
# Keyword args passed to ``format`` are interpreted as follows:
#
# #. Any keyword arg matching the name of an `~proplot.config.rc` setting
#    will be applied to the axes using
#    `~proplot.config.rc_configurator.context`. If the name has "dots", simply
#    omit them. See the :ref:`configuration section <ug_config>` for
#    details.
# #. Remaining keyword args are passed to the class-specific
#    `proplot.axes.CartesianAxes.format`, `proplot.axes.PolarAxes.format`, or
#    `proplot.axes.GeoAxes.format` methods. These change settings that are
#    specific to the axes type.
# #. Still remaining keyword args are passed to the base
#    `proplot.axes.Axes.format` method. `~proplot.axes.Axes` is the base class
#    for all other axes classes. This changes axes titles, a-b-c subplot
#    labeling, and figure titles -- things that are the same for all axes
#    types.
#
# ``format`` lets you use simple shorthands for changing all kinds of
# settings at once, instead of one-liner setter methods like
# ``ax.set_title()``, ``ax.set_xlabel()``, and ``ax.xaxis.tick_params()``. It
# is also integrated with the `~proplot.constructor.Locator`,
# `~proplot.constructor.Formatter`, and `~proplot.constructor.Scale`
# constructor functions (see the :ref:`x and y axis settings <ug_xy_axis>`
# section for details).
#
# The below example shows the many different keyword arguments accepted by
# ``format``, and demonstrates how ``format`` can be used to succinctly and
# efficiently customize your plots.

# %%
import proplot as plot
import numpy as np
fig, axs = plot.subplots(ncols=2, nrows=2, share=0, tight=True, axwidth=1.7)
state = np.random.RandomState(51423)
axs[0].plot(np.linspace(1, 10, 80), (state.rand(80, 5) - 0.5).cumsum(axis=0))
axs.format(
    suptitle='Format command demo',
    abc=True, abcloc='ul', abcstyle='a.',
    title='Main', ltitle='Left', rtitle='Right',  # different titles
    urtitle='Title A', lltitle='Title B', lrtitle='Title C',  # extra titles
    collabels=['Column label 1', 'Column label 2'],
    rowlabels=['Row label 1', 'Row label 2'],
    xlabel='x-axis', ylabel='y-axis',
    xscale='log',
    xlim=(1, 10), xticks=1,
    ylim=(-2, 2), yticks=plot.arange(-2, 2),
    yticklabels=('a', 'bb', 'c', 'dd', 'e'),
    ytickloc='both', yticklabelloc='both',
    xtickdir='inout', xtickminor=False, ygridminor=True,
    linewidth=0.8, gridlinewidth=0.8, gridminorlinewidth=0.5,
)


# %% [raw] raw_mimetype="text/restructuredtext"
# .. _ug_rc:
#
# Changing rc settings
# --------------------
#
# A special object named `~proplot.config.rc` is created whenever you import
# ProPlot. `~proplot.config.rc` is similar to the matplotlib
# `~matplotlib.rcParams` dictionary, but can be used to change (1)
# matplotlib's `builtin settings
# <https://matplotlib.org/tutorials/introductory/customizing.html>`_, (2)
# ProPlot's :ref:`added settings <rc_added>`, and (3) :ref:`quick settings
# <rc_quick>` that can be used to change lots of matplotlib and ProPlot
# settings at once. See the :ref:`configuration section <ug_config>` for
# details.
#
# To modify a setting for just one subplot, you can pass it to the
# `~proplot.axes.Axes` `~proplot.axes.Axes.format` method. To temporarily
# modify setting(s) for a block of code, use
# `~proplot.config.rc_configurator.context`. To modify setting(s) for the
# entire python session, just assign it to the `~proplot.config.rc` object or
# use `~proplot.config.rc_configurator.update`.  To reset everything to the
# default state, use `~proplot.config.rc_configurator.reset`. See the below
# example.

# %%
import proplot as plot
import numpy as np

# Update global settings in several different ways
plot.rc.cycle = 'colorblind'
plot.rc.color = 'gray6'
plot.rc.update({'fontname': 'Noto Sans'})
plot.rc['figure.facecolor'] = 'gray3'
plot.rc.axesfacecolor = 'gray4'

# Apply settings to figure with context()
with plot.rc.context({'suptitle.size': 11}, toplabelcolor='gray6', linewidth=1.5):
    fig, axs = plot.subplots(ncols=2, aspect=1, width=6, span=False, sharey=2)

# Plot lines
N, M = 100, 6
state = np.random.RandomState(51423)
values = np.arange(1, M + 1)
for i, ax in enumerate(axs):
    data = np.cumsum(state.rand(N, M) - 0.5, axis=0)
    lines = ax.plot(data, linewidth=3, cycle='Grays')

# Apply settings to axes with format()
axs.format(
    grid=False, xlabel='x label', ylabel='y label',
    collabels=['Column label 1', 'Column label 2'],
    suptitle='Rc settings demo',
    suptitlecolor='gray7',
    abc=True, abcloc='l', abcstyle='A)',
    title='Title', titleloc='r', titlecolor='gray7'
)
ay = axs[-1].twinx()
ay.format(ycolor='red', linewidth=1.5, ylabel='secondary axis')
ay.plot((state.rand(100) - 0.2).cumsum(), color='r', lw=3)

# Reset persistent modifications from head of cell
plot.rc.reset()


# %% [raw] raw_mimetype="text/restructuredtext"
# .. _ug_container:
#
# Subplot containers
# ------------------
#
# Instead of an `~numpy.ndarray` of axes, `~proplot.ui.subplots` returns a
# special `~proplot.ui.SubplotsContainer` container. This container behaves
# like a *python list*, but lets you call any arbitrary method on multiple
# axes at once. It supports both 2D indexing (e.g. ``axs[0,1]``) and 1D
# indexing (e.g. ``axs[2]``), and is row-major by default. Further, slicing a
# subplot grid (e.g. ``axs[:,0]``) returns another subplot grid.
#
# In the below example, the `~proplot.ui.SubplotsContainer` returned by
# `~proplot.ui.subplots` is used to call `~proplot.axes.Axes.format` on
# several axes at once. Note that you can make your own subplot grid simply
# by passing a list of axes to `~proplot.ui.SubplotsContainer`.

# %%
import proplot as plot
import numpy as np
state = np.random.RandomState(51423)
fig, axs = plot.subplots(ncols=4, nrows=4, axwidth=1.2)
axs.format(
    xlabel='xlabel', ylabel='ylabel', suptitle='Subplot grid demo',
    grid=False, xlim=(0, 50), ylim=(-4, 4)
)

# Various ways to select subplots in the subplot grid
axs[:, 0].format(color='blue7', facecolor='gray3', linewidth=1)
axs[0, :].format(color='red7', facecolor='gray3', linewidth=1)
axs[0].format(color='black', facecolor='gray5', linewidth=1.4)
axs[1:, 1:].format(facecolor='gray1')
for ax in axs[1:, 1:]:
    ax.plot((state.rand(50, 5) - 0.5).cumsum(axis=0), cycle='Grays', lw=2)
