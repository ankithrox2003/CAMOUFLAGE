import os
import cv2

# Folder paths
input_folder = "datasetOG"  # Folder containing original images
output_folder = "labeled1"  # Folder to save labeled images
coordinates_folder = "coordinates"  # Folder to save bounding box coordinates

# Create the output and coordinates folder if they don't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
if not os.path.exists(coordinates_folder):
    os.makedirs(coordinates_folder)

# Variables for the bounding box
drawing = False  # True if mouse is pressed
ix, iy = -1, -1  # Initial mouse positions
boxes = []  # List to store bounding box coordinates and classes
current_class = ""  # Store the current selected class
x_end, y_end = -1, -1  # To store the final mouse positions

# Function to draw bounding boxes
def draw_bounding_box(event, x, y, flags, param):
    global ix, iy, drawing, img, x_end, y_end

    # On left mouse button down event, start drawing
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    # On mouse movement, if drawing is True, draw a rectangle on the image
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            img_copy = img.copy()
            cv2.rectangle(img_copy, (ix, iy), (x, y), (0, 255, 0), 2)
            cv2.imshow("Image", img_copy)

    # On left mouse button up event, finalize the rectangle
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        x_end, y_end = x, y
        cv2.rectangle(img, (ix, iy), (x_end, y_end), (0, 255, 0), 2)
        cv2.imshow("Image", img)

# List of image filenames, sorted numerically
image_filenames = sorted(
    [f for f in os.listdir(input_folder) if f.endswith(".png") or f.endswith(".jpg")],
    key=lambda x: int(os.path.splitext(x)[0])  # Assuming filenames are numbers (e.g., 1.jpg, 2.jpg)
)

current_index = 0  # Index of the current image

# Main loop to iterate over images
while current_index < len(image_filenames):
    image_path = os.path.join(input_folder, image_filenames[current_index])
    img = cv2.imread(image_path)
    clone = img.copy()
    boxes = []  # Reset the boxes for the new image
    current_class = ""  # Reset the current class

    # Set up the window and mouse callback function
    cv2.namedWindow("Image")
    cv2.setMouseCallback("Image", draw_bounding_box)

    while True:
        cv2.imshow("Image", img)
        key = cv2.waitKey(1) & 0xFF

        # If 'r' is pressed, reset the image
        if key == ord('r'):
            img = clone.copy()  # Reset the image to original
            boxes = []  # Clear the box list
            current_class = ""  # Clear the current class

        # If 'c' is pressed, save the current image and bounding boxes and break to load the next image
        elif key == ord('c'):
            # Save the labeled image to the output folder
            output_image_path = os.path.join(output_folder, image_filenames[current_index])
            cv2.imwrite(output_image_path, img)

            # Save bounding box coordinates and class to a text file in the 'coordinates' folder
            coordinates_file_path = os.path.join(coordinates_folder, f"{image_filenames[current_index]}_boxes.txt")
            with open(coordinates_file_path, "w") as f:
                # Write the image filename first
                f.write(f"Image: {image_filenames[current_index]}\n")
                for box in boxes:
                    f.write(f"{box[0]}, {box[1]}, {box[2]}, {box[3]}, {box[4]}\n")

            break  # Break to load the next image

        # Choose class for bounding box: P for person, T for tank, W for weapons, S for suspect
        elif key == ord('p'):
            current_class = "person"
        elif key == ord('t'):
            current_class = "tank"
        elif key == ord('w'):
            current_class = "weapons"
        elif key == ord('s'):
            current_class = "suspect"

        # If class is selected and a bounding box is drawn, save it
        elif key == 13 and current_class != "" and ix != -1 and iy != -1 and x_end != -1 and y_end != -1:  # Enter key to save the bounding box
            boxes.append((ix, iy, x_end, y_end, current_class))  # Save the box coordinates and class
            current_class = ""  # Reset the class after saving

            # Redraw bounding boxes with their labels
            img = clone.copy()
            for box in boxes:
                cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
                cv2.putText(img, box[4], (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

        # Handle 'k' for previous image and 'j' for next image
        elif key == ord('k'):  # Previous image
            if current_index > 0:  # Prevent going out of bounds
                current_index -= 1
                break  # Break to load the previous image
        elif key == ord('j'):  # Next image
            if current_index < len(image_filenames) - 1:  # Prevent going out of bounds
                current_index += 1
                break  # Break to load the next image

    # Close the image window after processing
    cv2.destroyAllWindows()

print("Labeling completed. Labeled images and bounding boxes are saved in the output folder. Coordinates are saved in the coordinates folder.")
