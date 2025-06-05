# -*- coding: utf-8 -*-
"""
This script can be integrated towards generating QR codes of different types based on the data fed into the script.
The previous script allows creation of data towards this task.
The QR codes can further be encrypted and decrypted depending on user needs.
"""

import os
import qrcode
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import random
import math
import pandas as pd

# Generate a random sequence of single digits
def generate_random_single_digit_sequence(length):
    return np.random.randint(0, 9, size=length).tolist()

# Function to save selected digits from a sequence
def save_selected_digits(sequence, start_index=3, end_index=7):
    selected_digits = sequence[start_index:end_index]
    return ''.join(map(str, selected_digits))

# Function to save the QR code image with a filename based on selected digits
def save_qr_code(qr_image, sequence, folder="Output/QRs"):
    if not os.path.exists(folder):
        os.makedirs(folder)
    filename = f"{folder}/{''.join(map(str, sequence[3:7]))}.png"
    qr_image.save(filename)
    return filename

# Generate unique dotted pattern background
def generate_unique_dotted_pattern(bg_size, dot_radius=1, min_opacity=25, max_opacity=100):
    pattern_img = Image.new('RGBA', (bg_size, bg_size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(pattern_img)
    for y in range(0, bg_size, 2):
        for x in range(0, bg_size, 2):
            if random.random() < 0.5:
                x_offset = random.randint(-3, 3)
                y_offset = random.randint(-3, 3)
                random_opacity = random.randint(min_opacity, max_opacity)
                dot_color = (255, 0, 0, random_opacity)  # Red dots (adjusted)
                draw.ellipse([(x + x_offset - dot_radius, y + y_offset - dot_radius),
                              (x + x_offset + dot_radius, y + y_offset + dot_radius)], fill=dot_color)
    return pattern_img

# Create radial gradient background
def create_radial_gradient(bg_size, center_color=(255, 255, 204), edge_color=(255, 255, 153)):
    gradient_img = Image.new('RGB', (bg_size, bg_size))
    draw = ImageDraw.Draw(gradient_img)
    max_radius = math.sqrt(2) * bg_size / 2
    for y in range(bg_size):
        for x in range(bg_size):
            dx = x - bg_size / 2
            dy = y - bg_size / 2
            distance_from_center = math.sqrt(dx**2 + dy**2)
            normalized_distance = distance_from_center / max_radius
            normalized_distance = max(0, min(normalized_distance, 1))
            r = int(center_color[0] + (edge_color[0] - center_color[0]) * normalized_distance)
            g = int(center_color[1] + (edge_color[1] - center_color[1]) * normalized_distance)
            b = int(center_color[2] + (edge_color[2] - center_color[2]) * normalized_distance)
            draw.point((x, y), fill=(r, g, b))
    return gradient_img

# Generate random dots on QR
def generate_random_dots_on_qr(qr_img, dot_radius=1, min_opacity=1, max_opacity=30, dot_count=150):
    draw = ImageDraw.Draw(qr_img)
    for _ in range(dot_count):
        x = random.randint(10, qr_img.width-10)
        y = random.randint(10, qr_img.height-10)
        random_opacity = random.randint(min_opacity, max_opacity)
        dot_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random_opacity)
        draw.ellipse([(x - dot_radius, y - dot_radius), (x + dot_radius, y + dot_radius)], fill=dot_color)
    return qr_img


# Function to calculate the best QR code version based on qr_size in mm
def calculate_qr_version(qr_size_mm):
    # QR code versions range from 1 to 40
    # Approximate range of sizes in mm for versions 1 to 40
    min_qr_size = 21  # Version 1 has 21 modules, approximately 21mm
    max_qr_size = 177  # Version 40 has 177 modules, approximately 177mm
    
    # Calculate the corresponding version for the given qr_size_mm
    if qr_size_mm < min_qr_size:
        return 1
    elif qr_size_mm > max_qr_size:
        return 40
    else:
        # Linear interpolation to determine the version between 1 and 40
        version = math.ceil((qr_size_mm - min_qr_size) / (max_qr_size - min_qr_size) * 39) + 1
        return min(max(version, 1), 40)  # Ensure version is between 1 and 40


# Main function to generate custom QR code with dotted pattern and gradient background
def generate_custom_qr_with_dotted_pattern(qr_key, sequence, qr_version=10, qr_size=118, padding_ratio=0.2, dot_radius=0.2, min_opacity=1, max_opacity=50, qroption="With Background"):
    # Ensure qr_size is an integer
    qr_size = int(qr_size)

    # Dynamically adjust bg_size and padding based on qr_size
    padding = int(qr_size * padding_ratio)
    bg_size = qr_size + 2 * padding
    dot_count = int(qr_size * 1.5)  # Example: dot count is proportional to QR size

    qr = qrcode.QRCode(version=qr_version, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=2)
    qr.add_data(qr_key)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB').resize((qr_size, qr_size))

    qr_position = (padding, padding)

    if qroption == "With Background":
        # Generate gradient background with dots
        gradient_bg = create_radial_gradient(bg_size)
        bg_img = gradient_bg.convert('RGBA')
        dotted_pattern = generate_unique_dotted_pattern(bg_size, dot_radius, min_opacity, max_opacity)
        bg_img = Image.alpha_composite(bg_img, dotted_pattern)
    else:
        # Plain white background
        bg_img = Image.new('RGBA', (bg_size, bg_size), (255, 255, 255, 255))

    # Add the sequence as multiple overlapping vertical lines on the right side of the QR code
    font_size = 4  # Reduce the font size further
    try:
        small_font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        small_font = ImageFont.load_default()

    text_layer = Image.new('RGBA', (bg_size, bg_size), (255, 255, 255, 0))
    text_draw = ImageDraw.Draw(text_layer)

    # Calculate the width of one digit for positioning
    digit_width, text_height = text_draw.textsize('0', font=small_font)
    vertical_spacing = font_size  # Adjust spacing between each digit to reduce readability
    light_red_color = (255, 0, 0)
    alpha_value = 75

    # Draw 5 overlapping lines of the repeated sequence
    num_lines = 5
    overlap_fraction = 0.5
    initial_x_position = qr_position[0] + qr_size + 5

    for line_index in range(num_lines):
        x_position = initial_x_position + int(line_index * digit_width * (1 - overlap_fraction))
        y_position = qr_position[1]

        # Draw each digit from the sequence individually down the right side
        for _ in range(3):  # Repeat drawing the sequence 3 times to fill the height
            for number in sequence:
                text_draw.text((x_position, y_position), str(number), font=small_font, fill=(light_red_color[0], light_red_color[1], light_red_color[2], alpha_value))  # Light grey color
                y_position += vertical_spacing

    bg_img = Image.alpha_composite(bg_img, text_layer)

    qr_img_with_dots = generate_random_dots_on_qr(qr_img.copy(), dot_radius, min_opacity, max_opacity, dot_count)

    bg_img.paste(qr_img_with_dots, qr_position)

    return bg_img

# Process Excel file to generate QR codes
def process_excel_and_generate_qr(excel_path, output_path="Output/QR_Keys_Info.xlsx"):
    df = pd.read_excel(excel_path)
    qr_key_data = []
    for index, row in df.iterrows():
        qr_size_mm = row['qrsize']
        qroption = row['qroption']

        # Calculate the best-fit QR code version for the given size
        qr_version = calculate_qr_version(qr_size_mm)

        sequence = generate_random_single_digit_sequence(10)
        qr_key = save_selected_digits(sequence)
        print(f"Row {index} Key:", qr_key)

        # Generate custom QR code using parameters from the excel sheet
        custom_qr = generate_custom_qr_with_dotted_pattern(qr_key, sequence, qr_version=qr_version, qr_size=118, qroption=qroption)

        # Save QR code image
        qr_filename = save_qr_code(custom_qr, sequence)
        print(f"✅ Row {index} - Saved QR Code as:", qr_filename)

        # Store QR key and row data in the list
        qr_key_data.append([qr_key] + row.values.tolist())

    # Create a new DataFrame for the QR keys and row data
    qr_key_df = pd.DataFrame(qr_key_data, columns=["QR_Key"] + df.columns.tolist())

    # Save the new DataFrame to an Excel file
    qr_key_df.to_excel(output_path, index=False)
    print(f"📁 QR Keys and data saved to {output_path}")

# Set Excel file path and process it to generate QR codes and save the keys
excel_path = "Output/dataQR.xlsx"
process_excel_and_generate_qr(excel_path)
