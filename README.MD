# Python Environment Variable Loader

This Python script demonstrates motion detection using OpenCV and sends notifications via Telegram when motion is detected. It utilizes environment variables loaded from a `.env` file.

## Features

- **Motion Detection**: Detects motion in a video feed using OpenCV.
- **Telegram Notifications**: Sends notifications to a Telegram chat when motion is detected.
- **Dynamic Configuration**: Configuration such as the input video file and Telegram bot token can be set via environment variables.
- **Error Handling**: Handles errors gracefully and notifies via Telegram in case of exceptions.

## Installation

1. Clone this repository:

   ```bash
    git clone https://github.com/gaurav-321/python-motion-detection.git
    cd python-motion-detection
2. Install the required Python packages:
   ```python 
    pip install -r requirements.txt
3. Set up a .env file in the root directory with the following variables:
    ```
    INPUTVID=path/to/your/video.mp4
    BOT_TOKEN=your_telegram_bot_token
    CHAT_ID=your_telegram_chat_id
## Usage
Run the script using Python:
   ```python
    python motion_detection.py
   ```
## Contributing
Contributions are welcome! Please feel free to submit issues and pull requests.

## License
This project is licensed under the MIT License - see the LICENSE file for details.