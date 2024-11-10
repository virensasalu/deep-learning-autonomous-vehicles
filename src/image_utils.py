import cv2
import matplotlib.pyplot as plt

def load_image(file_path):
    """
    Load an image from file.
    
    Parameters:
        file_path (str): Path to the image file.

    Returns:
        np.ndarray: Loaded image.
    """
    image = cv2.imread(file_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB for Matplotlib
    return image

def display_image(image):
    """Display an image using Matplotlib."""
    plt.imshow(image)
    plt.axis('off')
    plt.show()

# Testing the functions in image_utils.py itself
if __name__ == "__main__":
    # Path to an image
    image_path = './data/2011_09_26_drive_0009_extract/image_00/data/0000000122.png'  # Adjust the path if necessary
    image = load_image(image_path)
    display_image(image)