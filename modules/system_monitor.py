import psutil
import time

def get_system_metrics():
    # Disk Usage
    disk = psutil.disk_usage('/')
    disk_usage_percent = disk.percent

    # CPU Usage
    cpu_usage_percent = psutil.cpu_percent(interval=1)

    # RAM Usage
    memory = psutil.virtual_memory()
    ram_usage_percent = memory.percent

    # System Uptime
    boot_time = psutil.boot_time()
    uptime_seconds = time.time() - boot_time
    uptime_hours = uptime_seconds / 3600

    return {
        "disk_usage": disk_usage_percent,
        "cpu_usage": cpu_usage_percent,
        "ram_usage": ram_usage_percent,
        "uptime_hours": uptime_hours
    }
