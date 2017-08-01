from utilities import get_video_filename
import pandas as pd
import cv2

class FrameOverlayer:
    def __init__(self, video_path, csv_file_path):
        self.frame_counter = 0
        self.offset = -20
        video_filename = get_video_filename(video_path)
        self.bees_paths_df = pd.read_csv(csv_file_path)
        #print(self.bees_paths_df.head())
        self.bees_paths_df['xy'] = self.bees_paths_df['xy'].apply(lambda x: eval(x))
        #print(self.bees_paths_df.head())

    def overlay_frame(self, frame):

        image_class_names = {0: 'CircleLine', 1: 'Leaf', 2: 'Note1', 3: 'Unknown', 4: 'DD', 5: 'Peace', 6: 'Question', 7: 'Pillars', 8: 'HH', 9: 'Ampersand', 10: 'PP', 11: 'Hash', 12: 'Power', 13: 'Ankh', 14: 'TT', 15: 'Trident', 16: 'Asterisk', 17: '4', 18: 'Lines3', 19: '1', 20: '0', 21: '3', 22: 'Plane', 23: '5', 24: 'CircleHalf', 25: '7', 26: 'Sun', 27: '8', 28: 'Omega', 29: 'ArrowHollow', 30: 'AA', 31: 'Note2', 32: 'Radioactive', 33: 'EE', 34: 'UU', 35: '6', 36: 'Plant', 37: 'GG', 38: 'XX', 39: 'ZZ', 40: 'Necklace', 41: 'Umbrella', 42: 'Triangle', 43: 'Dot', 44: 'a', 45: 'Heart', 46: 'e', 47: 'RR', 48: 'KK', 49: 'h', 50: 'Queen', 51: 'Tadpole', 52: 'n', 53: 'MM', 54: '2', 55: 'r', 56: 'ArrowLine', 57: 'y', 58: 'Scissors', 59: 'CircleCross'}

        frame_df = self.bees_paths_df[self.bees_paths_df['frame_nums']==self.frame_counter]
        frame_num_text = 'Frame: ' + str(self.frame_counter)
        cv2.putText(frame, frame_num_text, (40, 40), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)
        for row in frame_df.itertuples():
            cv2.rectangle(frame, (int(row.xy['x']-15), int(row.xy['y']-15)), (int(row.xy['x']+15), int(row.xy['y']+15)), (0,255,0), 2)
            #frame_class_bee_class_text = "{} {} {}".format(row.CLASSIFIED, row.CLASS_CLASSIFIED, row.BEE_ID)
            frame_class_bee_class_text = image_class_names[row.classifications]
            #if row.CLASSIFIED == -1:
                #frame_class_bee_class_text = str(row.classifications)
            #else:
                #frame_class_bee_class_text = image_class_names[row.classifications]

            cv2.putText(frame, frame_class_bee_class_text, (int(row.xy['x'] + self.offset), int(row.xy['y'] + self.offset)), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)

        self.frame_counter += 1
        return frame
