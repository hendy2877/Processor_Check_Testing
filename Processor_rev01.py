import subprocess
import psutil
import tkinter as tk
from matplotlib import animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Create a Tkinter window
window = tk.Tk()
window.title("System Information")

# Set the font size for all labels
font_size = 24
font = ("Arial", font_size)

# Get CPU information
cpu_label = tk.Label(window, text=f"CPU: {psutil.cpu_percent()}%", font=font)
cpu_label.pack()

# Get memory information
mem = psutil.virtual_memory()
mem_label = tk.Label(window, text=f"Memory: {mem.percent}% ({mem.used / (1024 ** 3):.1f}GB / {mem.total / (1024 ** 3):.1f}GB)", font=font)
mem_label.pack()

# Get graphics information
try:
    output = subprocess.check_output(["nvidia-smi", "--query-gpu=temperature.gpu", "--format=csv,noheader"])
    gpu_temp = output.decode("utf-8").strip()
    gpu_label = tk.Label(window, text=f"Graphics: {gpu_temp}°C", font=font)
    gpu_label.pack()
    
    # Create a checklist for the GPU
    gpu_check_var = tk.BooleanVar()
    gpu_checkbutton = tk.Checkbutton(window, text="GPU OK?", variable=gpu_check_var, font=font)
    gpu_checkbutton.pack()
except:
    gpu_label = tk.Label(window, text="Graphics: N/A", font=font)
    gpu_label.pack()

# Create a plot of CPU usage over time
fig = Figure(figsize=(5, 4), dpi=100)
ax = fig.add_subplot(111)
ax.set_xlabel('Time (s)')
ax.set_ylabel('CPU Usage (%)')
ax.set_title('CPU Usage Over Time')
xs = []
ys = []
line, = ax.plot(xs, ys)

def animate(i):
    xs.append(i)
    ys.append(psutil.cpu_percent())
    line.set_xdata(xs)
    line.set_ydata(ys)
    ax.relim()
    ax.autoscale_view()
    return line,

canvas = FigureCanvasTkAgg(fig, master=window)
canvas.draw()
canvas.get_tk_widget().pack()

# Start the animation
ani = animation.FuncAnimation(fig, animate, interval=1000,  cache_frame_data=False)

# Start the Tkinter event loop
window.mainloop()
