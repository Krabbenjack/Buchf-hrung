#!/bin/bash
# Setup script for Buchführung application

echo "============================================"
echo "Buchführung - Setup Script"
echo "============================================"
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "Error: Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies."
    exit 1
fi

echo ""
echo "============================================"
echo "Setup completed successfully!"
echo "============================================"
echo ""
echo "To run the application:"
echo "  python src/main.py"
echo ""
echo "To create sample data:"
echo "  python create_sample_data.py"
echo ""
echo "To run tests:"
echo "  python test_functionality.py"
echo ""
