import cv2
import sys
import time

def print_usage():
    usage_text = """
    Usage: python script.py <image_path>
    
    Description:
    ------------
    This script allows interactive cropping of an image using OpenCV. You can move a cropping square around the image
    using the mouse and dynamically resize the square using the `f` and `d` keys. The script also provides functionality to 
    zoom in and out of the cropping area and save the cropped image with a unique filename.

    Arguments:
    ----------
    <image_path> : The path to the image file you want to crop. The image must be in a format readable by OpenCV (e.g., JPEG, PNG).

    Controls:
    ---------
    - Mouse Movement: Move the cropping square around the image.
    - 'f' Key: Zoom in (increase the size of the cropping square).
    - 'd' Key: Zoom out (decrease the size of the cropping square).
    - 'a' Key: Preview the currently selected cropped area.
    - 's' Key: Save the current preview of the cropped area.
    - 'c' Key: Crop the image at the current selection and save it with a unique filename.
    - 'q' Key: Quit the application.

    """
    print(usage_text)

# Check if the image path is provided as a command-line argument or if help is requested
if len(sys.argv) < 2 or sys.argv[1] in ['-h', '--help']:
    print_usage()
    sys.exit(1)

# Load the image from the provided path
image_path = sys.argv[1]
image = cv2.imread(image_path)

if image is None:
    print(f"Error: Could not load image at {image_path}")
    sys.exit(1)

# Initial parameters
crop_size = 512
min_crop_size = 50
max_crop_size = min(image.shape[0], image.shape[1])  # Ensure the max crop size does not exceed image dimensions
x_start, y_start = 0, 0  # Initial position of the cropping window

# Function to update the cropping window based on mouse movement
def update_crop(event, x, y, flags, param):
    global x_start, y_start

    if event == cv2.EVENT_MOUSEMOVE:
        # Center the crop window around the mouse pointer
        x_start = max(0, min(x - crop_size // 2, image.shape[1] - crop_size))
        y_start = max(0, min(y - crop_size // 2, image.shape[0] - crop_size))
        draw_crop_window()

def draw_crop_window():
    # Copy the image to draw the cropping rectangle on
    temp_image = image.copy()

    # Draw the cropping rectangle
    cv2.rectangle(temp_image, (x_start, y_start), (x_start + crop_size, y_start + crop_size), (0, 255, 0), 2)

    # Display the updated image
    cv2.imshow("Image Cropper", temp_image)

def generate_unique_filename(base_name="cropped_image", extension=".png"):
    # Generate a unique filename using the current timestamp
    timestamp = int(time.time() * 1000)  # Milliseconds since epoch
    return f"{base_name}_{timestamp}{extension}"

# Create a window and set a mouse callback function
cv2.namedWindow("Image Cropper")
cv2.setMouseCallback("Image Cropper", update_crop)

# Main loop to keep the window open and respond to keypresses
while True:
    draw_crop_window()
    key = cv2.waitKey(1) & 0xFF

    # Press 'f' to zoom in (increase cropping square size)
    if key == ord("f"):
        crop_size = min(crop_size + 20, max_crop_size)  # Increase the crop size, but do not exceed max size

    # Press 'd' to zoom out (decrease cropping square size)
    elif key == ord("d"):
        crop_size = max(crop_size - 20, min_crop_size)  # Decrease the crop size, but do not go below min size

    elif key == ord("a"):
        cropped_image = image[y_start:y_start + crop_size, x_start:x_start + crop_size]
        cv2.imshow("Cropped Image", cropped_image)

    elif key == ord("s"):
        filename = generate_unique_filename()
        cv2.imwrite(filename, cropped_image)
        print(f"Cropped image saved as {filename}")

    # Press 'c' to crop the image
    elif key == ord("c"):
        cropped_image = image[y_start:y_start + crop_size, x_start:x_start + crop_size]
        cv2.imshow("Cropped Image", cropped_image)

        filename = generate_unique_filename()
        cv2.imwrite(filename, cropped_image)
        print(f"Cropped image saved as {filename}")

    # Press 'q' to exit the program
    elif key == ord("q"):
        break

# Close all windows
cv2.destroyAllWindows()

