#!/bin/bash

# Activate Python virtual environment if needed
# source /path/to/your/virtualenv/bin/activate

# Define the paths to your Python scripts
SCRIPT1="/Users/joeltikkanen/Documents/lsb/kaantaminen.py"
SCRIPT2="/Users/joeltikkanen/Documents/lsb/varikorjaus.py"

# Run the first Python script
echo "Running kaantaminen.py..."
python "$SCRIPT1"

# Check if the first script ran successfully
if [ $? -eq 0 ]; then
    echo "kaantaminen.py completed successfully."
else
    echo "kaantaminen.py encountered an error." >&2
    exit 1
fi

# Run the second Python script
echo "Running varikorjaus.py..."
python "$SCRIPT2"

# Check if the second script ran successfully
if [ $? -eq 0 ]; then
    echo "varikorjaus.py completed successfully."
else
    echo "varikorjaus.py encountered an error." >&2
    exit 1
fi

# Deactivate virtual environment if needed
# deactivate

echo "All scripts have been run successfully."

# run with command: chmod +x /Users/joeltikkanen/Documents/lsb/run_python_script.sh
