import os
import hashlib
import tkinter as tk
from tkinter import ttk

def string_to_binary(input_string):
    # Hash the input string
    hashed = hashlib.sha256(input_string.encode()).digest()
    
    # Convert the hash to binary
    binary_str = ''.join(format(byte, '08b') for byte in hashed)
    
    return binary_str

def transform_binary():
    # Retrieve the user's input from the input field
    input_string = input_text.get()
    
    # Use the input string to generate binary
    generate_binary(input_string)



def binary_to_decimal(binary):
    binary = binary[::-1]  # Reverse the binary string to start from rightmost bit
    decimal = 0
    for i in range(len(binary)):
        decimal += int(binary[i]) * (2**i)
    return decimal

def import_words(file_path):
    with open(file_path, 'r') as file:
        words = [line.strip() for line in file]
    return words

# import words from a file
word_list = import_words('bip39list.txt')

def generate_binary(input_string=None):
    # If an input string is given, use it to generate the binary string
    if input_string is not None:
        binary_str = string_to_binary(input_string)
    else:
        # Generate 256 random bits
        binary_data = os.urandom(32)  
        binary_str = ''.join(format(byte, '08b') for byte in binary_data)

    # Clear the text fields and labels
    result_text.delete(1.0, tk.END)
    hashed_result_text.delete(1.0, tk.END)
    appended_result_text.delete(1.0, tk.END)
    for row in binary_labels:
        for label in row:
            label['text'] = ''
    for row in decimal_labels:
        for label in row:
            label['text'] = ''
    for row in word_labels:
        for label in row:
            label['text'] = ''

    # Insert the new binary string into the text field
    result_text.insert(tk.END, binary_str)

def generate_sha256():
    # Retrieve binary from text field
    binary_str = result_text.get(1.0, tk.END).strip()

    # Convert binary to bytes
    binary_bytes = bytes(int(binary_str[i:i+8], 2) for i in range(0, len(binary_str), 8))

    # Calculate SHA256 hash
    sha256 = hashlib.sha256(binary_bytes).digest()

    # Convert hash to binary
    sha256_binary = ''.join(format(byte, '08b') for byte in sha256)

    # Clear the hashed result text field
    hashed_result_text.delete(1.0, tk.END)

    # Insert the new binary hash into the hashed result text field
    hashed_result_text.insert(tk.END, sha256_binary)

    # Append first 8 bits of SHA256 to original binary and display in appended result text field
    appended_binary = binary_str + sha256_binary[:8]
    appended_result_text.delete(1.0, tk.END)
    appended_result_text.insert(tk.END, appended_binary)

    # Split appended binary into chunks of 11 bits and display in labels
    for i in range(6):
        for j in range(4):
            binary_chunk = appended_binary[(i*4+j)*11:(i*4+j+1)*11]
            binary_labels[i][j]['text'] = binary_chunk

            # Convert binary to decimal and display in decimal labels
            decimal = binary_to_decimal(binary_chunk)
            decimal_labels[i][j]['text'] = str(decimal)

            # Look up word in list and display in word labels
            word = word_list[decimal]
            word_labels[i][j]['text'] = word



###################
ro = 8
##################

# Create the main window
root = tk.Tk()
root.title("Seed Phrase Generator")

# Create a main frame
main_frame = ttk.Frame(root, padding="10")
main_frame.grid(sticky='NSEW')

# Create a #frame for the buttons and text fields
frame = ttk.Frame(main_frame, padding="10", relief='sunken', borderwidth=2)
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))


# Create a button that will call generate_binary to fill binary data
generate_button = ttk.Button(frame, text="Produce 256 bits of Random Entropy", command=generate_binary)
generate_button.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5, columnspan=4)

# Create a button that will transform user input to binary
generate_button = ttk.Button(frame, text="Transform Input to Binary", command=transform_binary)
generate_button.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

# Create a text field for input here.  Use the input for 
input_text = tk.Entry(frame, width=48)
input_text.grid(row=1, column=0, columnspan=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)



# Create a label
result_label = ttk.Label(frame, text="256 bits:")
result_label.grid(row=2, column=0, sticky=(tk.E))

# Create a text field to display the binary
result_text = tk.Text(frame, width=96, height=3)
result_text.grid(row=2, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), columnspan=4)

# Create a button that will call generate_sha256 when clicked
hash_button = ttk.Button(frame, text="Generate", command=generate_sha256)
hash_button.grid(row=ro, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=25, columnspan=5)





# Create a label
hashed_result_label = ttk.Label(frame, text="Take the SHA256 of that entropy, jam the\nfirst 8 bits of the result to the end of that entropy\n(gives you 264 bits in total):")
hashed_result_label.grid(row=ro+1, column=0, sticky=(tk.W))

# Create a text field to display the hashed binary
hashed_result_text = tk.Text(frame, width=96, height=3)
hashed_result_text.grid(row=ro+1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), columnspan=4)

# Create a label
appended_result_label = ttk.Label(frame, text="Now split this into 24 groups of 11 bits,\nconvert to decimal, and map the decimal to\nthe appropriate index in the BIP39 list:")
appended_result_label.grid(row=ro+2, column=0, sticky=(tk.W))

# Create a text field to display the appended binary
appended_result_text = tk.Text(frame, width=96, height=3)
appended_result_text.grid(row=ro+2, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), columnspan=4)

howto_label = ttk.Label(frame, text="Convert binary to decimal:\nsum of {bit} * 2 ^ {position}\nafter reversing the string (LSB position 0):")
howto_label.grid(row=ro+4, column=0, sticky=(tk.W))

# Create a 6x4 grid of labels to display binary chunks
binary_labels = [[ttk.Label(frame, text='') for _ in range(4)] for _ in range(6)]
for i in range(6):
    for j in range(4):
        binary_labels[i][j].grid(row=ro+3+i, column=j+1, sticky=(tk.W),pady=5)
        
howto_label2 = ttk.Label(frame, text="Take resulting integers (0-2048)\nand map to the BIP39 list:")
howto_label2.grid(row=ro+10, column=0, sticky=(tk.W))

# Create a 6x4 grid of labels to display decimal equivalents of binary chunks
decimal_labels = [[ttk.Label(frame, text='') for _ in range(4)] for _ in range(6)]
for i in range(6):
    for j in range(4):
        decimal_labels[i][j].grid(row=ro+8+i, column=j+1, sticky=(tk.W),pady=5)


howto_label2 = ttk.Label(frame, text="Your new seed phrase:\n(Adjust entropy, try hit Generate again)")
howto_label2.grid(row=ro+16, column=0, sticky=(tk.W))

# Create a 6x4 grid of labels to display words corresponding to decimal values
word_labels = [[ttk.Label(frame, text='') for _ in range(4)] for _ in range(6)]
for i in range(6):
    for j in range(4):
        word_labels[i][j].grid(row=ro+14+i, column=j+1, sticky=(tk.W),pady=5)

root.mainloop()