import psutil
import time


def get_system_health():

    # Disk usage
    disk = psutil.disk_usage('/')
    disk_percent = disk.percent

    # CPU usage
    cpu_percent = psutil.cpu_percent(interval=1)

    # RAM usage
    memory = psutil.virtual_memory()
    ram_percent = memory.percent

    # Uptime
    uptime_hours = (time.time() - psutil.boot_time()) / 3600

    return {
        "disk_usage_percent": disk_percent,
        "cpu_usage_percent": cpu_percent,
        "ram_usage_percent": ram_percent,
        "uptime_hours": uptime_hours
    }
