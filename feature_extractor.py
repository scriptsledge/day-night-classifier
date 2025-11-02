import os
import numpy as np
from PIL import Image
from skimage.color import rgb2hsv

def calculate_features(image_path):
    """
    Calculates the 4 features for a single image.
    """
    try:
        img = Image.open(image_path).convert('RGB')
        img_array = np.array(img)

        # 1. Grayscale features
        gray_img = img.convert('L')
        gray_array = np.array(gray_img)
        brightness = gray_array.mean()
        contrast = gray_array.std()

        # 2. HSV features
        hsv_array = rgb2hsv(img_array)
        colorfulness = hsv_array[:, :, 1].mean()  # Mean of the saturation channel
        color_variety = hsv_array[:, :, 0].std()   # Std dev of the hue channel

        return brightness, contrast, colorfulness, color_variety
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None, None, None, None

def main():
    """
    Main function to process all images and print features.
    """
    image_dir = 'dataset'
    
    # Get a sorted list of image files
    try:
        image_files = sorted([f for f in os.listdir(image_dir) if f.endswith('.jpg')])
    except FileNotFoundError:
        print(f"Error: Directory not found at '{image_dir}'")
        return

    # Print CSV header
    print("ImageName,brightness,contrast,colorfulness,color_variety")

    # Process each image
    for image_file in image_files:
        image_path = os.path.join(image_dir, image_file)
        features = calculate_features(image_path)
        if all(f is not None for f in features):
            print(f"{image_file},{features[0]},{features[1]},{features[2]},{features[3]}")

if __name__ == '__main__':
    main()
