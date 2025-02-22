import cv2
import os
import numpy as np

img = cv2.imread("mypic.jpg")
if img is None:
    print("Error: Could not load image 'mypic.jpg'.")
    exit(1)

# Input secret message and password
msg = input("Enter secret message: ")
password = input("Enter a passcode: ")

# Create a dictionary for ASCII conversion
d = {chr(i): i for i in range(256)}

# --- Store Meta Information ---
# 1. Store the message length in pixel (0,0) channel 0
msg_length = len(msg)
if msg_length > 255:
    print("Error: Message too long, must be less than 256 characters.")
    exit(1)
img[0, 0, 0] = msg_length

# 2. Store the password length and password characters in row 0, channel 1.
pw_length = len(password)
if pw_length > (img.shape[1] - 1):  # ensure there is enough space in row 0
    print("Error: Password too long for this image.")
    exit(1)
img[0, 0, 1] = pw_length  # Store password length
for i in range(pw_length):
    img[0, i + 1, 1] = d[password[i]]  # Store each character's ASCII value

# --- Encode the Secret Message ---
# We encode the message starting from row 1, column 0 in channel 0.
n = 1  # starting row for message data
m = 0  # starting column for message data
for char in msg:
    if n >= img.shape[0]:
        print("Error: Image is not large enough to encode the message.")
        exit(1)
    img[n, m, 0] = d[char]
    m += 1
    if m >= img.shape[1]:
        m = 0
        n += 1

# Save the encrypted image using PNG to ensure lossless storage of data
cv2.imwrite("encryptedImage.png", img)
os.system("start encryptedImage.png")  # Windows-specific command to open the image
print("Encryption complete. Encrypted image saved as 'encryptedImage.png'.")
