from tkinter import ttk
import tkinter as tk

def configure_styles():
    style = ttk.Style()
    
    # Configure frame style
    style.configure(
        "TFrame",
        background="#2C3E50"
    )
    
    # Configure label style
    style.configure(
        "TLabel",
        background="#2C3E50",
        foreground="#ECF0F1",
        font=("Helvetica", 12)
    )
    
    # Configure button style
    style.configure(
        "TButton",
        background="#3498DB",
        foreground="#ECF0F1",
        padding=10,
        font=("Helvetica", 10, "bold")
    )
    
    # Add hover effect for buttons
    style.map("TButton",
        background=[("active", "#2980B9")],
        foreground=[("active", "#FFFFFF")]
    )
    
    # Configure entry style
    style.configure(
        "TEntry",
        padding=5,
        font=("Helvetica", 10),
        fieldbackground="#ECF0F1"
    ) 