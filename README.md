# TFmini-i LiDAR Sensor Simulation (Modbus RTU)

![Project Status](https://img.shields.io/badge/status-completed-green)
![Python](https://img.shields.io/badge/python-3.13%2B-blue)
![Platform](https://img.shields.io/badge/hardware-STM32F4_Discovery-orange)

## 📖 Overview

This project implements a **Hardware-in-the-Loop (HIL)** simulation for the **TFmini-i LiDAR Sensor** using the Modbus RTU protocol. 

The system consists of two main components:
1.  **Master (PC/Python):** A Python-based control software that acts as the Modbus Master, sending requests (frames) to the sensor.
2.  **Slave Mock (STM32F4):** An STM32F4 Discovery board acting as the sensor emulator. It receives UART commands, parses Modbus frames, simulates sensor logic (state machine), and responds with appropriate data packets.

This setup allows for testing communication drivers and protocol handling without needing the actual expensive sensor hardware.

## 🚀 Key Features

* **Full Modbus RTU Implementation:** Handles Frame Header, Function Codes, Data Payload, and CRC-16 checksums.
* **Sensor Simulation:**
    * **Read Distance:** Returns simulated distance values.
    * **Read Signal Strength:** Returns distance + signal confidence.
    * **Configuration:** Supports changing Slave ID, Working Mode and Frame Rate.
    * **State Persistence:** Simulates "Save Settings" and "System Reset" behavior.
* **Robust Error Handling:** Python script handles Timeouts, CRC Mismatches, and Invalid Frame Formats.
* **Visual Logging:** Color-coded terminal output (TX/RX/Error) for easy debugging.

## 🛠️ Hardware Architecture

### Requirements
* **Host:** PC/Laptop running Python.
* **Microcontroller:** STM32F4 Discovery (STM32F407VGT6).
* **Interface:** USB-to-TTL Serial Converter (Prolific).
* **Wiring:** Jumper wires.

### Pinout Configuration (UART)

| PC (USB-TTL) | STM32F4 Discovery | Description |
| :--- | :--- | :--- |
| **TX** | **PB7 (RX)** | PC Transmits -> STM32 Receives |
| **RX** | **PB6 (TX)** | PC Receives <- STM32 Transmits |
| **GND** | **GND** | Common Ground (Crucial) |
| 3.3V | 3.3V | Power |

*Note: The UART Pins (PB6/PB7) may vary depending on your specific STM32 firmware configuration.*

---
## 💻 Software Prerequisites

### Master Side (PC)
* Python 3.13.5
* Virtual Environment (recommended: `pipenv` or `venv`)
* Dependencies:
    * `pyserial`
    * `termcolor`

### Slave Side (STM32)
* STM32CubeIDE (for firmware compilation)
* HAL Library
## 📡 Modbus RTU Frame Structure

The communication follows the standard Modbus RTU protocol over RS-485. Both the Master (PC) and Slave (Sensor) must adhere to this frame structure.

### 1. Request Frame (Master -> Slave)

This is the format sent by your Python script to the sensor.

| Byte Index | Field | Length | Description |
| :--- | :--- | :--- | :--- |
| **0** | **Slave ID** | 1 Byte | [cite_start]Target sensor address (Default: `0x01`)[cite: 138]. |
| **1** | **Function Code** | 1 Byte | [cite_start]`0x03` (Read) or `0x06` (Write)[cite: 156]. |
| **2-3** | **Register Address** | 2 Bytes | [cite_start]The memory address to read/write (**Big Endian**)[cite: 149]. |
| **4-5** | **Data / Length** | 2 Bytes | [cite_start]Value to write or number of registers to read (**Big Endian**)[cite: 149]. |
| **6-7** | **CRC-16** | 2 Bytes | [cite_start]Checksum for error detection (**Little Endian**)[cite: 149]. |

**Example: Request to Read Distance**
`01 03 00 00 00 01 84 0A`
* **01**: Slave ID
* **03**: Function (Read)
* **00 00**: Start Address (Distance Register)
* **00 01**: Length (Read 1 Register)
* **84 0A**: CRC Checksum


### 2. Response Frame (Slave -> Master)

This is the format returned by the STM32 (Mock Sensor) to your Python script.

| Byte Index | Field | Length | Description |
| :--- | :--- | :--- | :--- |
| **0** | **Slave ID** | 1 Byte | [cite_start]Address of the responding sensor[cite: 151]. |
| **1** | **Function Code** | 1 Byte | [cite_start]Echoes the requested function code[cite: 151]. |
| **2** | **Byte Count** | 1 Byte | [cite_start]Number of data bytes following (Only for Read `0x03`)[cite: 151]. |
| **3...N** | **Data Payload** | N Bytes | [cite_start]The requested sensor data (**Big Endian**)[cite: 160]. |
| **N+1...N+2** | **CRC-16** | 2 Bytes | [cite_start]Checksum for error detection (**Little Endian**)[cite: 151]. |

**Example: Response for Distance (700 cm)**
`01 03 02 02 BC B8 95`
* **01**: Slave ID
* **03**: Function (Read)
* **02**: Byte Count (2 bytes of data follow)
* **02 BC**: Distance Data (`0x02BC` = 700 cm)
* **B8 95**: CRC Checksum
---

### ⚠️ Protocol Implementation Notes

* **Endianness Mix:**
    * **Data Content (Distance, Signal, Address)** is sent in **Big Endian** (High Byte First).
    * **CRC Checksum** is sent in **Little Endian** (Low Byte First).
* **Write Response:** For Write commands (`0x06`), the sensor echoes back the exact Request frame as an acknowledgement.
* **Slave ID Changes:** If the Slave ID is modified (Register `0x0085`), the new ID takes effect only after a **Save & Reboot** operation. The Master **must** update the target ID in its requests to match the new configuration; the old ID will no longer be recognized.
---

## 📦 Installation & Setup
### 1. Clone the Repository
```bash
git clone [https://github.com/yourusername/tfmini-simulation.git](https://github.com/yourusername/tfmini-simulation.git)
cd tfmini-simulation
```
### 2. Python Environment Setup
-  Choose `master_simulation` directory
```
cd master_simulation
```
- Run Virtual environtment pipenv

```
pipenv shell
pipenv install
```

### 3. Flash the Firmware
1. Open the `slave_simulation/` folder in STM32CubeIDE.
2. Build the project.
3. Connect the STM32F4 Discovery via USB (ST-LINK).
4. Run/Debug to flash the `.elf` file to the board.
---
## ⚙️ Communication Parameters
The simulation adheres strictly to the TFmini-i default settings:

* **Baud Rate:** 115200 bps
* **Data Bits:** 8
* **Parity:** None
* **Stop Bits:** 1
---
## 🏃 Usage Guide
1. **Connect Hardware:** Ensure the USB-TTL is plugged into the PC and wired correctly to the STM32.

2. **Check Port:** Verify the COM port (Windows) or /dev/ttyUSB* (Linux/Mac) in serial_config.py.
---
## 📖 Command Definitions for Simulation

This section defines the exact Hexadecimal sequences used in the simulation. The **Master (Python Script)** sends the **REQ** frames, and the **Slave (STM32)** Mock as `TFmini-i` must reply with the corresponding **RES** frames to pass the test.

### 1. GET DISTANCE

* **Open:** `master_simulation/get_distance.py`
    * set `SLAVE_ID = b'\x01'` 
    * run program `python get_distance.py` 

| Type | Hex Frame |
| :--- | :--- |
| **REQ** | `01 03 00 00 00 01 84 0A` |
| **RES** | `01 03 02 02 BC B8 95` |

* **Description:** Reads the distance value from the sensor.
* **Target Register:** `0x0000` (Length: 1 Word)
* **Expected Data:** Distance = 700 cm (`0x02BC`)



---

### 2. GET DISTANCE AND SIGNAL STRENGTH
* **Open:** `master_simulation/get_distance_signal.py`
    * set `SLAVE_ID = b'\x01'` 
    * run program `python get_distance_signal.py`

| Type | Hex Frame |
| :--- | :--- |
| **REQ** | `01 03 00 00 00 02 C4 0B` |
| **RES** | `01 03 04 00 64 03 E8 BB 52` |
* **Description:** Reads both distance and signal confidence level.
* **Target Register:** `0x0000` (Length: 2 Words)
* **Expected Data:** Distance = 100 cm (`0x0064`), Signal = 1000 (`0x03E8`)
---

### 3. SET FRAME RATE
* **Open:** `master_simulation/set_frame_rate.py`
    * set `SLAVE_ID = b'\x01'` and `FRAME_RATE = 10`
    * run program `python set_frame_rate.py`

| Type | Hex Frame |
| :--- | :--- |
| **REQ** | `01 06 00 86 00 0A E8 24` |
| **RES** | `01 06 00 86 00 0A E8 24` |

* **Description:** Sets the internal update frequency of the sensor.
* **Target Register:** `0x0086`
* **Value:** 10 Hz (`0x000A`)
---
### 4. SET SLAVE ID
* **Open:** `master_simulation/set_new_slave_id.py`
    * set `CURRENT_SLAVE_ID = b'\x01'` and `NEW_SLAVE_ID = b'\x03'`
    * run program `python set_new_slave_id.py`

**Step 1: Write New ID**
| Type | Hex Frame |
| :--- | :--- |
| **REQ** | `01 06 00 85 00 03 D8 22` |
| **RES** | `01 06 00 85 00 03 D8 22` |

**Step 2: Save Configuration (Required to apply change)**
| Type | Hex Frame |
| :--- | :--- |
| **REQ** | `01 06 00 80 00 00 88 22` |
| **RES** | `01 06 00 80 00 00 88 22` |

* **Description:** Changes the sensor's Modbus address (Slave ID).
* **Target Register:** `0x0085`
* **Action:** Change ID from `0x01` to `0x03`, then Save Settings.
---

### 5. SET WORKING MODE
* **Open:** `master_simulation/set_working_mode.py`
    * set `SLAVE_ID = b'\x01'` and `WORKING_MODE = 1`
    * run program `python set_working_mode.py`

**Step 1: Write Trigger Mode**
| Type | Hex Frame |
| :--- | :--- |
| **REQ** | `01 06 00 87 00 01 F8 23` |
| **RES** | `01 06 00 87 00 01 F8 23` |

**Step 2: Save Configuration**
| Type | Hex Frame |
| :--- | :--- |
| **REQ** | `01 06 00 80 00 00 88 22` |
| **RES** | `01 06 00 80 00 00 88 22` |
* **Description:** Toggles between Continuous Mode `(0x00)` and Trigger Mode `(0x01)`.
* **Target Register:** `0x0087`
* **Value:** `0x01` (Trigger Mode)
* **Action:** Write Mode, then Save Settings.
---

### 6. GET FIRMWARE VERSION
* **Open:** `master_simulation/get_firmware_ver.py`
    * set `SLAVE_ID = b'\x01'`
    * run program `python get_firmware_ver.py`

| Type | Hex Frame |
| :--- | :--- |
| **REQ** | `01 03 00 06 00 02 24 0A` |
| **RES** | `01 03 04 00 03 05 0A 89 64` |

* **Description:** Retrieves the firmware version from the sensor.
* **Target Register:** `0x0006` (Length: 2 Words)
* **Expected Data:** Version 3.5.10 (main version :`0x03`, sub-version `0x05`, revised version`0x0A`) 
---

### 7. RESET SENSOR

* **Open:** `master_simulation/reset_sensor.py`
    * set `CURRENT_SLAVE_ID = b'\x01'`
    * run program `python reset_sensor.py`

| Type | Hex Frame |
| :--- | :--- |
| **REQ** | `01 06 00 89 00 00 58 20` |
| **RES** | `01 06 00 89 00 00 58 20` | 
* **Description:** Restores the sensor to factory default settings.
* **Target Register:** `0x0089`
---