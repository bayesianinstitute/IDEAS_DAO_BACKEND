#!/bin/bash

# Function to run the Django server
run_server() {
    python3 manage.py runserver 0.0.0.0:8000
}

# Run the Django server function
run_server

# Ignore Ctrl+C signal
trap '' INT

# Loop to monitor and restart the server
while true; do
    # Sleep for a few seconds before checking again
    sleep 2

    # Check if the server process is running
    ps aux | grep "python3 manage.py runserver 0.0.0.0:8000" | grep -v "grep"
    
    # $? stores the exit status of the last command (grep)
    if [ $? -ne 0 ]; then
        echo "Server crashed. Restarting..."
        run_server
    fi
done
