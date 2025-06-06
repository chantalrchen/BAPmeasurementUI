import tkinter as tk
import matplotlib.pyplot as plt
#import time
import csv

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

# store parameters for plotting
flow_rate_values = []
pressure_values = []
time_since_start = []

start_time = None  #to keep
current_fig = None #to store the last figure

# Function to update time label
def update_time():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    time_label.config(text=current_time)
    window.after(1000, update_time)  #Updating the time every second
    
def update_parameters():
    global current_fig
    try:
        # Obtain values from entry fields
        flow_rate = float(flow_rate_entry.get())
        pressure = float(pressure_entry.get())

        # Update the parameters
        flow_rate_display.config(text=f"Flow Rate: {flow_rate}")
        pressure_display.config(text=f"Pressure: {pressure}")
        
        flow_rate_values.append(flow_rate)
        pressure_values.append(pressure)
        
        now = datetime.now()
        elapsed = (now - start_time).total_seconds()
        time_since_start.append(elapsed)
        
        current_fig = update_graph()
    except ValueError:
        # non float numbers are entered
        flow_rate_display.config(text="Flow Rate: non-float number, invalid input")
        pressure_display.config(text="Pressure: non-float number, invalid input")
    
def update_graph():
    fig = plt.Figure(figsize=(5, 4))
    ax = fig.add_subplot(111)

    # Plot the updated values
    ax.plot(time_since_start, flow_rate_values, label="Flow Rate", color='blue')
    ax.plot(time_since_start, pressure_values, label="Pressure", color='red')

    # Labeling the axes
    ax.set_xlabel('Time')
    ax.set_ylabel('Values')

    # Adding title and legend
    ax.set_title('Flow Rate and Pressure Over Time')
    ax.legend()
    
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().grid(row=0, column=2, padx=20, pady=20)
    canvas.draw()
    return fig #such that the figure can be saved later

def cmd_start():
    ##connecting with the three devices, idk how to implement
    # clear the par lists
    global start_time
    start_time = datetime.now()
    flow_rate_values.clear()
    pressure_values.clear()
    time_since_start.clear()
    update_graph()

def save_graph():
    if not current_fig:
        print("No graph to save yet.")
        return
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"graph_{timestamp}.png"
    current_fig.savefig(filename)
    print(f"Graph saved as {filename}")

def save_data():
    if not time_since_start:
        print("No data to save yet.")
        return
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data_{timestamp}.csv"
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Time (s)", "Flow Rate", "Pressure"])
        for t, f, p in zip(time_since_start, flow_rate_values, pressure_values):
            writer.writerow([t, f, p])
    print(f"Data saved as {filename}")
   
    
window = tk.Tk()
window.title("Test UI Chantal")
window.geometry("1000x500")

frame = tk.Frame(window)
frame.pack(padx=20, pady=20)

##left frame where you can adjust the values
left_datainput= tk.Frame(frame)
left_datainput.grid(row=0, column=0, padx=20)

#flow rate
flow_rate_label = tk.Label(left_datainput, text="Flow rate: ")
flow_rate_label.grid(column=0, row=0, pady=10)

flow_rate_entry = tk.Entry(left_datainput, width=50)
flow_rate_entry.grid(column=0, row=1, pady=10)

#pressure
pressure_label = tk.Label(left_datainput, text="Pressure: ")
pressure_label.grid(column=0, row=2, pady=10)

pressure_entry = tk.Entry(left_datainput, width=50)
pressure_entry.grid(column=0, row=3, pady=10)

start_button = tk.Button(left_datainput, text="Start", command= cmd_start)
start_button.grid(column=0, row=4, pady=20)

#to update the parameter values
update_button = tk.Button(left_datainput, text="Update Parameters: ", command=update_parameters)
update_button.grid(column=0, row=5, pady=20)

save_graph_button = tk.Button(left_datainput, text="Save Graph", command=save_graph)
save_graph_button.grid(column=0, row=6, pady=10)

save_data_button = tk.Button(left_datainput, text="Save Data", command=save_data)
save_data_button.grid(column=0, row=7, pady=10)

##right frame with the display of the updated values
right_datadisplay = tk.Frame(frame)
right_datadisplay.grid(column=1, row=0, padx=20)

flow_rate_display = tk.Label(right_datadisplay, text="Flow Rate: ")
flow_rate_display.grid(column=1, row=0, pady=10)

pressure_display = tk.Label(right_datadisplay, text="Pressure: ")
pressure_display.grid(column=1, row=1, pady=10)

##time rechtsboven display
time_label = tk.Label(window)
time_label.place(x=850, y=10)  # Adjust the position

update_time() ##updating the time every second
window.mainloop()

