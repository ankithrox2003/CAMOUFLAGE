import os
import cv2
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img

# Paths to input/output image folders
input_folder = 'input'
output_folder = 'output'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Helper function to adjust contrast and brightness
def adjust_contrast_brightness(image, contrast=1.0, brightness=0):
    return cv2.convertScaleAbs(image, alpha=contrast, beta=brightness)

# Initialize the ImageDataGenerator with minimal transformations
datagen = ImageDataGenerator(
    rotation_range=0,               # Set rotation to 0 to avoid gaps
    width_shift_range=0,            # No shift
    height_shift_range=0,           # No shift
    shear_range=0,                  # No shearing
    zoom_range=[1.0, 1.0],          # No zooming
    horizontal_flip=True,           # Flip images horizontally
    fill_mode='nearest',            # Fill any small empty pixels with nearest
    rescale=1./255                  # Rescale pixel values between 0 and 1
)

# Loop through each image in the folder
for filename in os.listdir(input_folder):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        # Load the image
        img_path = os.path.join(input_folder, filename)
        img = cv2.imread(img_path)

        # Apply random color adjustments (contrast and brightness)
        contrast = np.random.uniform(0.8, 1.2)  # Mild contrast adjustment
        brightness = np.random.randint(-30, 30) # Mild brightness adjustment
        img = adjust_contrast_brightness(img, contrast, brightness)

        # Convert the processed image to array and apply Keras augmentations
        x = img_to_array(img)
        x = x.reshape((1,) + x.shape)  # Reshape the array to (1, height, width, channels)

        # Generate multiple augmented images using Keras' ImageDataGenerator
        i = 0
        for batch in datagen.flow(x, batch_size=1, save_to_dir=output_folder, save_prefix='aug', save_format='jpg'):
            i += 1
            if i >= 5:  # Set the number of augmented images to generate per input image
                break