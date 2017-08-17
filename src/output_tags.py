import sys

from Processor.file_utils import get_video_filename, create_dir_check_exists, read_coordinates_file
from Processor.image_utils import output_training_images

def main():
    csv_file = sys.argv[1]
    experiment_dir_path = sys.argv[2]
    reduce_images = bool(int(sys.argv[3]))

    video_datetime = get_video_filename(csv_file)
    bees_df, file_extension = read_coordinates_file(csv_file)

    image_output_directory = create_dir_check_exists(experiment_dir_path, 'training_images')
    csv_image_output_directory = create_dir_check_exists(image_output_directory, video_datetime)

    grouped_bee_id = bees_df.groupby('bee_id')
    for bee_id, df_bee_id in grouped_bee_id:
        output_training_images(bee_id, list(df_bee_id['frame_nums']), list(df_bee_id['flattened_28x28_tag_matrices']), \
                                csv_image_output_directory, reduce_images)


if __name__ == "__main__":
    main()
