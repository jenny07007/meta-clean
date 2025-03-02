#!/usr/bin/env python3
# Setup script for MetaClean - Image Metadata Removal Tool

import os
import sys
import subprocess

print("\n" + "=" * 60)
print("METACLEAN - IMAGE METADATA REMOVAL TOOL SETUP")
print("=" * 60)

print("\nInstalling required packages...")
try:
    subprocess.check_call([sys.executable, "-m", "pip",
                          "install", "pillow", "piexif", "exifread", "numpy"])
    print("✓ All packages installed successfully")
except Exception as e:
    print(f"✗ Error installing packages: {e}")
    print("Please run this command manually:")
    print("pip install pillow piexif exifread numpy")


print("\nCreating necessary folders...")
if not os.path.exists("img"):
    os.makedirs("img")
    print("✓ Created 'img' folder")
else:
    print("✓ 'img' folder already exists")

if not os.path.exists(os.path.join("img", "clean")):
    os.makedirs(os.path.join("img", "clean"))
    print("✓ Created 'img/clean' folder")
else:
    print("✓ 'img/clean' folder already exists")


print("\n" + "=" * 60)
print("SETUP COMPLETE - NEXT STEPS")
print("=" * 60)
print("\n1. Add your images to the 'img' folder")
print("2. Edit example_usage.py to use your image:")
print("   - Open example_usage.py")
print("   - Change line 9 to point to your image")
print("   - Example: sample_image = \"img/your_photo.jpg\"")
print("\n3. Run the example:")
print("   python example_usage.py")
print("\nThat's it! Your clean images will be saved to the 'img/clean' folder.")
