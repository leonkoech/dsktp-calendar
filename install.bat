#!/bin/bash

# Function to check if Python is installed
check_python() {
    if command -v python3 >/dev/null 2>&1; then
        echo "Python is already installed."
    else
        echo "Please install Python manually from https://www.python.org/downloads/ and add it to PATH."
        # exit 1
    fi
}

# Function to install Python packages using pip
install_requirements() {
    echo "Installing required Python packages..."
    pip3 install -r requirements.txt
}

run_application(){

    @echo off
    rem Activate the virtual environment
    call \venv\Scripts\activate

    rem Run the Python script
    python \main.py

    rem Deactivate the virtual environment (optional)
    deactivate
}

# Main function
main() {
    check_python
    install_requirements
    run_application

    echo "Installation completed successfully."
}

# Call the main function
main
