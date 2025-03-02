#!/usr/bin/env python3
# Example usage of MetaClean - Image Metadata Removal Tool

from metadata_remover import display_metadata, remove_metadata, process_directory
import os
import sys
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


# IMPORTANT: Replace this with your own image path
sample_image = "img/iced.jpg"  # ← CHANGE THIS to your own image


def main():
    print("=" * 60)
    print("METACLEAN - IMAGE METADATA REMOVAL TOOL")
    print("=" * 60)

    # Check if the image exists
    if not os.path.exists(sample_image):
        print(f"\nERROR: Image '{sample_image}' not found!")
        print("\nPlease do the following:")
        print("1. Add your images to the 'img' folder")
        print("2. Edit line 9 of this file to point to your image")
        print("   sample_image = \"img/your_photo.jpg\"")
        return

    # Step 1: Display original metadata
    print("\nSTEP 1: VIEWING ORIGINAL METADATA\n")
    display_metadata(sample_image)

    # Step 2: Remove metadata and save to clean folder
    print("\n" + "=" * 60)
    print("STEP 2: REMOVING METADATA")
    print("=" * 60)
    clean_image = remove_metadata(sample_image)

    # Step 3: Verify that metadata was removed
    print("\nSTEP 3: VERIFYING METADATA REMOVAL\n")
    display_metadata(clean_image)

    # Step 4: Process all images in the directory
    print("\n" + "=" * 60)
    print("STEP 4: PROCESSING ALL IMAGES IN FOLDER")
    print("=" * 60)
    image_dir = os.path.dirname(sample_image)
    process_directory(image_dir)

    print("\n" + "=" * 60)
    print("COMPLETED SUCCESSFULLY!")
    print("=" * 60)

    print(f"\nAll clean images saved to: {os.path.dirname(clean_image)}")
    print(f"Example clean image: {clean_image}")


if __name__ == "__main__":
    main()
