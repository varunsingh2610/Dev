import tkinter
from tkinter import messagebox

# hide main window
root = tkinter.Tk()
root.withdraw()

# message box display
# messagebox.showerror("Error", "Error message")
messagebox.showwarning("Warning","Database overload!")
# messagebox.showinfo("Information","Informative message")
