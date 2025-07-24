# HGDream_LinearStage

A Python-based control interface for a 2-axis Velmex linear stage system which holds the HGDream Hodoscope and MCP-Timing devices. This project includes both a serial controller and a live-updating GUI for manually moving and monitoring stage position.

## Features

- Serial communication with Velmex VXM or VP9000 via RS-232
- Homing and absolute coordinate movement
- Live Matplotlib visualization of stage movement and position
- GUI for interactive control
- Position tracking

## Requirements

- Python 3.7+
- `pyserial`
- `matplotlib`
- `tkinter` (standard with most Python distributions)

Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
- [Linear Stage User Manual (PDF) ](docs/User_Manual.pdf)
### Launch the GUI

```bash
python GUI.py 
```
When you run the GUI, you'll be prompted to enter your serial port (e.g., COM3). The interface allows you to:

Home the linear stage

Enter X/Y coordinates to move the stage

Visualize motion using a live plot

Reset the plot and position trace

Import the Controller Script into the GUI Script

```bash
python controller_VXM.py
```

or

```bash
python controller_VP9000.py
```

This will:

Initialize the VXM or VP9000 controller

Home both motors

Move the stage to an absolute position 

Move the stage to a relative position

If you want to run the GUI without any connection to a motor import: 

``` bash
python controller_dummy.py
```

and when prompted for port name type 'dummy'.

This will disable the valid port connection requirment. 

Both controller files will print the sent command which you can compare with the VXM or VP9000 user manuals 

- [Velmex VXM User Manual (PDF)](docs/vxm_user_manl.pdf)
- [Velmex VP9000 User Manual (PDF)](docs/vp9002_usrman.pdf)
