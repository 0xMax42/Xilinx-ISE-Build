#!/bin/bash

# 🧠 Show help message
function show_help() {
    echo "Usage: $0 [-d device] [-i index] TopModuleName"
    echo
    echo "Arguments:"
    echo "  -d <device>   Name of the USB device (e.g., DOnbUsb), optional (default: DOnbUsb)"
    echo "  -i <index>    Interface index, optional (default: 0)"
    echo "  TopModule     Name of the top module (e.g., VGATimingGenerator)"
    exit 1
}

# 🔧 Default values
DEVICE="DOnbUsb"
INDEX=0

# 🧩 Parse arguments
while [[ "$1" =~ ^- ]]; do
    case "$1" in
        -d)
            shift
            DEVICE="$1"
            ;;
        -i)
            shift
            INDEX="$1"
            ;;
        -h|--help)
            show_help
            ;;
        *)
            echo "❌ Unknown option: $1"
            show_help
            ;;
    esac
    shift
done

# 📛 Get top module name
TOPMODULE="$1"

if [ -z "$TOPMODULE" ]; then
    echo "❌ Error: No top module specified."
    show_help
fi

# 📂 Path to bitstream file
BITFILE="working/${TOPMODULE}.bit"

# 📡 Flashing function
function flash_bitstream() {
    echo "⚡ Flashing bitstream to device $DEVICE, index $INDEX..."
    yes Y | djtgcfg prog -d "$DEVICE" -i "$INDEX" -f "$BITFILE"
}

# 🧹 Cleanup on Ctrl+C
function cleanup() {
    echo
    echo "👋 Terminated. Auto-flashing is no longer active."
    exit 0
}
trap cleanup SIGINT

# 🔍 Initial check
if [ -f "$BITFILE" ]; then
    echo "📦 Bitstream file $BITFILE found. Starting initial flash..."
    flash_bitstream
    echo "✅ Initial flash completed. Waiting for changes..."
else
    echo "⚠️  Bitstream file $BITFILE does not exist yet. Waiting for initial creation..."
fi

echo "👂 Monitoring $BITFILE for changes... (Press Ctrl+C to exit)"

# ♻️ Infinite watch loop
while true; do
    inotifywait -e close_write "$BITFILE" >/dev/null 2>&1
    echo "🌀 Change detected. Waiting 3 second..."
    sleep 3
    flash_bitstream
    echo "✅ Done. Waiting for next change..."
done
