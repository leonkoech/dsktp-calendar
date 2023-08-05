#!/bin/bash

# Function to check if Python is installed
check_python() {
    if command -v python3 >/dev/null 2>&1; then
        echo "Python is already installed."
    else
        echo "Installing Python..."
        # Replace the installation command with the appropriate one for your system
        # For example, on Ubuntu, you can use: sudo apt-get install python3
        # On macOS with Homebrew: brew install python3
        # On Windows: Download the Python installer from the official website and run it.
        # Make sure to add Python to the PATH.
        # The script should exit if Python installation fails.
        # Uncomment and use the appropriate command for your system:

        # sudo apt-get install python3
        # brew install python3
        # echo "Please install Python manually from https://www.python.org/downloads/ and add it to PATH."
        # exit 1
    fi
}

# Function to install Python packages using pip
install_requirements() {
    echo "Installing required Python packages..."
    pip3 install -r requirements.txt
}

# Main function
main() {
    check_python
    install_requirements

    echo "Installation completed successfully."
}

# Call the main function
main
