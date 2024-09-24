
# Desktop Controller Bot

This project is a Desktop Controller Bot using Python and the Telegram Bot API. It allows you to control your desktop through various commands sent via a Telegram bot, including mouse clicks, scrolling, typing, and more.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Features](#features)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

1. **Python 3.6+**: This project requires Python 3.6 or higher.
   - You can download Python from [here](https://www.python.org/downloads/).

2. **Pip**: Python's package installer.
   - It usually comes bundled with Python, but you can install or upgrade it using:
     ```bash
     python -m ensurepip --upgrade
     ```

3. **Telegram Bot Token**: You need a Telegram bot token to run this application.
   - You can get this token by creating a bot with [BotFather](https://t.me/BotFather) on Telegram.

## Installation

1. **Clone the Repository:**
   Clone this repository to your local machine using:
   ```bash
   git clone https://github.com/your-username/your-repository.git
   ```
   Replace `your-username` and `your-repository` with your actual GitHub username and repository name.

2. **Navigate to the Project Directory:**
   ```bash
   cd your-repository
   ```

3. **Install Required Packages:**
   Install the required Python packages using `pip`:
   ```bash
   pip install -r requirements.txt
   ```
   Ensure that your `requirements.txt` file includes the following dependencies:
   ```txt
   pyautogui
   pyTelegramBotAPI
   Pillow
   tkinter
   ```

   You may need to install Tkinter separately, depending on your system:
   - For **Windows**: Tkinter is included with Python.
   - For **Linux**: You can install it using:
     ```bash
     sudo apt-get install python3-tk
     ```
   - For **macOS**: Tkinter is included with Python, but you may need XQuartz.

4. **Create the Required Files:**
   - Create a `data.json` file in the project directory to store your Telegram bot token:
     ```json
     {
       "token": "YOUR_TELEGRAM_BOT_TOKEN"
     }
     ```
   - Replace `YOUR_TELEGRAM_BOT_TOKEN` with your actual bot token.

5. **Set Permissions (Linux/macOS):**
   - If you are using Linux or macOS, ensure the script has the necessary permissions:
     ```bash
     chmod +x your-script.py
     ```

## Configuration

1. **Telegram Bot Token:**
   - Open the `data.json` file and replace the placeholder with your actual Telegram bot token.

2. **Screen Resolution:**
   - The script uses your screen's resolution to position the window and execute commands accurately. It automatically detects your screen resolution, but you can modify the resolution settings in the script if needed.

## Usage

1. **Run the Application:**
   - To start the application, execute the following command:
     ```bash
     python your-script.py
     ```
   - This will launch a Tkinter window where you can enter your Telegram bot token.

2. **Telegram Commands:**
   - Once the bot is running, you can send various commands to it from your Telegram chat. Some of the supported commands include:
     - `/LEFT_CLICK`: Simulate a left mouse click.
     - `/RIGTH_CLICK`: Simulate a right mouse click.
     - `/SCROLL_UP`: Scroll up.
     - `/SCROLL_DOWN`: Scroll down.
     - `/TYPE [your_text]`: Type the specified text.

## Features

- **Mouse Control**: Left click, right click, and double click.
- **Keyboard Control**: Type, press enter, backspace, delete, and more.
- **Scrolling**: Scroll up and down.
- **Screenshot**: Take a screenshot of the current screen.
- **Image Recognition**: Find a target on the screen based on color.

## Troubleshooting

- **Application Freezing**: If the application freezes, ensure that the `pyautogui` fail-safe feature is not triggered by moving the mouse to the top-left corner of the screen.
- **Permission Issues**: If you are on macOS, make sure to grant accessibility permissions to Python in `System Preferences > Security & Privacy > Accessibility`.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
