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

        image_class_names = {0: 'CircleLine', 1: 'heart', 2: 'Note1', 3: 'DD', 4: 'Note2', 5: 'EE', 6: 'Pillars', 7: 'HH', 8: 'Ampersand', 9: 'Plant', 10: 'leaf', 11: 'arrowhollow', 12: 'nn', 13: 'Ankh', 14: 'sun', 15: 'TT', 16: 'Trident', 17: 'Asterisk', 18: 'UU', 19: '1', 20: '0', 21: '3', 22: '2', 23: '5', 24: '4', 25: '7', 26: '6', 27: '8', 28: 'Omega', 29: 'CircleCross', 30: 'AA', 31: 'SS', 32: 'Peace', 33: 'hash', 34: 'Tadpole', 35: 'ArrowLine', 36: 'Question', 37: 'RR', 38: 'PP', 39: 'lines3', 40: 'GG', 41: 'y', 42: 'XX', 43: 'ZZ', 44: 'radioactive', 45: 'Triangle', 46: 'Umbrella', 47: 'Dot', 48: 'a', 49: 'e', 50: 'Power', 51: 'KK', 52: 'h', 53: 'Queen', 54: 'Plane', 55: 'MM', 56: 'r', 57: 'circlehalf', 58: 'w', 59: 'unknown', 60: 'necklace', 61: 'Scissors'}

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
