# mkp224o GUI

A simple graphical interface for [`mkp224o`](https://github.com/cathugger/mkp224o), the vanity .onion address generator. This GUI is built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) and allows you to easily generate vanity Tor v3 addresses.

> **Note:** This GUI does not bundle `mkp224o`. You need to compile `./mkp224o` yourself and put the binary in the **same directory** as this Python script.

---

## Prerequisites

- Python 3
- `mkp224o` binary compiled and placed in the same folder as this script.

To install `mkp224o`, go to [`mkp224o`](https://github.com/cathugger/mkp224o) and follow the instructions there.

Copy the `mkp224o` binary to the same folder as this script.

---

## Installation

1. Clone or download this repository.
2. Navigate to the project directory.
3. Install required Python modules:

```bash
pip install customtkinter tk
```

---

## Running the GUI

Ensure the `mkp224o` binary is present in the same directory.

Then, run the GUI with:

```bash
python3 main.py
```

---

## Usage

1. Enter one or more space-separated words to use as vanity prefixes.
2. Choose the output folder where the resulting vanity onion keys will be saved.
3. Use the slider to select how many threads to use.
4. Optionally, enable or disable verbose output.
5. Click **Start** to begin the generation.

---

## Contributing

Pull requests are welcome!

If you'd like to add features or fix bugs, follow these steps:

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
5. Commit and push your branch.
6. Open a pull request.

Suggestions and improvements are appreciated!

![image](https://github.com/user-attachments/assets/0e351b6b-0cd8-4be5-8b88-56abbf6f9fbc)
