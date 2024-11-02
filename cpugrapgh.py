import psutil
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

# Settings for deque to store only the latest values
MAX_LEN = 50  # adjust this for how much history you want to display

# Initialize deques for each metric
cpu_data = deque([0] * MAX_LEN, maxlen=MAX_LEN)
memory_data = deque([0] * MAX_LEN, maxlen=MAX_LEN)
disk_data = deque([0] * MAX_LEN, maxlen=MAX_LEN)
network_sent_data = deque([0] * MAX_LEN, maxlen=MAX_LEN)
network_recv_data = deque([0] * MAX_LEN, maxlen=MAX_LEN)

# Set up figure and subplots
fig, axs = plt.subplots(4, 1, figsize=(10, 8))
fig.suptitle("System Monitoring")

# Functions to update each metric
def update_cpu():
    cpu_data.append(psutil.cpu_percent(interval=0.5))

def update_memory():
    memory = psutil.virtual_memory()
    memory_data.append(memory.percent)

def update_disk():
    disk = psutil.disk_usage('/')
    disk_data.append(disk.percent)

def update_network():
    network = psutil.net_io_counters()
    network_sent_data.append(network.bytes_sent / (1024 ** 2))  # MB
    network_recv_data.append(network.bytes_recv / (1024 ** 2))  # MB

# Update function for animation
def animate(i):
    update_cpu()
    update_memory()
    update_disk()
    update_network()

    # CPU plot
    axs[0].cla()
    axs[0].plot(cpu_data, color='blue')
    axs[0].set_title("CPU Usage (%)")
    axs[0].set_ylim(0, 100)

    # Memory plot
    axs[1].cla()
    axs[1].plot(memory_data, color='green')
    axs[1].set_title("Memory Usage (%)")
    axs[1].set_ylim(0, 100)

    # Disk plot
    axs[2].cla()
    axs[2].plot(disk_data, color='purple')
    axs[2].set_title("Disk Usage (%)")
    axs[2].set_ylim(0, 100)

    # Network plot
    axs[3].cla()
    axs[3].plot(network_sent_data, label='Sent (MB)', color='red')
    axs[3].plot(network_recv_data, label='Received (MB)', color='orange')
    axs[3].set_title("Network I/O (MB)")
    axs[3].legend(loc='upper right')

# Create the animation
ani = animation.FuncAnimation(fig, animate, interval=1000)

plt.tight_layout()
plt.show()