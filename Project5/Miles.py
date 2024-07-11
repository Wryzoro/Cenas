import tkinter as tk
from tkinter import ttk

def convert():
    mile_inputs = entry_int.get()
    try:
        km_output = mile_inputs * 1.61
        output_string.set(f"{mile_inputs} miles is equal to {km_output:.2f} kilometers.")
    except tk.TclError:
        output_string.set("Please enter a valid number.")

# window
window = tk.Tk()
window.title("Demo")
window.geometry("500x250")

# title label
title_label = ttk.Label(master=window, text="Miles To Kilometers Converter", font="Calibri 24 bold")
title_label.pack()

# input frame
input_frame = ttk.Frame(master=window)
input_frame.pack(pady=10)

# input field and button
entry_int = tk.IntVar()
entry = ttk.Entry(master=input_frame, textvariable=entry_int)
button = ttk.Button(master=input_frame, text="Convert", command=convert)
entry.pack(side='left', padx=10)
button.pack(side='left')

# output
output_string = tk.StringVar()
output_label = ttk.Label(master=window, textvariable=output_string, font="Calibri 14")
output_label.pack(pady=5)

# start the main loop
window.mainloop()














#run
window.mainloop()
