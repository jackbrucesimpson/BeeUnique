import os

import numpy as np
import pandas as pd
from keras.models import load_model
import constants

def classify_tags(flattened_28x28_tag_matrices):
    this_dir, this_filename = os.path.split(__file__)
    data_path = os.path.join(this_dir, "model.h5")
    model = load_model(data_path)

    tag_image_array = np.array(list(flattened_28x28_tag_matrices))
    tag_image_array_tf_shaped = tag_image_array.reshape(tag_image_array.shape[0], 28, 28, 1)
    tag_image_array_tf_shaped_float = tag_image_array_tf_shaped.astype('float32')
    tag_image_array_tf_shaped_float /= 255
    predict_classes = model.predict_classes(tag_image_array_tf_shaped_float)
    return list(predict_classes)

def classify_df_tags(bees_df):
    bees_df_tags_predicted = bees_df[bees_df['flattened_28x28_tag_matrices'].notnull()]
    bees_df_tags_not_predicted = bees_df[bees_df['flattened_28x28_tag_matrices'].isnull()]

    bees_df_tags_predicted['classifications'] = classify_tags(bees_df_tags_predicted['flattened_28x28_tag_matrices'])

    bees_classified_df = pd.concat([bees_df_tags_predicted, bees_df_tags_not_predicted], ignore_index=True)
    bees_classified_df_sorted = bees_classified_df.sort_values('frame_nums', ascending=True)

    return bees_classified_df_sorted
