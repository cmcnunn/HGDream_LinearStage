# HGDream_LinearStage

A Python-based control interface for a 2-axis Velmex linear stage system. This project includes both a serial controller and a live-updating GUI for manually moving and monitoring stage position.

## Features

- Serial communication with Velmex VXM or VP9000 via RS-232
- Homing and absolute coordinate movement
- Live Matplotlib visualization of stage movement and position
- GUI for interactive control
- Real-time position tracking with support for trails and arrows

## Requirements

- Python 3.7+
- `pyserial`
- `matplotlib`
- `tkinter` (standard with most Python distributions)

Install dependencies:
```bash
pip install -r requirements.txt
