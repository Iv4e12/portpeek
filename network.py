
import socket


def inspect():
    print("\n  === NETWORK INSPECTOR ===\n")

    hostname = socket.gethostname()

    try:
        ip_address = socket.gethostbyname(hostname)
    except socket.gaierror:
        ip_address = "Unavailable"

    print(f"  Hostname : {hostname}")
    print(f"  Local IP : {ip_address}")

    target = input("\n  Enter target IP or hostname: ").strip()

    if not target:
        print("  No target entered.")
        input("\n  Press Enter to return...")
        return

    try:
        target_ip = socket.gethostbyname(target)
        print(f"\n  Target IP: {target_ip}")

        ports = [22, 53, 80, 443, 3306, 8080, 8443]

        print("\n  Checking common TCP ports...\n")

        for port in ports:
            connection = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )
            connection.settimeout(0.5)

            result = connection.connect_ex((target_ip, port))
            connection.close()

            service = socket.getservbyport(port, "tcp") \
                if port in [22, 53, 80, 443] else "Unknown"

            status = "OPEN" if result == 0 else "CLOSED"

            print(f"  {port:<6} {service:<12} {status}")

    except socket.gaierror:
        print("\n  Could not resolve target hostname.")

    input("\n  Press Enter to return...")
