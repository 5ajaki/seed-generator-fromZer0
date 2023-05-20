from tkinter import *

# Create the root window
root = Tk()
root.title("24 Word Seed Generator")
root.maxsize(900, 600)
root.config(bg="skyblue")

# Create the left frame
left_frame = Frame(root, width=200, height=400, bg='grey')
left_frame.grid(row=0, column=0, padx=10, pady=5)

# Create labels in the left frame
Label(left_frame, text="24 Word Seed Generator").grid(row=0, column=0, padx=5, pady=5)
Label(left_frame, text="Click the button below to generate a new seed").grid(row=1, column=0, padx=5, pady=5)

# Create the right frame
right_frame = Frame(root, width=650, height=400, bg='grey')
right_frame.grid(row=0, column=1, padx=10, pady=5)

# Here you can add other widgets like buttons, text boxes, etc.

root.mainloop()
