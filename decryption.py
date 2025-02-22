import cv2
import os
import numpy as np

# Load the encrypted image (using PNG ensures no data loss)
img = cv2.imread("encryptedImage.png")
if img is None:
    print("Error: Could not load image 'encryptedImage.png'.")
    exit(1)

# Create a dictionary for ASCII conversion
c = {i: chr(i) for i in range(256)}

# --- Retrieve Meta Information ---
# 1. Retrieve the secret message length from pixel (0,0) channel 0.
msg_length = int(img[0, 0, 0])

# 2. Retrieve the stored password from row 0, channel 1.
pw_length = int(img[0, 0, 1])
stored_password = ""
for i in range(pw_length):
    stored_password += c[int(img[0, i + 1, 1])]

# Prompt user for the passcode for decryption and verify it.
input_password = input("Enter passcode for decryption: ")
if input_password != stored_password:
    print("YOU ARE NOT AUTHORIZED")
    exit(1)

# --- Decode the Secret Message ---
# The message was encoded starting from row 1, column 0 in channel 0.
message = ""
n = 1  # starting row for the message
m = 0  # starting column for the message
for i in range(msg_length):
    message += c[int(img[n, m, 0])]
    m += 1
    if m >= img.shape[1]:
        m = 0
        n += 1

print("Decryption message:", message)
