import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from datetime import datetime, timedelta

class IncomeGraph:
    def __init__(self, master, figure_size=(6, 3)):
        self.figure = plt.Figure(figsize=figure_size, facecolor='#2C3E50')
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor('#2C3E50')
        
        # Style the graph
        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['top'].set_color('white')
        self.ax.spines['left'].set_color('white')
        self.ax.spines['right'].set_color('white')
        self.ax.tick_params(colors='white')
        self.ax.yaxis.label.set_color('white')
        self.ax.xaxis.label.set_color('white')
        
        # Initialize data
        self.times = []
        self.values = []
        self.line, = self.ax.plot([], [], color='#3498DB', linewidth=2)
        
        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.figure, master=master)
        self.canvas_widget = self.canvas.get_tk_widget()
        
    def update(self, current_value):
        current_time = datetime.now()
        
        # Keep only last 50 points
        if len(self.times) > 50:
            self.times.pop(0)
            self.values.pop(0)
            
        self.times.append(current_time)
        self.values.append(float(current_value))
        
        # Update plot
        times_formatted = [(t - self.times[0]).total_seconds() for t in self.times]
        self.line.set_data(times_formatted, self.values)
        
        # Adjust limits
        self.ax.relim()
        self.ax.autoscale_view()
        self.ax.set_ylabel('Balance ($)')
        self.ax.set_xlabel('Time (seconds)')
        
        self.canvas.draw() 