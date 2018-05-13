import sys

TAG_CLASS_NAMES = {0: 'CircleLine', 1: 'Sun', 2: 'Unknown', 3: 'Peace', 4: 'Pillars', 5: 'H', 6: 'Ampersand', 7: 'P', 8: 'Hash', 9: 'R', 10: 'Ankh', 11: 'Trident', 12: 'Asterisk', 13: '4', 14: 'Lines3', 15: '1', 16: '0', 17: '3', 18: 'Plane', 19: '5', 20: 'CircleHalf', 21: '7', 22: '6', 23: '8', 24: 'Omega', 25: 'ArrowHollow', 26: 'A', 27: 'Radioactive', 28: 'Heart', 29: 'E', 30: 'U', 31: 'Plant', 32: 'G', 33: 'X', 34: 'Z', 35: 'Necklace', 36: 'Triangle', 37: 'Dot', 38: 'a', 39: 'Note', 40: 'e', 41: 'Power', 42: 'K', 43: 'h', 44: 'Queen', 45: 'Tadpole', 46: 'M', 47: '2', 48: 'r', 49: 'ArrowLine', 50: 'y', 51: 'CircleCross'}

control_class_names = ['CircleLine', 'Sun', 'Peace', 'Pillars', 'Hash', 'Ankh', 'Trident', 'Lines3', 'Plane', 'CircleHalf', 'Omega', 'ArrowHollow', 'Radioactive', 'Heart', 'Plant', 'Necklace', 'Triangle', 'Dot', 'Note', 'Power', 'Tadpole', 'ArrowLine', 'CircleCross', 'Asterisk', 'Ampersand']

treatment_class_names = ['H', 'P', 'R', '4', '1', '0', '3', '5', '7', '6', '8', 'A', 'E', 'U', 'G', 'X', 'Z', 'a', 'e', 'K', 'h', 'M', '2', 'r', 'y']

unknown_class_num = None
queen_class_num = None
treatment_class_nums = []
control_class_nums = []
for tag_class in TAG_CLASS_NAMES.keys():
    if TAG_CLASS_NAMES[tag_class] == 'Unknown':
        unknown_class_num = tag_class
    elif TAG_CLASS_NAMES[tag_class] == 'Queen':
        queen_class_num = tag_class
    elif TAG_CLASS_NAMES[tag_class] in treatment_class_names:
        treatment_class_nums.append(tag_class)
    elif TAG_CLASS_NAMES[tag_class] in control_class_names:
        control_class_nums.append(tag_class)
    else:
        print("Eror, couldn't find control/treatment class name")
        sys.exit(1)

NIGHT_HOURS = [19, 20, 21, 22, 23, 0, 1, 2, 3, 4, 5, 6]
FPS = 20
SECONDS_IN_45_MINS = 2700
SECONDS_IN_HOUR = 3600
SECONDS_IN_12_HOURS = 43200
NUM_FRAMES_IN_VIDEO = FPS * SECONDS_IN_HOUR
TAG_DIAMETER = 30
HALF_TAG_DIAMETER = int(TAG_DIAMETER / 2)
DOUBLE_TAG_DIAMETER = int(TAG_DIAMETER * 2)
PERIMETER_RADIUS = int(TAG_DIAMETER * 6)
MIN_NUM_SECONDS_SPENT_IN_AREA = 15

MAX_FRAME_GAP_BETWEEN_PATHS = 1 * FPS
MAX_FRAME_GAP_BETWEEN_VIDEOS = 3 * FPS

UNKNOWN_CLASS = unknown_class_num
QUEEN_CLASS = queen_class_num
TREATMENT_CLASSES = treatment_class_nums
CONTROL_CLASSES = control_class_nums

MIXED_CLASS = 'mixed'
GAP_CLASS = 'gap'

NUM_GROUP_CLASSIFICATIONS = 40
MIN_NUM_CLASSIFIED_GROUP = 10
NUM_GROUPS_IN_SECTION = 5
CLASS_CONF_THRESH = 0.6
NUM_UNKNOWNS_IN_PATH_THRESHOLD = 3

NUM_X_CELLS = 80
NUM_Y_CELLS = 40
X_BINS = 3840/NUM_X_CELLS
Y_BINS = 2160/NUM_Y_CELLS
