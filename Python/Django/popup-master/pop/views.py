from django.shortcuts import render
from django.http import JsonResponse
import tkinter
from tkinter import messagebox

# Create your views here.
def home(request):
    context = {}
    return render(request, "index.html", context)

def showPopUp(request):
    root = tkinter.Tk()
    root.withdraw()

    # message box display
    # messagebox.showerror("Error", "Error message")
    messagebox.showwarning("Warning","Database overload!")
    # messagebox.showinfo("Information","Informative message")
    context = {}
    return render(request, "index.html", context)
