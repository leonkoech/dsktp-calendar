# Function to check if Python is installed
function Check-Python {
    if (Get-Command python3 -ErrorAction SilentlyContinue) {
        Write-Output "Python is already installed."
    } else {
        Write-Output "Please install Python manually from https://www.python.org/downloads/ and add it to PATH."
        # Exit with an error code if needed: exit 1
    }
}

# Function to install Python packages using pip
function Install-Requirements {
    Write-Output "Installing required Python packages..."
    pip3 install -r requirements.txt
}

# Function to run the application
function Run-Application {
    # Activate the virtual environment
    & .\venv\Scripts\Activate

    # Run the Python script
    python .\main.py

    # Deactivate the virtual environment (optional)
    # Deactivate
}

# Main function
function Main {
    # Uncomment the following lines if you want to call the functions
    # Check-Python
    # Install-Requirements
    Write-Output "Installation completed successfully."

    Run-Application

    Write-Output "Application ran successfully."
}

# Call the main function
Main
