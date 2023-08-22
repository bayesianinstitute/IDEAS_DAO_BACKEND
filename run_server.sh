#!/bin/bash

# Function to run the Django server
run_server() {
    python manage.py runserver
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
    ps aux | grep "python manage.py runserver" | grep -v "grep"
    
    # $? stores the exit status of the last command (grep)
    if [ $? -ne 0 ]; then
        echo "Server crashed. Restarting..."
        run_server
    fi
done
