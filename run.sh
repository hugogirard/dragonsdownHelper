#!/bin/bash
# Quick start script for Dragons Down Adventure Journal

echo "🐉 Starting Dragons Down Adventure Journal..."
echo ""

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null
then
    echo "Streamlit not found. Installing dependencies..."
    pip install streamlit pandas
fi

# Run the application
streamlit run main.py
