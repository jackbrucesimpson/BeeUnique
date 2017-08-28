import matplotlib
matplotlib.use("Agg")
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
rcParams['figure.figsize'] = 20, 16

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
#plt.style.use('ggplot')

import cv2

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

def plot_path_bg(x_paths, y_paths, bg_image, file_name):
    plt.figure()
    for i in range(len(x_paths)):
        plt.plot(x_paths[i], y_paths[i], alpha=0.2, color='r')
    plt.imshow(bg_image, cmap=cm.Greys_r)
    plt.axis('off')
    plt.savefig(file_name, dpi=100)
    plt.clf()
    plt.close()

def plot_heatmaps_bg_image(heatmap, bg_image, vmax, title, file_name):
    # resize so same size as bg image
    upscaled_heatmap = cv2.resize(heatmap, (3840, 2160))

    plt.figure()
    plt.imshow(bg_image, cmap = cm.Greys_r)
    plt.imshow(upscaled_heatmap, vmin=0, alpha=0.3, interpolation='bilinear', cmap='jet')
    plt.axis('off')
    plt.xlabel("Bottom of frame")
    plt.ylabel("Left side of frame")
    #plt.colorbar()
    plt.title(title)
    plt.show()
    plt.savefig(file_name)
    plt.clf()
    plt.close()


def plot_heatmaps(heatmap, vmax, title, file_name):
    plt.figure()
    #interpolation="nearest",
    #plt.imshow(heatmap, vmin=0, vmax=vmax, interpolation='gaussian')
    plt.imshow(heatmap, vmin=0, interpolation='bilinear')
    plt.xlabel("Bottom of frame")
    plt.ylabel("Left side of frame")
    plt.colorbar()
    plt.title(title)
    plt.show()
    plt.savefig(filename)
    plt.clf()
    plt.close()

def plot_histogram(list_of_values, title, file_name):
    plt.figure()
    plt.hist(list_of_values, bins=100)
    plt.xlabel("Values")
    plt.ylabel("Frequency")
    plt.title(title)
    plt.savefig(file_name)
    plt.clf()
    plt.close()
