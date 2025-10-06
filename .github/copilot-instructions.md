# Copilot Instructions for Prototype Repository

## Overview
This project integrates ESP32 microcontroller(s) with a Python Flask server for data collection and communication. It is organized for rapid prototyping of physiological data workflows, with a focus on GSR and PPG datasets.

## Architecture
- **ESP32 Firmware (`esp32/esp32wifi.ino`)**: Connects to Wi-Fi and sends a POST request with device status and IP to the Flask server on startup.
- **Flask Server (`server.py`)**: Listens for POST requests at `/data`, logs incoming JSON from ESP32, and responds with status.
- **Datasets (`datasets/gsr`, `datasets/ppg`)**: Contains CSV files for High/Low MWL (Mental Workload Level) for multiple participants (e.g., `p10h.csv`, `p10l.csv`).
- **Models (`models/`)**: Placeholder for future ML models or scripts (currently empty).
- **Misc (`code.py`)**: Example or scratch file (currently prints "HELLO").

## Developer Workflows
- **Run the Flask server**:  
  ```powershell
  python server.py
  ```
  The server listens on all interfaces at port 5000. Ensure your PC's IP matches the `serverName` in the ESP32 firmware.
- **ESP32 Communication**:  
  On ESP32 boot, it connects to Wi-Fi and sends a JSON payload to the Flask server. No continuous data streaming is implemented yet.
- **Dataset Usage**:  
  Data is organized by signal type (GSR/PPG), MWL level, and participant. Use these files for ML/data analysis scripts.

## Project Conventions
- **No test framework or build system is present.**
- **All IPs and credentials are hardcoded for prototyping.**
- **Data files are named as `pXX[h|l].csv` for participant and MWL level.**
- **No package management or requirements file yet.**

## Integration Points
- **ESP32 <-> Flask**: HTTP POST to `/data` with JSON body. Example payload:
  ```json
  {"status": "connected", "ip": "192.168.100.50"}
  ```
- **Datasets**: CSVs are not loaded by any script yet, but are intended for future ML/data processing.

## Key Files/Directories
- `esp32/esp32wifi.ino` — ESP32 Wi-Fi and HTTP logic
- `server.py` — Flask server for device communication
- `datasets/` — GSR and PPG data, organized by MWL and participant
- `models/` — Reserved for ML models/scripts

## Recommendations for AI Agents
- When adding new data processing, follow the dataset organization pattern.
- If implementing continuous ESP32 data streaming, update both firmware and server accordingly.
- Document any new dependencies or setup steps in a `README.md` or requirements file.
