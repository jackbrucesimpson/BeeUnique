import cv2

import matplotlib
matplotlib.use("Agg")
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
#plt.style.use('ggplot')

def plot_barplot(list_values, list_values_names, file_name, title, xtitle, ytitle, ymin, ymax):
    plt.figure(figsize=(20,16))
    plt.bar(range(len(list_values)), list_values)
    plt.xticks(range(len(list_values_names)), list_values_names, rotation=90)
    plt.ylim(ymin, ymax)
    plt.xlabel(xtitle)
    plt.ylabel(ytitle)
    plt.title(title)
    plt.savefig(file_name, dpi=100)
    plt.clf()
    plt.close()

def plot_seconds_of_activity(seconds_activity, file_name):
    num_y_cells = 2
    num_x_cells = sum([a['num_seconds'] if a['num_seconds'] > 0 else 1 for a in seconds_activity])
    seconds_array = np.zeros((num_y_cells, num_x_cells, 3), dtype=np.uint8)

    absent_blue_color = (65, 105, 225)
    moving_black_color = (0, 0, 0)
    motionless_red_color = (205, 92, 92)
    filler_grey_color = (128,128,128)

    seconds_index = 0
    for a in seconds_activity:
        if a['activity'] == 'filler':
            width = a['num_seconds']
            seconds_array[0, seconds_index:seconds_index + width] = filler_grey_color
            seconds_index += width
        elif a['activity'] == 'absent':
            width = a['num_seconds']
            seconds_array[0, seconds_index:seconds_index + width] = absent_blue_color
            seconds_index += width
        elif a['activity'] == 'moving':
            width = 1
            seconds_array[0, seconds_index:seconds_index + width] = moving_black_color
            seconds_index += width
        else:
            width = a['num_seconds']
            seconds_array[0, seconds_index:seconds_index + width] = motionless_red_color
            seconds_index += width

    is_night = True
    for i in np.arange(1, num_x_cells, 43200):
        if is_night:
            seconds_array[1, i:i+43200] = (51, 153, 255)
            is_night = False
        else:
            seconds_array[1, i:i+43200] = (255,255,102)
            is_night = True

    plt.figure(figsize=(100,10))
    plt.imshow(seconds_array, extent=[0, num_x_cells, 0, 1], aspect='auto')
    #
    #plt.show()

    #plt.ylim(0, 1)
    #plt.xlim(0, 30000)


        #print(seconds_index)


    #for xc in np.arange(0, num_x_cells, 43200):
        #plt.axvline(x=xc, ymin=-1, linewidth=1, color='green', alpha=1)



    #plt.axis('off')
    plt.yticks([])
    plt.xticks(np.arange(21600, num_x_cells, 43200), ['Night' if i%2==0 else 'Day' for i in range(len(np.arange(0, num_x_cells, 43200)))])
    #plt.set_xticklabels()

    #plt.ylim(0,10)
    #plt.xlim(0,10)
    #plt.axis('off')

    #plt.ylim(0,1)
    #plt.xlim(0,seconds_index)
    plt.savefig(file_name, dpi=300)


    plt.clf()
    plt.close()

    #plt.bar(range(len(list_values)), list_values)
    #plt.xticks(range(len(list_values_names)), list_values_names, rotation=90)
    #plt.ylim(ymin, ymax)
    #plt.xlabel(xtitle)
    #plt.ylabel(ytitle)
    #plt.title(title)
    #plt.savefig(file_name, dpi=100)
    #plt.clf()
    #plt.close()


def plot_path_bg(x_path, y_path, bg_image, file_name):
    plt.figure(figsize=(20,16))
    plt.plot(x_path, y_path, alpha=0.8, color='orange', linewidth=2, marker='o', linestyle='-')
    #for i in range(len(x_paths)):
        #plt.plot(x_paths[i], y_paths[i], alpha=0.5, color='r', marker='o', linestyle='--')
    plt.imshow(bg_image, cmap=cm.Greys_r)
    plt.axis('off')
    plt.savefig(file_name, dpi=100)
    plt.clf()
    plt.close()

def plot_line(x_values, y_values, title, xtitle, ytitle, ymin, ymax, file_name):
    plt.figure(figsize=(20,16))
    plt.plot(x_values, y_values, alpha=1, color='r')
    #plt.ylim(ymin, ymax)
    plt.xlabel(xtitle)
    plt.ylabel(ytitle)
    plt.title(title)
    plt.savefig(file_name, dpi=100)
    plt.clf()
    plt.close()

def plot_heatmaps_bg_image(heatmap, bg_image, vmax, title, file_name):
    # resize so same size as bg image
    upscaled_heatmap = cv2.resize(heatmap, (3840, 2160))

    plt.figure(figsize=(20,16))
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
    plt.figure(figsize=(20,16))
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
    plt.figure(figsize=(20,16))
    plt.hist(list_of_values, bins=100)
    plt.xlabel("Values")
    plt.ylabel("Frequency")
    plt.title(title)
    plt.savefig(file_name)
    plt.clf()
    plt.close()

def plot_scatter(x, y, title, x_title, y_title, file_name):
    plt.figure(figsize=(20,16))
    plt.scatter(x, y)
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    plt.title(title)
    plt.savefig(file_name)
    plt.clf()
    plt.close()
