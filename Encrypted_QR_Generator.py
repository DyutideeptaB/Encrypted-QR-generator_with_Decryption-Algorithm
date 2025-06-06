# -*- coding: utf-8 -*-
"""
This script is for QR Code generation with encrypted Identifiers and JSON Storage
The following can be decrypted using the decryption algorithm script.
"""

import os
import qrcode
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import random
import math
import pandas as pd
from cryptography.fernet import Fernet
import json

# Function to generate and save an encryption key (only needed once)
def generate_encryption_key(key_folder="keys"):
    if not os.path.exists(key_folder):
        os.makedirs(key_folder)
    key = Fernet.generate_key()
    with open(os.path.join(key_folder, "encryption_key.key"), "wb") as key_file:
        key_file.write(key)
    return key

# Load all encryption keys from a folder
def load_possible_keys(key_folder="keys"):
    keys = []
    if not os.path.exists(key_folder):
        raise FileNotFoundError(f"Key folder '{key_folder}' not found.")
    
    for file in os.listdir(key_folder):
        if file.endswith(".key"):
            with open(os.path.join(key_folder, file), "rb") as f:
                keys.append(f.read())
    return keys

# Encrypt the unique identifier and return as a string
def encrypt_identifier(identifier, fernet):
    encrypted_id = fernet.encrypt(identifier.encode())
    return encrypted_id.decode()  # Convert bytes to string for JSON compatibility

# Save row information and encrypted identifier mapping in JSON format
def save_row_information(encrypted_id, row_data, storage_file="Row_Info.json"):
    # Load existing data or create a new dictionary if file doesn't exist
    if os.path.exists(storage_file):
        with open(storage_file, "r") as file:
            data = json.load(file)
    else:
        data = {}

    # Store encrypted identifier as key and row data as value
    data[encrypted_id] = row_data

    # Save updated data back to the JSON file
    with open(storage_file, "w") as file:
        json.dump(data, file, indent=4)  # Use indent for readability

# Function to save selected digits from a sequence to a text file
def save_selected_digits(sequence, start_index=18, end_index=22, filename="QR_Keys.txt", folder="Output"):
    # Create folder if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Select specific digits from the sequence
    selected_digits = sequence[start_index:end_index]
    full_path = os.path.join(folder, filename)

    # Append the selected digits to a text file
    with open(full_path, 'a') as file:
        file.write(','.join(map(str, selected_digits)) + '\n')

    return selected_digits

# Function to save the QR code image with a filename based on selected digits
def save_qr_code(qr_image, sequence, folder="Output/Encrypted_QRs"):
    # Create folder if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Define the filename based on selected digits from the sequence
    filename = f"{folder}/{''.join(map(str, sequence[18:22]))}.png"
    qr_image.save(filename)
    return filename

# Generate a unique dotted pattern background with random dot colors and positions
def generate_unique_dotted_pattern(bg_size, dot_radius=1, min_opacity=50, max_opacity=150):
    pattern_img = Image.new('RGBA', (bg_size, bg_size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(pattern_img)

    # Place dots randomly across the background
    for y in range(0, bg_size, 2):
        for x in range(0, bg_size, 2):
            if random.random() < 0.5:
                x_offset = random.randint(-3, 3)
                y_offset = random.randint(-3, 3)
                random_opacity = random.randint(min_opacity, max_opacity)
                dot_color = (255, 182, 193, random_opacity)  # Light red dots with varying opacity
                draw.ellipse([(x + x_offset - dot_radius, y + y_offset - dot_radius),
                              (x + x_offset + dot_radius, y + y_offset + dot_radius)], fill=dot_color)
    return pattern_img

# Create a radial gradient background centered around the QR code
def create_radial_gradient_from_qr_edges(bg_size, qr_size, qr_position, center_color=(255, 255, 204), edge_color=(255, 255, 153)):
    gradient_img = Image.new('RGB', (bg_size, bg_size))
    draw = ImageDraw.Draw(gradient_img)

    # Calculate the center and maximum radius for gradient effect
    qr_center = (qr_position[0] + qr_size // 2, qr_position[1] + qr_size // 2)
    max_radius = math.sqrt(2) * bg_size / 2

    # Generate gradient color at each pixel
    for y in range(bg_size):
        for x in range(bg_size):
            dx = x - qr_center[0]
            dy = y - qr_center[1]
            distance_from_qr_center = math.sqrt(dx**2 + dy**2)

            # Apply gradient effect outside the QR code area
            if qr_position[0] <= x <= qr_position[0] + qr_size and qr_position[1] <= y <= qr_position[1] + qr_size:
                draw.point((x, y), fill="white")
            else:
                normalized_distance = (distance_from_qr_center - qr_size / 2) / (max_radius - qr_size / 2)
                normalized_distance = max(0, min(normalized_distance, 1))
                r = int(center_color[0] + (edge_color[0] - center_color[0]) * normalized_distance)
                g = int(center_color[1] + (edge_color[1] - center_color[1]) * normalized_distance)
                b = int(center_color[2] + (edge_color[2] - center_color[2]) * normalized_distance)
                draw.point((x, y), fill=(r, g, b))
    return gradient_img

# Add random dots on top of the QR code for visual interest
def generate_random_dots_on_qr(qr_img, dot_radius=1, min_opacity=25, max_opacity=150, dot_count=100):
    draw = ImageDraw.Draw(qr_img)
    for _ in range(dot_count):
        x = random.randint(0, qr_img.width)
        y = random.randint(0, qr_img.height)
        random_opacity = random.randint(min_opacity, max_opacity)
        dot_color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
            random_opacity
        )
        draw.ellipse([(x - dot_radius, y - dot_radius), (x + dot_radius, y + dot_radius)], fill=dot_color)
    return qr_img

# Main function to generate custom QR code with a dotted pattern and gradient background
def generate_custom_qr_with_dotted_pattern(data, sequence, qr_size=275, bg_size=400,
                                           dot_radius=1, min_opacity=25, max_opacity=200,
                                           qroption="With Background"):
    # print(f"✅ QR Option Selected: {qroption}")

    # Generate base QR code
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H,
                       box_size=10, border=3)
    qr.add_data(data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB').resize((qr_size, qr_size))
    qr_position = ((bg_size - qr_size) // 2, (bg_size - qr_size) // 2)

    # Add random dots on top of QR code
    qr_img_with_dots = generate_random_dots_on_qr(qr_img.copy(), dot_radius, min_opacity, max_opacity)

    # Create background (with or without pattern)
    if qroption == "With Background":
        # print("✅ Generating background with gradient and dotted pattern.")
        gradient_bg = create_radial_gradient_from_qr_edges(bg_size, qr_size, qr_position)
        bg_img = gradient_bg.convert('RGBA')
        dotted_pattern = generate_unique_dotted_pattern(bg_size, dot_radius, min_opacity, max_opacity)
        bg_img = Image.alpha_composite(bg_img, dotted_pattern)
    else:
        # print("✅ Using plain white background.")
        bg_img = Image.new('RGBA', (bg_size, bg_size), (255, 255, 255, 255))

    # Add overlapping number sequence (always)
    font = ImageFont.load_default()
    text_layer = Image.new('RGBA', (bg_size, bg_size), (255, 255, 255, 0))
    text_draw = ImageDraw.Draw(text_layer)

    num_lines = 5
    overlap_fraction = 0.5
    digits_to_draw = sequence  # Original sequence
    total_digits = len(digits_to_draw)

    # Ensure vertical space is divided evenly over QR height
    vertical_spacing = qr_size / total_digits  # Even if small
    initial_x_position = qr_position[0] + qr_size + 5
    light_red_color = (255, 0, 0)
    alpha_value = 40  # Faint color

    for line in range(num_lines):
        x_shift = int(line * vertical_spacing * overlap_fraction)
        for i in range(int(qr_size / vertical_spacing)):
            index = i % total_digits  # Wrap around if needed
            y_position = qr_position[1] + int(i * vertical_spacing)
            text_draw.text((initial_x_position + x_shift, y_position), str(digits_to_draw[index]), font=font, 
                           fill=(light_red_color[0], light_red_color[1], light_red_color[2], alpha_value))


    # Overlay text on background
    bg_img = Image.alpha_composite(bg_img, text_layer)

    # Paste QR code with dots on top
    bg_img.paste(qr_img_with_dots, qr_position)

    return bg_img

# Generate a random sequence of single digits
def generate_random_single_digit_sequence(length):
    return np.random.randint(0, 9, size=length).tolist()

# Process each row in the Excel file, generate QR codes with encrypted identifiers
def process_excel_and_generate_encrypted_qr(excel_path, key_folder="keys"):
    keys = load_possible_keys(key_folder)
    if not keys:
        raise ValueError("No encryption keys found in the key folder.")

    key = keys[0]  # Use the first available key
    fernet = Fernet(key)
    df = pd.read_excel(excel_path)

    for index, row in df.iterrows():
        identifier = f"Row_{index}"
        encrypted_id = encrypt_identifier(identifier, fernet)
    
        sequence = generate_random_single_digit_sequence(40)
    
        # 👇 Get qroption from Excel column (case-insensitive fallback)
        qroption = str(row.get("qroption", "With Background")).strip()
    
        print(f"✅ Row {index} - QR Option Selected from Excel: {qroption}")
    
        custom_qr = generate_custom_qr_with_dotted_pattern(encrypted_id, sequence, qroption=qroption)
    
        row_data = row.to_dict()
        save_row_information(encrypted_id, row_data)
    
        qr_filename = save_qr_code(custom_qr, sequence)
        print(f"📁 Row {index} - Saved QR Code as:", qr_filename)
        custom_qr.show()

# Initialize encryption key (only needs to be done once)
if not os.path.exists("keys/encryption_key.key"):
    generate_encryption_key()

# Set Excel file path and process it to generate QR codes with encrypted identifiers
excel_path = "Output/dataQR.xlsx"
process_excel_and_generate_encrypted_qr(excel_path)
