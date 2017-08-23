import matplotlib
matplotlib.use("Agg")
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
rcParams['figure.figsize'] = 20, 16

import matplotlib.pyplot as plt
import matplotlib.cm as cm
#plt.style.use('ggplot')

def plot_barplot(list_values, list_values_names, file_name, title, xtitle, ytitle, ymin, ymax):
    plt.figure()
    plt.bar(range(len(list_values)), list_values)
    plt.xticks(range(len(list_values_names)), list_values_names, rotation=90)
    plt.ylim(ymin, ymax)
    plt.xlabel(xtitle)
    plt.ylabel(ytitle)
    plt.title(title)
    plt.savefig(file_name)
    plt.clf()
    plt.close()

def plot_path_bg(bg_image, paths, file_name):
    plt.figure()
    for path in paths:
        plt.plot(path['x_path'], path['y_path'], alpha=0.2, color='r')
    plt.imshow(bg_image, cmap=cm.Greys_r)
    plt.axis('off')
    plt.savefig(file_name, dpi=100)
    plt.show()

def plot_heatmaps(heatmap, vmax, title, filename):
    plt.figure()
    plt.imshow(heatmap, interpolation="nearest", vmin=0, vmax=vmax)
    plt.xlabel("Bottom of frame")
    plt.ylabel("Left side of frame")
    plt.colorbar()
    plt.title(title)
    plt.savefig(filename)
    plt.clf()
    plt.close()

def create_histogram(list_of_values, title, filename):
    plt.figure()
    plt.hist(list_of_values, bins=100)
    plt.xlabel("Values")
    plt.ylabel("Frequency")
    plt.title(title)
    plt.savefig(filename)
    plt.clf()
    plt.close()
