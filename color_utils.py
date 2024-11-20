import tkinter as tk
import colorsys
import time
import threading

def rainbow_effect(label, text):
    def animate():
        for i in range(100):
            if not label.winfo_exists():
                return
                
            # Generate rainbow colors
            hue = (i % 100) / 100
            rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
            color = '#{:02x}{:02x}{:02x}'.format(
                int(rgb[0] * 255),
                int(rgb[1] * 255),
                int(rgb[2] * 255)
            )
            
            label.configure(text=text, fg=color)
            time.sleep(0.01)
            
        # Reset to white
        if label.winfo_exists():
            label.configure(fg='white')
    
    # Run animation in separate thread
    threading.Thread(target=animate, daemon=True).start() 