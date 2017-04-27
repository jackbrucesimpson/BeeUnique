import cv2
import numpy as np

def mean_smooth(image):
    mean_smoothed = cv2.blur(image, (3, 3))
    return mean_smoothed

def add_noise(image, n_or_u):
    noise = np.zeros((28,28), np.uint8)
    if n_or_u == 'n':
        cv2.randn(noise, 30, 2)
    else:
        cv2.randu(noise, 30, 2)
    noisy_image = np.uint32(image) + noise
    noisy_image[noisy_image < 0] = 0
    noisy_image[noisy_image > 255] = 255
    noisy_image = np.uint8(noisy_image)
    return noisy_image

def rotate_image(image):
    rotated_images = []
    for angle in range(45, 360, 45):
        M = cv2.getRotationMatrix2D((14,14),angle,1)
        r = cv2.warpAffine(image,M,(28,28))
        rotated_images.append(r)
    return rotated_images

def norm_image(image):
    image[image < 0] = 0
    image[image > 255] = 255
    return np.uint8(image)

def change_brightness_contrast(image):
    image_int32 = np.int32(image)
    increase_brightness = norm_image(image_int32 + 70)
    decrease_brightness = norm_image(image_int32 - 70)
    increase_contrast = norm_image(image_int32 * 1.4)
    decrease_contrast = norm_image(image_int32 * 0.4)

    return [increase_brightness, decrease_brightness, increase_contrast, decrease_contrast]

def translate_image(image):
    translated_images = []
    for t in [(0,25, 0,25, 1,26, 1,26), (3,28, 3,28, 2,27, 2,27), (1,26, 3,28, 2,27, 2,27), (3,28, 1,26, 2,27, 2,27)]:
        full_size = np.zeros((28, 28), dtype=np.uint8)
        cv2.randn(full_size, 50, 3)
        full_size[t[0]:t[1], t[2]:t[3]] = image[t[4]:t[5], t[6]:t[7]]
        translated_images.append(full_size)
    return translated_images

def resize_image(image):
    i_size = cv2.resize(image,(32, 32), interpolation = cv2.INTER_CUBIC)
    d_size = cv2.resize(image,(24, 24), interpolation = cv2.INTER_AREA)
    zoomed_in = i_size[2:30, 2:30]
    zoomed_out = np.zeros((28, 28), dtype=np.uint8)
    cv2.randn(zoomed_out, 40, 2)
    zoomed_out[2:26, 2:26] = d_size
    return [zoomed_in, zoomed_out]

def occlude_edges(image):
    full_size = np.zeros((28, 28), dtype=np.uint8)
    full_size[4:24, 4:24] = image[4:24, 4:24]
    return full_size

def processing_pipeline(image):
    outputs = [image, occlude_edges(image), add_noise(mean_smooth(image), 'u')]
    outputs.extend(change_brightness_contrast(image))

    for r in rotate_image(image):
        for z in resize_image(r):
            outputs.append(z)

    return outputs
