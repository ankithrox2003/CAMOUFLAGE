import os

def rename_images(folder_path):
    # List all files in the directory
    files = os.listdir(folder_path)
    
    # Filter only image files (you can add more extensions as needed)
    image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
    
    # Sort files to maintain order
    image_files.sort()
    
    for index, filename in enumerate(image_files, start=1):
        # Define new filename
        new_name = f"{index}.jpg"
        # Construct full file paths
        old_file = os.path.join(folder_path, filename)
        new_file = os.path.join(folder_path, new_name)
        
        # Rename the file
        os.rename(old_file, new_file)
        print(f'Renamed: {old_file} to {new_file}')

# Example usage
folder_path = 'datasetOG'  # Replace with your folder path
rename_images(folder_path)
