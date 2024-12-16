import os
import subprocess
import platform

def get_wifi_profiles_windows():
    """Get previously connected Wi-Fi networks on Windows."""
    try:
        # Run the command to show profiles in Windows
        command = "netsh wlan show profiles"
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        profiles = []

        # Parse the output to get the Wi-Fi network names
        if result.returncode == 0:
            lines = result.stdout.splitlines()
            for line in lines:
                if "All User Profile" in line:
                    # Extract Wi-Fi network names
                    profile_name = line.split(":")[1].strip()
                    profiles.append(profile_name)
        return profiles
    except Exception as e:
        print(f"Error: {e}")
        return []

def get_wifi_profiles_linux():
    """Get previously connected Wi-Fi networks on Linux."""
    try:
        # List files in the NetworkManager's system-connections directory
        connections_path = "/etc/NetworkManager/system-connections/"
        if not os.path.exists(connections_path):
            print("NetworkManager system connections directory not found.")
            return []

        profiles = []
        for file_name in os.listdir(connections_path):
            if file_name.endswith(".nmconnection"):
                profiles.append(file_name)
        return profiles
    except Exception as e:
        print(f"Error: {e}")
        return []

def main():
    system_platform = platform.system()
    print(f"Operating System: {system_platform}")

    if system_platform == "Windows":
        print("\nPreviously connected Wi-Fi networks on Windows:")
        profiles = get_wifi_profiles_windows()
    elif system_platform == "Linux":
        print("\nPreviously connected Wi-Fi networks on Linux:")
        profiles = get_wifi_profiles_linux()
    else:
        print("Unsupported OS. This script works on Windows and Linux only.")
        return

    if profiles:
        print("\nFound Wi-Fi profiles:")
        for profile in profiles:
            print(f"- {profile}")
    else:
        print("No previously connected Wi-Fi networks found.")

if __name__ == "__main__":
    main()
