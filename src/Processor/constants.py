

tag_class_names = {0: 'CircleLine', 1: 'Leaf', 2: 'Note1', 3: 'Unknown', 4: 'DD', 5: 'Peace', 6: 'Question', 7: 'Pillars', 8: 'HH', 9: 'Ampersand', 10: 'PP', 11: 'Hash', 12: 'Power', 13: 'Ankh', 14: 'TT', 15: 'Trident', 16: 'Asterisk', 17: '4', 18: 'Lines3', 19: '1', 20: '0', 21: '3', 22: 'Plane', 23: '5', 24: 'CircleHalf', 25: '7', 26: 'Sun', 27: '8', 28: 'Omega', 29: 'ArrowHollow', 30: 'AA', 31: 'Note2', 32: 'Radioactive', 33: 'EE', 34: 'UU', 35: '6', 36: 'Plant', 37: 'GG', 38: 'XX', 39: 'ZZ', 40: 'Necklace', 41: 'Umbrella', 42: 'Triangle', 43: 'Dot', 44: 'a', 45: 'Heart', 46: 'e', 47: 'RR', 48: 'KK', 49: 'h', 50: 'Queen', 51: 'Tadpole', 52: 'n', 53: 'MM', 54: '2', 55: 'r', 56: 'ArrowLine', 57: 'y', 58: 'Scissors', 59: 'CircleCross'}

unknown_class_num = None
for tag_class in tag_class_names:
    if tag_class_names[tag_class] == 'Unknown':
        unknown_class_num = tag_class

UNKNOWN_CLASS = unknown_class_num
MIXED_CLASS = 'mixed'
GAP_CLASS = 'gap'
MAX_FRAME_GAP_BETWEEN_PATHS = 10
NUM_GROUP_CLASSIFICATIONS = 40
MIN_NUM_CLASSIFIED_GROUP = 10
NUM_GROUPS_IN_SECTION = 5
CLASS_CONF_THRESH = 0.6
NUM_UNKNOWNS_IN_PATH_THRESHOLD = 3
NUM_FRAMES_IN_VIDEO = 72000
