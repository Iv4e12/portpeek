import re
import subprocess
import time


def inspect():
    print("\n  === USB INSPECTOR ===\n")

    try:
        result = subprocess.run(
            ["lsusb"],
            capture_output=True,
            text=True,
            check=True
        )

        lines = result.stdout.strip().splitlines()

        if not lines or not lines[0]:
            print("  No USB devices detected.")
        else:
            print(f"  Devices detected: {len(lines)}\n")

            for index, line in enumerate(lines, 1):
                match = re.search(
                    r"Bus\s+(\d+)\s+Device\s+(\d+):\s+ID\s+([0-9a-fA-F]{4}):([0-9a-fA-F]{4})\s*(.*)",
                    line
                )

                if match:
                    bus, device, vendor, product, name = match.groups()

                    print(f"  [{index}] {name or 'Unknown device'}")
                    print(f"      Bus: {bus}  Device: {device}")
                    print(
                        f"      Vendor ID: {vendor.upper()}  "
                        f"Product ID: {product.upper()}\n"
                    )

    except FileNotFoundError:
        print("  Error: lsusb is not installed.")
        print(
            "  Install the 'usbutils' package "
            "using your distribution's package manager."
        )

    except subprocess.CalledProcessError:
        print("  Error: Could not retrieve USB devices.")

    choice = input("\n  Start USB monitoring? [y/N]: ").strip().lower()

    if choice == "y":
        monitor()


def monitor():
    print("\n  === USB HOTPLUG MONITOR ===")
    print("  Monitoring USB devices...")
    print("  Press Ctrl+C to stop.\n")

    try:
        result = subprocess.run(
            ["lsusb"],
            capture_output=True,
            text=True,
            check=True
        )

        previous = set(result.stdout.strip().splitlines())

        while True:
            time.sleep(2)

            result = subprocess.run(
                ["lsusb"],
                capture_output=True,
                text=True,
                check=True
            )

            current = set(result.stdout.strip().splitlines())

            connected = current - previous
            disconnected = previous - current

            for device in connected:
                print(f"  [+] CONNECTED: {device}")

            for device in disconnected:
                print(f"  [-] DISCONNECTED: {device}")

            previous = current

    except KeyboardInterrupt:
        print("\n\n  Monitoring stopped.")

    except (FileNotFoundError, subprocess.CalledProcessError):
        print("\n  Could not monitor USB devices.")

    input("\n  Press Enter to return...")
