#!/usr/bin/env python3
# MetaClean - Image Quality Comparison Tool
# Compare the visual quality of original and cleaned images

import os
import sys
from PIL import Image
import numpy as np


def compare_images(original_path, cleaned_path):
    """Compare two images and calculate the difference"""
    if not os.path.exists(original_path):
        print(f"Error: Original image '{original_path}' not found.")
        return

    if not os.path.exists(cleaned_path):
        print(f"Error: Cleaned image '{cleaned_path}' not found.")
        return

    try:
        original = Image.open(original_path)
        cleaned = Image.open(cleaned_path)

        # Check if images have the same dimensions
        if original.size != cleaned.size:
            print(f"Error: Images have different dimensions")
            print(f"Original: {original.size}, Cleaned: {cleaned.size}")
            return

        # Convert to numpy arrays
        original_array = np.array(original)
        cleaned_array = np.array(cleaned)

        # Calculate differences
        if original_array.shape == cleaned_array.shape:
            # Calculate Mean Squared Error (MSE)
            mse = np.mean((original_array - cleaned_array) ** 2)

            # Calculate Peak Signal-to-Noise Ratio (PSNR)
            if mse == 0:
                psnr = float('inf')
            else:
                max_pixel = 255.0
                psnr = 20 * np.log10(max_pixel / np.sqrt(mse))

            # Calculate basic statistics
            mean_original = np.mean(original_array)
            mean_cleaned = np.mean(cleaned_array)
            std_original = np.std(original_array)
            std_cleaned = np.std(cleaned_array)

            print("\n" + "=" * 60)
            print("IMAGE QUALITY COMPARISON")
            print("=" * 60)

            print(
                f"\nComparing: {os.path.basename(original_path)} vs {os.path.basename(cleaned_path)}")
            print(f"\nQuality Metrics:")
            print(f"- Mean Squared Error: {mse:.2f} (lower is better)")
            print(f"- Signal-to-Noise Ratio: {psnr:.2f} dB (higher is better)")

            print(f"\nImage Statistics:")
            print(f"- Original Mean Pixel Value: {mean_original:.2f}")
            print(f"- Cleaned Mean Pixel Value: {mean_cleaned:.2f}")
            print(f"- Original Standard Deviation: {std_original:.2f}")
            print(f"- Cleaned Standard Deviation: {std_cleaned:.2f}")

            print("\n" + "=" * 60)
            print("RESULTS")
            print("=" * 60)

            if psnr > 30:
                print("\n✓ The images are visually identical - quality preserved!")
            elif psnr > 20:
                print(
                    "\n✓ The images have minor differences but are still very similar.")
            else:
                print("\n⚠ The images have noticeable differences.")
        else:
            print(f"Error: Images have different shapes")
            print(
                f"Original shape: {original_array.shape}, Cleaned shape: {cleaned_array.shape}")
    except Exception as e:
        print(f"Error comparing images: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("\n" + "=" * 60)
        print("METACLEAN - IMAGE QUALITY COMPARISON TOOL")
        print("=" * 60)
        print("\nThis tool compares your original image with the cleaned version")
        print("to verify that no quality was lost during metadata removal.")
        print("\nUsage:")
        print("python compare_images.py <original_image> <cleaned_image>")
        print("\nExample:")
        print("python compare_images.py img/photo.jpg img/clean/photo.jpg")
        sys.exit(1)

    original_path = sys.argv[1]
    cleaned_path = sys.argv[2]

    compare_images(original_path, cleaned_path)
