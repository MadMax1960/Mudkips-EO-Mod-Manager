import os
import shutil

# Get the current script directory
script_directory = os.path.dirname(os.path.abspath(__file__))

# Check if the game folder text file exists
game_folder_file = os.path.join(script_directory, "game_folder.txt")
if os.path.isfile(game_folder_file):
    # Read the game folder path from the text file
    with open(game_folder_file, "r") as f:
        game_folder = f.read().strip()
else:
    # Prompt for the game folder path if the text file doesn't exist
    game_folder = input("Enter the path to your game folder: ")

    # Save the game folder path to the text file
    with open(game_folder_file, "w") as f:
        f.write(game_folder)

# Prompt for options
print("Options:")
print("\033[92m1. Install Mods\033[0m")  # Green
print("\033[91m2. Uninstall Mods\033[0m")  # Red
print("\033[91m3. Blacklist Mods\033[0m")  # Red

option = input("Enter the number corresponding to your choice: ")

if option == "1":
    # Set the paths and directories
    catalog_file_path = os.path.join(game_folder, "Etrian Odyssey_Data", "StreamingAssets", "aa", "catalog.json")
    tool_directory = os.path.join(script_directory, "Example")
    patched_file_path = os.path.join(tool_directory, "catalog.json.patched")
    example_command = os.path.join(tool_directory, "example.exe")

    # Copy catalog.json to the tool's directory
    shutil.copy(catalog_file_path, os.path.join(tool_directory, "catalog.json"))

    # Run the tool with the appropriate command
    os.chdir(tool_directory)
    os.system(f'"{example_command}" patchcrc catalog.json')

    # Move the patched file back to the original directory and rename it
    shutil.move(patched_file_path, catalog_file_path)

    mod_folder = os.path.join(script_directory, "Mods")
    backup_folder = os.path.join(game_folder, "Backup")
    mod_temp_folder = os.path.join(script_directory, "Mod_Temp")

    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)

    if not os.path.exists(mod_temp_folder):
        os.makedirs(mod_temp_folder)

    mod_files = {}

    # ANSI escape sequences for colors
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    RED = "\033[91m"
    RESET = "\033[0m"

    def remove_escape_sequences(text):
        # Function to remove ANSI escape sequences
        escape_chars = ['\033', '\x1b']
        for escape in escape_chars:
            text = text.replace(escape, '')
        return text

    for mod_name in os.listdir(mod_folder):
        mod_path = os.path.join(mod_folder, mod_name, "Etrian Odyssey_Data")
        if not os.path.isdir(mod_path):
            continue

        if "Naoto" in mod_name:
            mod_name = BLUE + mod_name + RESET
        else:
            mod_name = GREEN + mod_name + RESET
        
        print("Modding with", GREEN + mod_name + RESET)

        for root, _, files in os.walk(mod_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                relative_path = os.path.relpath(file_path, mod_path)
                game_file = os.path.join(game_folder, "Etrian Odyssey_Data", relative_path)
                backup_file = os.path.join(backup_folder, relative_path)

                if os.path.isfile(game_file):
                    # Check for conflicts
                    if game_file in mod_files and mod_files[game_file] != mod_name:
                        # Conflict detected
                        print(RED + "Conflict detected:" + RESET, game_file)
                        print("  - Mod 1:", mod_files[game_file])
                        print("  - Mod 2:", mod_name)

                        while True:
                            choice = input("Choose mod to copy over (1 or 2): ")
                            if choice in ("1", "2"):
                                chosen_mod = mod_files[game_file] if choice == "1" else mod_name
                                print("Copying file from", chosen_mod)
                                break
                            else:
                                print("Invalid choice. Please enter '1' or '2'.")

                        if choice == "1":
                            # Remove the conflicting file from the unchosen mod
                            os.remove(backup_file)
                            continue

                    # Backup the game file
                    os.makedirs(os.path.dirname(backup_file), exist_ok=True)
                    shutil.copy(game_file, backup_file)

                # Copy the mod file to the temporary folder
                mod_temp_file = os.path.join(mod_temp_folder, relative_path)
                os.makedirs(os.path.dirname(mod_temp_file), exist_ok=True)
                shutil.copy(file_path, mod_temp_file)

                mod_files[game_file] = mod_name

    # Move the mod files from the temporary folder to the game folder
    for root, _, files in os.walk(mod_temp_folder):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            relative_path = os.path.relpath(file_path, mod_temp_folder)
            game_file = os.path.join(game_folder, "Etrian Odyssey_Data", relative_path)
            shutil.copy(file_path, game_file)

    print("Modding completed successfully.")

elif option == "2":
    # Uninstall Mods
    print("Uninstalling Mods...")

    backup_folder = os.path.join(game_folder, "Backup")

    for root, _, files in os.walk(backup_folder):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            relative_path = os.path.relpath(file_path, backup_folder)
            game_file = os.path.join(game_folder, "Etrian Odyssey_Data", relative_path)

            if os.path.isfile(game_file):
                print("Restoring file", game_file)
                shutil.copy(file_path, game_file)

    print("Mod uninstallation completed successfully.")

elif option == "3":
    # Blacklist Mods
    print("Blacklisting Mods...")
    # Add code to blacklist mods here

else:
    print("Invalid option. Exiting...")
