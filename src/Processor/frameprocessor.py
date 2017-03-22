import multiprocessing
import cv2
import collections
import operator
import os
import uuid

UNKNOWN_CLASS = 0

class FrameProcessor:
    def __init__(self, output_directory, is_training):
        self.is_training = is_training
        self.output_directory = output_directory
        self.num_frames_averaged = 0
        self.frame_bg_sample_freq = 20
        self.sum_matrix_bg = None
        self.num_frames_batch_process = 100
        self.num_frames_predict_tags = 10000
        self.n_processes = 4
        self.chunksize = 1
        self.list_frames = []
        self.frame_counter = 0

    def append_frame_increment_counter(self, frame):
        self.list_frames.append((self.frame_counter, frame))
        self.frame_counter += 1

        # check to add frame to background average
        if self.frame_counter % self.frame_bg_sample_freq == 0:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if self.sum_matrix_bg is None:
                self.sum_matrix_bg = gray.astype(np.float64)
            else:
                self.sum_matrix_bg += gray.astype(np.float64)
            self.num_frames_averaged += 1

        # check if enough frames to process
        if self.frame_counter % self.num_frames_batch_process == 0:
            return True
        else:
            return False

    def parallel_process_frames(self):
        processes = multiprocessing.Pool(processes=self.n_processes)
        frames_output = processes.map(func=segment_frame, iterable=self.list_frames, chunksize=self.chunksize)
        processes.close()
        processes.join()

        frames_output.sort(key=operator.itemgetter('frame_num'))

        frame_nums = []
        all_tag_locs = []
        all_tag_images_classify = []
        all_tag_loc_indexes = []
        all_classified_loc_indexes = []

        for frame_output in frames_output:
            frame_nums.append(frame_output['frame_num'])
            all_tag_locs.append(frame_output['tag_locs'])
            all_tag_images_classify.extend(frame_output['tag_images_classify'])
            all_tag_loc_indexes.append(frame_output['tag_loc_indexes'])

        tag_classifications = self.classify_tags(all_tag_images_classify, training=self.is_training)

        i = 0
        for frame_loc_indexes in all_tag_loc_indexes:
            classified_loc_indexes = []
            for loc_index in frame_loc_indexes:
                classified_loc_indexes.append({'loc_index': loc_index, 'classification': tag_classifications[i]})
                i += 1
            all_classified_loc_indexes.append(classified_loc_indexes)

        if self.is_training:
            for i, frame in enumerate(list_frames):
                tracker.track_frame(all_tag_locs[i], all_classified_loc_indexes[i])
                tracked_bees = tracker.get_tracked_bees_current_frame(frame_nums[i])
                overlaid_frame = self.overlay_frame(frame, tracked_bees)
                resized_overlaid_frame = cv2.resize(overlaid_frame, (1200, 720));

                cv2.imshow('frame', resized_overlaid_frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        else:
            tracker.track_frames_batch(all_tag_locs, all_classified_loc_indexes)

        self.list_frames = []
        return (all_tag_locs, all_classified_loc_indexes)

    def overlay_frame(self, frame, tracked_bees):
        for bee in tracked_bees:
            cv2.rectangle(frame, (int(bee['x']-14), int(bee['y']-14)), (int(bee['x']+14), int(bee['y']+14)), (0,255,0), 2)
            #bee['bee_classification'], bee['current_tag_classification']
            return frame

    def classify_tags(self, all_tag_images_classify, training):
        classifications = []
        if training:
            classifications = [0] * len(all_tag_images_classify)
            for img in all_tag_images_classify:
                filename = uuid.uuid4().hex + '.png'
                file_output = os.path.join(self.output_directory, filename)
                cv2.imwrite(file_output, img)
        else:
            pass
        return classifications

    def output_background_image(self):
        clahe = cv2.createCLAHE(clipLimit=10.0, tileGridSize=(9,9))
        img = self.sum_matrix_bg / self.num_frames_averaged
        img_uint8 = self.sum_matrix_bg.astype(np.uint8)
        clahe_img = clahe.apply(img_uint8)

        filename = 'bg' + '.png'
        file_output = os.path.join(self.output_directory, filename)

        cv2.imwrite(file_output, clahe_img)

def segment_frame(counter_frame):
    rect_dims = 15
    frame_num, frame = counter_frame
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    smoothed_frame = cv2.GaussianBlur(gray_frame, (9, 9), 0)

    grad_x = cv2.Sobel(smoothed_frame, cv2.CV_16S, 1, 0, ksize=3, scale=1.5, delta=0, borderType=cv2.BORDER_DEFAULT)
    grad_y = cv2.Sobel(smoothed_frame, cv2.CV_16S, 0, 1, ksize=3, scale=1.5, delta=0, borderType=cv2.BORDER_DEFAULT)
    abs_grad_x = cv2.convertScaleAbs(grad_x)
    abs_grad_y = cv2.convertScaleAbs(grad_y)
    scharr = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
    ret, thresh = cv2.threshold(scharr, 70, 255, 0)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(13, 13))
    closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    tag_locs = []
    tag_images_classify = []
    tag_loc_indexes = []

    contour_index = 0
    contours, hierarchy = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        if cv2.contourArea(cnt) > 100:
            centre, width_height, rotation = cv2.minAreaRect(cnt)
            tag_locs.append({'x': centre[0], 'y': centre[1]})
            if width_height[0] > 27 and abs(width_height[0] - width_height[1]) < 4 and width_height[0] < 100:
                extract_tag = frame[int(centre[1])-rect_dims:int(centre[1])+rect_dims, int(centre[0])-rect_dims:int(centre[0])+rect_dims]
                tag_images_classify.append(extract_tag)
                tag_loc_indexes.append(contour_index)
            contour_index += 1

    return {'frame_num': frame_num, 'tag_locs': tag_locs, 'tag_images_classify': tag_images_classify, 'tag_loc_indexes': tag_loc_indexes}
