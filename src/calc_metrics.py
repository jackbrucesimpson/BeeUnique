import sys
import os

from Processor import PathMetrics
from Processor.graphics import plot_path_bg

def main():
    experiment_directory = sys.argv[1]

    pm = PathMetrics(experiment_directory)
    pm.generate_night_day_bgs()

    plot_path_bg(pm.night_day_bg_images['night'][0], pm.night_day_tag_paths['night'][0][50], '/home/jack/0' + '.png')
    plot_path_bg(pm.night_day_bg_images['night'][1], pm.night_day_tag_paths['night'][1][50], '/home/jack/1' + '.png')


    night = pm.night_day_tag_paths['night']

    print(type(night))
    print(len(night))

    print(type(night[0]))

    print(night[0].keys())
    print(type(night[0][50]))
    print(len(night[0][50]))
    print(len(night[1][50]))


    #print(night[0].keys())
    #print(night[0][50])

if __name__ == "__main__":
    main()
