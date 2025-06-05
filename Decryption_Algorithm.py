# -*- coding: utf-8 -*-
"""
This decryption script is to create an output with all information of encrypted data points read into it via file input.
"""

import os
import json
import pandas as pd
from cryptography.fernet import Fernet, InvalidToken

# Path to the folder containing key files
KEYS_FOLDER = "keys"
ROW_INFO_FILE = "Row_Info.json"
OUTPUT_FILE = "Decrypted_Row_Info.xlsx"  # Can change to .csv if needed

def load_all_keys(keys_folder):
    """Load all .key files from the specified folder."""
    keys = []
    for filename in os.listdir(keys_folder):
        if filename.endswith(".key"):
            with open(os.path.join(keys_folder, filename), "rb") as f:
                key_data = f.read()
                keys.append((filename, key_data))
    return keys

def try_decrypt(encrypted_id, keys):
    """Try decrypting the ID with each key. Return decrypted ID and key filename if successful."""
    for key_name, key_bytes in keys:
        fernet = Fernet(key_bytes)
        try:
            decrypted_id = fernet.decrypt(encrypted_id.encode()).decode()
            return decrypted_id, key_name
        except InvalidToken:
            continue
    return None, None

def decrypt_row_info():
    if not os.path.exists(ROW_INFO_FILE):
        print(f"❌ Row_Info file not found: {ROW_INFO_FILE}")
        return

    # Load encrypted data
    with open(ROW_INFO_FILE, "r") as file:
        encrypted_data = json.load(file)

    # Load all keys
    keys = load_all_keys(KEYS_FOLDER)
    if not keys:
        print(f"❌ No key files found in {KEYS_FOLDER}")
        return

    decrypted_rows = []
    failed_ids = []

    for encrypted_id, row in encrypted_data.items():
        decrypted_id, key_used = try_decrypt(encrypted_id, keys)
        if decrypted_id:
            row['Decrypted ID'] = decrypted_id
            row['Key Used'] = key_used
            decrypted_rows.append(row)
        else:
            failed_ids.append(encrypted_id)

    # Export result
    if decrypted_rows:
        df = pd.DataFrame(decrypted_rows)
        df.to_excel(OUTPUT_FILE, index=False)
        print(f"✅ Successfully decrypted {len(decrypted_rows)} records.")
        print(f"📁 Output saved to: {OUTPUT_FILE}")
    else:
        print("❌ No rows could be decrypted.")

    if failed_ids:
        print(f"\n⚠️ Failed to decrypt {len(failed_ids)} records.")
        print("🔒 Encrypted IDs that could not be decrypted:")
        for enc_id in failed_ids:
            print(" -", enc_id)

if __name__ == "__main__":
    decrypt_row_info()
