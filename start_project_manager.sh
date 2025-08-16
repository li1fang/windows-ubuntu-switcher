#!/bin/bash

# Windows/Ubuntu Switcher Project Manager
# A comprehensive tool for managing your dual-boot switching project

echo "============================================================"
echo "🚀 Windows/Ubuntu Switcher Project Manager"
echo "============================================================"
echo "A comprehensive tool for managing your dual-boot switching project"
echo "============================================================"
echo

echo "🔍 Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "❌ Python is not installed or not in PATH"
        echo "Please install Python 3.6+ from https://www.python.org/"
        echo
        read -p "Press Enter to continue..."
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo "✅ Python found: $($PYTHON_CMD --version)"
echo

echo "🚀 Starting Project Manager..."
echo

$PYTHON_CMD scripts/start_here.py

echo
echo "👋 Project Manager finished"
read -p "Press Enter to continue..."
