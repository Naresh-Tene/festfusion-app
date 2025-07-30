#!/usr/bin/env python3
"""
Create a test image for testing the upload functionality
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_test_image():
    """Create a simple test image"""
    # Create a 300x200 image with a white background
    img = Image.new('RGB', (300, 200), color='white')
    draw = ImageDraw.Draw(img)
    
    # Add some text to make it look like a festival image
    try:
        # Try to use a default font
        font = ImageFont.load_default()
    except:
        font = None
    
    # Draw some text
    text = "Test Festival Image"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Center the text
    x = (300 - text_width) // 2
    y = (200 - text_height) // 2
    
    # Draw the text
    draw.text((x, y), text, fill='black', font=font)
    
    # Add a border
    draw.rectangle([0, 0, 299, 199], outline='red', width=3)
    
    # Save the image
    filename = "test_festival_image.jpg"
    img.save(filename, "JPEG")
    print(f"✅ Created test image: {filename}")
    print(f"📁 File size: {os.path.getsize(filename)} bytes")
    
    return filename

if __name__ == "__main__":
    create_test_image() 