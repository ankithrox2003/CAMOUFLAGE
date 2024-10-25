import os
from PIL import Image

# Folder containing the images
folder_path = "MOD"  # Replace with your folder path

# Iterate over files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".jpeg"):  # Check for .jpeg files
        # Full path of the image
        img_path = os.path.join(folder_path, filename)
        
        # Open the image
        img = Image.open(img_path)
        
        # Convert and save as .jpg
        new_filename = filename.replace(".jpeg", ".jpg")  # Change extension
        new_img_path = os.path.join(folder_path, new_filename)
        img.save(new_img_path, "JPEG")
        
        # Optionally remove the original .jpeg file
        os.remove(img_path)
        print(f"Converted {filename} to {new_filename}")

print("Conversion completed!")
