
import platform
import os
import socket


def inspect():
    print("\n  === SYSTEM INFORMATION ===\n")

    print(f"  OS          : {platform.system()}")
    print(f"  Distribution: {platform.platform()}")
    print(f"  Release     : {platform.release()}")
    print(f"  Architecture: {platform.machine()}")
    print(f"  Hostname    : {socket.gethostname()}")
    print(f"  Python      : {platform.python_version()}")
    print(f"  CPU cores   : {os.cpu_count()}")

    try:
        with open("/proc/meminfo", "r") as file:
            memory = file.readlines()

        total = next(
            line for line in memory
            if line.startswith("MemTotal:")
        )

        available = next(
            line for line in memory
            if line.startswith("MemAvailable:")
        )

        total_mb = int(total.split()[1]) // 1024
        available_mb = int(available.split()[1]) // 1024
        used_mb = total_mb - available_mb

        print(f"  RAM total   : {total_mb} MB")
        print(f"  RAM used    : {used_mb} MB")
        print(f"  RAM available: {available_mb} MB")

    except (OSError, StopIteration, ValueError):
        print("  RAM information unavailable.")

    input("\n  Press Enter to return...")
