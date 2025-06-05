# 🔍 Data Screener & Secure QR Code Generator
This project is a comprehensive solution designed for secure product data screening, QR code generation with encryption, and subsequent decryption — all built using Python and Tkinter, with support from PIL, cryptography, and qrcode libraries.

It includes:

    📋 **Data Screener** GUI for structured data entry and validation

    🔐 **Encrypted QR Generator** using Fernet keys

    🧩 **Decryption Algorithm** to read encrypted QR codes

    🖼️ *Optional* **Visual Enhancements** like dotted patterns and background layers

## 💻 Features

**User-Friendly Interface:** A Tkinter-based GUI to input personal and product-related metadata (name, factory ID, QR size, etc.)

**Flexible QR Options:** Choose between QR codes with background pattern or simple QR codes on a plain white background

**Encrypted QR Generation:** Encrypts user-defined fields and saves the result as a secure QR image

**Decryption Script:** Recovers original information from the encrypted QR

**Stylized QR Presentation:**

    Steganographic overlapping and compressed number bars printed on the right of each QR

    Visual patterns overlaid to deter unauthorized scanning/copying

## 🗂️ Folder Structure & File Format

Project/
│
├── Data_Screener.py             # GUI interface for data collection
├── QR_with_Key_Generator.py     # Script to generate encrypted QR codes
├── Encrypted_QR_Generator.py    # Script to generate encrypted QR codes
├── Decryption_Algorithm.py      # Script to decode encrypted QR images
│
├── keys/
│   ├── encryption_key.key       # Fernet symmetric encryption key
│
├── Encoded/
│   └── QRs/                     # Stores all generated QR images using Encrypted_QR_Generator.py
│       └── <ID>.png             # Named using row-based identifier (e.g., 0001.png)
│
├── Output/
│   └── dataQR.xlsx              # Excel sheet storing generated input metadata from GUI
│   └── QR_Keys_Info.xlsx        # Excel sheet storing corresponding "keys" from either QR generator files
│   └── QRs/                     # Stores all generated QR images using QR_with_Key_Generator.py
│       └── <ID>.png             # Named using row-based identifier (e.g., 0001.png)
│
├── Image/
│   └── background.jpg           # Optional image used for QR background
|   └── License Free.txt         # License of the free image used for demo
│
├── Row_Info.json                # Metadata output from either QR generator files later used for decryption
|
├── Decrypted_Row_Info.xlsx      # Excel sheet storing output for decrypted QRs using Decryption_Algorithm.py
|
|
└── README.md                    # Project description and documentation

## 📁 File Format Summary
*dataQR.xlsx:* Excel file storing each row of metadata inputs.

    Fields: First Name, Last Name, Title, Factory, Product ID, Registration Status, Other, QR Option, QR Size

**QR Images:**

    File Name: *<RowIndex>.png*

    Location: *Encoded/QRs/*

    Order: Saved in sequence based on row number in *dataQR.xlsx*

    Design: Depends on *QR Option* selected:

        "With Background" → Gradient + dotted overlay

        "Without Background" → Plain white + sequence line, with visual dots retained

## 🛠️ Tech Stack

    **Python 3.8+**

    **tkinter** – for the GUI

    **Pillow** – for image processing

    **qrcode** – QR code generation

    **cryptography** – for encryption/decryption

    **openpyxl** – for Excel file handling

## 🔐 Security Note
The encryption uses **Fernet (symmetric AES-based encryption)**. Only users with the correct *.key* file can decrypt and read the QR content. Do not share the *encryption_key.key* publicly.

## 🧪 Sample Output & QR Examples
To help users understand the output structure and test the functionalities, the repository includes **pre-generated sample data**:

    ✅ A few rows of metadata stored in *Output/dataQR.xlsx*

    🖼️ Corresponding QR images saved under *Encoded/QRs/* OR *Output/QRs/*
        Each file is named with a unique identifier (e.g., *4423.png*, *0284.png*) and demonstrates variations like:

            Encrypted content

            With or without background

            Stylized dotted overlay

            Overlapping number sequences on the right

    These examples can be used as a **reference** to verify script behavior or adapt for integration with your own datasets.
