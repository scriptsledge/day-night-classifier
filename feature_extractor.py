import os
import numpy as np
from PIL import Image
from skimage.color import rgb2hsv
import sys

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
    Main function to process all images and save features to CSV for manual labeling.
    """
    image_dir = 'dataset'
    output_file = 'feature_table.csv'
    
    # Check if dataset exists
    if not os.path.exists(image_dir):
        print(f"Error: Directory '{image_dir}' not found.")
        sys.exit(1)

    image_files = sorted([f for f in os.listdir(image_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
    
    if not image_files:
        print(f"No images found in '{image_dir}'.")
        sys.exit(1)

    print(f"Processing {len(image_files)} images...")

    with open(output_file, 'w') as f:
        # Write CSV header
        f.write("ImageName,brightness,contrast,colorfulness,color_variety,Class\n")

        # Process each image
        for image_file in image_files:
            image_path = os.path.join(image_dir, image_file)
            features = calculate_features(image_path)
            
            if all(feat is not None for feat in features):
                # We intentionally leave the Class column empty for the user to fill
                f.write(f"{image_file},{features[0]:.4f},{features[1]:.4f},{features[2]:.4f},{features[3]:.4f},\n")
    
    print("-" * 50)
    print(f"✅ Success! Features extracted to '{output_file}'.")
    print("-" * 50)
    print("🎓 EDUCATIONAL STEP REQUIRED:")
    print("1. Open 'feature_table.csv' in Excel, Sheets, or a text editor.")
    print("2. Look at the images in the 'dataset/' folder.")
    print("3. Manually fill in the 'Class' column with either 'Day' or 'Night'.")
    print("   (Check README.md if you are in a hurry for the cheat sheet!)")
    print("4. Save the file.")
    print("5. Run 'train_and_save_model.py'.")
    print("-" * 50)

if __name__ == '__main__':
    main()
