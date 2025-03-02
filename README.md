<!-- markdownlint-disable-->

# MetaClean - Image Metadata Removal Tool

MetaClean is a simple Python tool that removes all embedded metadata from images without affecting their quality. I created this because I wanted a way to clean my image metadata before uploading them to the internet, without relying on online tools that might compromise privacy 😉

## Features

- Remove all metadata (EXIF, GPS, camera info, etc.) from images
- Preserve image quality during the cleaning process
- Process individual images or entire directories
- View metadata before removal
- Support for multiple image formats (JPEG, PNG, TIFF, etc.)

## Installation

### Prerequisites

- Python 3.6 or higher

### Setup

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

Or let the script install dependencies automatically when you run it for the first time.

## Usage

### Quick Start

1. Add your images to the `img` folder
2. Edit `example_usage.py` to point to your image:
   ```python
   sample_image = "img/your_photo.jpg"  # Change this to your image path
   ```
3. Run the example script:
   ```bash
   python example_usage.py
   ```

### Command Line Usage

You can also use the tool directly from the command line:

```bash
# View metadata without removing it
python metadata_remover.py --input img/your_photo.jpg --view

# Remove metadata from a single image
python metadata_remover.py --input img/your_photo.jpg

# Process all images in a directory
python metadata_remover.py --input img/
```

## Output

All cleaned images are saved to an `img/clean/` directory by default, preserving the original files.

## Dependencies

- Pillow: For image processing
- piexif: For EXIF data handling
- ExifRead: For detailed metadata reading

## License

This project is open source and available under the MIT License.
