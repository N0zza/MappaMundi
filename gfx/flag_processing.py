# This is a file which takes an image or a folder of images and converts them into Paradox-accepted .tga files.
# It will create three folders in the directory which the images are in, one for each flag size, and save them there.
import os
import select
import sys
import time

# MAKE SURE YOUR PILLOW VERSION == 10.2.0
from PIL import Image

# Image sizes of Paradox flags.
FLAG_SIZES = {
    "large": (82, 52),
    "medium": (41, 26),
    "small": (11, 7),
}
# Supported image formats.
VALID_EXTENSIONS = ["png", "jpg", "jpeg", "bmp", "tga", "dds", "tiff"]

def sleep_and_exit(code, seconds=5):
    """Sleeps for 5 seconds and exits the program, to give people time to read."""
    time.sleep(seconds)
    sys.exit(code)

def wait_for_enter_or_timeout(timeout):
    print("Press Enter to quit the program.")
    try:
        ready_objects, _, _ = select.select([sys.stdin], [], [], timeout)
        if ready_objects:
            sys.stdin.readline()
        else:
            pass
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        sys.exit(0)

def convert_image_to_tga(image_path, output_folder):
    """Converts an image to a .tga file and saves it in the output folder.

    Args:
        image_path (str): The path to the image file.
        output_folder (str): The folder to save the .tga file in.
    """
    # Open the image.
    with Image.open(image_path) as img:
        # Convert the image to RGBA.
        img = img.convert("RGBA")
        # Create a .tga file for each flag size.
        for size, dimensions in FLAG_SIZES.items():
            # Resize the image. Bicubic should fit nicely for these scenarios.
            resized_img = img.resize(dimensions, resample=Image.Resampling.BICUBIC)
            # Save the image.
            save_path = os.path.join(output_folder, size) if size != "large" else output_folder
            resized_img.save(os.path.join(save_path, f"{os.path.basename(image_path).split('.')[0]}.tga"), "TGA")

if len(sys.argv) > 2:
    print("No image or folder of images provided. Exiting program.")
    sleep_and_exit(1)

# Get the image or folder of images.
image_path = sys.argv[1]
# Check if the image path exists. If not, quit.
if not os.path.exists(image_path):
    print(f"The image or folder of images '{image_path}' does not exist. Exiting program.")
    # Give the person time to read.
    sleep_and_exit(1)

# Create the 'medium' and 'small' folders.
if os.path.isfile(image_path):
    source_dir = os.path.dirname(image_path)
else:
    source_dir = image_path

flag_dir = os.path.join(source_dir, "flags")

os.makedirs(os.path.join(flag_dir, "medium"), exist_ok=True)
os.makedirs(os.path.join(flag_dir, "small"), exist_ok=True)

# Check if the image path is a file or a folder.
if os.path.isdir(image_path):
    # Get valid image files.
    image_files = [f for f in os.listdir(image_path) if f.split(".")[-1].lower() in VALID_EXTENSIONS]
    # Convert each image to .tga.
    for img in image_files:
        convert_image_to_tga(os.path.join(image_path, img), flag_dir)

    print(f"Images converted to .tga and saved in '{image_path}'.")
elif os.path.isfile(image_path):
    # Check if the file is a valid image.
    if image_path.split(".")[-1].lower() not in VALID_EXTENSIONS:
        print(f"The file '{image_path}' is not a valid image or is not in a valid image format. Exiting program.")
        sleep_and_exit(1)
    # Convert.
    convert_image_to_tga(image_path, flag_dir)
    print(f"Image converted to .tga and saved in '{image_path}'.")

else:
    print("You shouldn't be seeing this. Open an issue in the GitHub repo.")
    sleep_and_exit(1)

# Successful exit.
wait_for_enter_or_timeout(3)