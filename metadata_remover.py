#!/usr/bin/env python3
# MetaClean - Image Metadata Removal Tool
# This tool removes all embedded metadata from images without affecting their quality.

from datetime import datetime
import exifread
import piexif
from PIL import Image
import os
import sys
import glob
import subprocess
import importlib.util

# Check for required dependencies
required_packages = ['PIL', 'piexif', 'exifread']
missing_packages = []

for package in required_packages:
    # For PIL, we need to check for Pillow
    if package == 'PIL':
        package_name = 'Pillow'
        module_name = 'PIL'
    else:
        package_name = package
        module_name = package

    if importlib.util.find_spec(module_name) is None:
        missing_packages.append(package_name)

# If there are missing packages, inform the user and offer to install them
if missing_packages:
    print("=" * 60)
    print("METACLEAN - MISSING DEPENDENCIES")
    print("=" * 60)
    print(
        f"\nThe following required packages are missing: {', '.join(missing_packages)}")
    print("\nYou can install them using pip:")
    print(f"pip install {' '.join(missing_packages)}")
    print("\nOr install all dependencies at once using the requirements.txt file:")
    print("pip install -r requirements.txt")

    # Ask if the user wants to install the dependencies automatically
    try:
        install = input(
            "\nWould you like to install the missing dependencies now? (y/n): ")
        if install.lower() == 'y':
            print("\nInstalling missing dependencies...")
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
                print("Dependencies installed successfully!")
                # Continue with the script after installing
            except subprocess.CalledProcessError:
                print("Failed to install dependencies. Please install them manually.")
                sys.exit(1)
        else:
            print("Please install the dependencies manually and run the script again.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\nInstallation cancelled. Please install the dependencies manually.")
        sys.exit(1)


def display_metadata(image_path):
    """Display all metadata in an image file"""
    print(f"Metadata for: {os.path.basename(image_path)}\n")

    # Using exifread to get detailed metadata
    with open(image_path, 'rb') as f:
        tags = exifread.process_file(f, details=True)

    if not tags:
        print("No metadata found.")
        return

    # Print all metadata tags
    for tag, value in tags.items():
        print(f"{tag}: {value}")

    print(f"\nTotal metadata tags found: {len(tags)}")


def remove_metadata(input_path, output_path=None):
    """Remove all metadata from an image and save it to a new file"""
    try:
        # If no output path is specified, create one in the img/clean directory
        if output_path is None:
            # Get the base filename
            base_filename = os.path.basename(input_path)

            # Create the output directory if it doesn't exist
            output_dir = os.path.join(os.path.dirname(input_path), "clean")
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Set the output path to be in the clean directory
            output_path = os.path.join(output_dir, base_filename)

        # Open the image
        img = Image.open(input_path)

        # Extract image format and mode
        img_format = img.format
        img_mode = img.mode

        if img_format == 'JPEG':
            # Create a new image with the same content but without metadata
            data = list(img.getdata())
            image_without_exif = Image.new(img_mode, img.size)
            image_without_exif.putdata(data)

            # Use maximum quality settings to ensure no quality loss
            image_without_exif.save(output_path, format=img_format, quality=100,
                                    subsampling=0, optimize=True)
        else:
            # For other formats, copy the image and remove EXIF data
            # This preserves all image attributes except metadata
            image_without_exif = img.copy()

            # Save with appropriate format-specific settings for maximum quality
            if img_format == 'PNG':
                image_without_exif.save(output_path, format=img_format,
                                        optimize=True, compress_level=0)  # No compression for max quality
            elif img_format == 'TIFF':
                image_without_exif.save(output_path, format=img_format,
                                        compression=None)  # No compression for max quality
            else:
                # For other formats, use highest quality settings
                image_without_exif.save(output_path, format=img_format)

        print(
            f"Metadata removed successfully. Clean image saved to: {output_path}")
        return output_path

    except Exception as e:
        print(f"Error removing metadata: {e}")
        return None


def process_directory(input_dir, output_dir=None):
    """Process all images in a directory to remove metadata"""
    # Always use a 'clean' subdirectory within the input directory
    output_dir = os.path.join(input_dir, "clean")

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Get all image files
    image_extensions = ['.jpg', '.jpeg', '.png', '.tiff', '.bmp', '.gif']
    image_files = []

    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(input_dir, f"*{ext}")))
        image_files.extend(
            glob.glob(os.path.join(input_dir, f"*{ext.upper()}")))

    # Filter out any files that are already in the clean directory
    image_files = [f for f in image_files if os.path.dirname(f) != output_dir]

    if not image_files:
        print(f"No image files found in {input_dir}")
        return

    print(f"Found {len(image_files)} image files to process.")

    # Process each image
    processed_files = []
    for img_path in image_files:
        filename = os.path.basename(img_path)
        output_path = os.path.join(output_dir, filename)
        result = remove_metadata(img_path, output_path)
        if result:
            processed_files.append(result)

    print(
        f"\nProcessed {len(processed_files)} images. Clean images saved to: {output_dir}")
    return processed_files


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="MetaClean - Remove metadata from images without affecting quality")
    parser.add_argument("--input", "-i", required=True,
                        help="Input image file or directory")
    parser.add_argument(
        "--output", "-o", help="Output image file or directory (optional)")
    parser.add_argument("--view", "-v", action="store_true",
                        help="View metadata without removing it")

    args = parser.parse_args()

    if os.path.isdir(args.input):
        if args.view:
            print("Viewing metadata for all images in directory is not supported.")
            print("Please specify a single image file with --view option.")
            return
        process_directory(args.input, args.output)
    elif os.path.isfile(args.input):
        if args.view:
            display_metadata(args.input)
        else:
            remove_metadata(args.input, args.output)
    else:
        print(f"Error: {args.input} is not a valid file or directory.")


if __name__ == "__main__":
    main()
