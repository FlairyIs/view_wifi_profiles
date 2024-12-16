import os
import subprocess
import platform

def get_wifi_password_windows(profile_name):
    """Get the Wi-Fi password for a given profile on Windows."""
    try:
        # Run the command to show the Wi-Fi profile details
        command = f'netsh wlan show profiles name="{profile_name}" key=clear'
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        
        if result.returncode == 0:
            # Parse the output to find the password
            lines = result.stdout.splitlines()
            for line in lines:
                if "Key Content" in line:
                    # Extract and return the Wi-Fi password
                    password = line.split(":")[1].strip()
                    return password
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

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

def get_wifi_password_linux(profile_name):
    """Get the Wi-Fi password for a given profile on Linux."""
    try:
        # Check if the NetworkManager configuration directory exists
        connections_path = f"/etc/NetworkManager/system-connections/{profile_name}"
        if not os.path.exists(connections_path):
            print(f"Configuration file for {profile_name} not found.")
            return None

        # Read the connection file to extract the password
        with open(connections_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if "psk=" in line:
                    # Extract the password (after the "psk=" keyword)
                    password = line.split("psk=")[1].strip()
                    return password
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

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
        for profile in profiles:
            print(f"\nNetwork: {profile}")
            password = get_wifi_password_windows(profile)
            if password:
                print(f"Password: {password}")
            else:
                print("No password found or cannot retrieve the password.")
    elif system_platform == "Linux":
        print("\nPreviously connected Wi-Fi networks on Linux:")
        profiles = get_wifi_profiles_linux()
        for profile in profiles:
            print(f"\nNetwork: {profile}")
            password = get_wifi_password_linux(profile)
            if password:
                print(f"Password: {password}")
            else:
                print("No password found or cannot retrieve the password.")
    else:
        print("Unsupported OS. This script works on Windows and Linux only.")

if __name__ == "__main__":
    main()
