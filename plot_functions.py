import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import numpy as np

########### 
#  colors
# #87C8E3 - silver blue
# #596063 - grey
# #E3B887 - lightbrown
# #CC5C82 - red

colors = ["#00be00", "#00c9ff", "#dc8200", "#fc65ff", "#993a03", "#00734a", "#9e46a8", "#32587c"]

def plot_year_time_series(years, to_plot, ylabel = None, xlabel = None, legend = None, fname = None):

    plt.figure(figsize = (13,7))
    if isinstance(to_plot, list) and len(to_plot) >= 2:
        for plot, year, col in zip(to_plot, years, colors):
            plt.plot(year, plot, linewidth = 3.5, color = col)
    else:
        plt.plot(years, to_plot, linewidth = 3.5, color = "#dc8200")
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    plt.xticks(rotation = 30, size = 22)
    plt.yticks(size = 22)
    if xlabel is not None:
        plt.xlabel(xlabel, size = 27)
    if ylabel is not None:
        plt.ylabel(ylabel, size = 27, style = "italic")
    plt.xlim([1950, 2020])
    plt.gca().xaxis.set_major_locator(MultipleLocator(10))
    plt.gca().xaxis.set_minor_locator(MultipleLocator(2))
    if legend is not None:
        plt.legend(legend)
    if fname is None:
        plt.show()
    else:
        plt.savefig(fname, bbox_inches = 'tight')


def histogram(data, bins = 30, ylabel = None, xlabel = None, fname = None):

    plt.figure(figsize = (7,7))
    plt.hist(data, bins = bins, fc = colors[0])
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    plt.xticks(size = 22)
    plt.yticks(size = 22)
    if xlabel is not None:
        plt.xlabel(xlabel, size = 27)
    if ylabel is not None:
        plt.ylabel(ylabel, size = 27, style = "italic")
    rng = (data.max() - data.min())
    plt.gca().xaxis.set_major_locator(MultipleLocator(rng//6))
    plt.gca().xaxis.set_minor_locator(MultipleLocator(rng//12))

    if fname is None:
        plt.show()
    else:
        plt.savefig(fname, bbox_inches = 'tight')


