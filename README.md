# Motion Detection & Notification System 🎥🤖

## Description

The Motion Detection & Notification System is a Python program that detects motion in a video feed using OpenCV and sends notifications via Telegram when motion is detected. It leverages environment variables for configuration and includes basic error handling.

## Features

- **Motion Detection**: Utilizes OpenCV's background subtraction and contour detection to identify motion.
- **Telegram Notifications**: Sends photos and text messages to a configured Telegram chat when motion is detected or if the DVR is offline.
- **Error Handling**: Basic exception handling to notify via Telegram if something goes wrong.

## Installation

To set up this project, follow these steps:

1. **Clone the repository**:
   ```sh
   git clone https://github.com/gag3301v/python-motion-detection.git
   cd python-motion-detection
   ```

2. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   Create a `.env` file and set the following environment variables:
   ```
   TELEGRAM_API_ID=your_telegram_api_id
   TELEGRAM_API_HASH=your_telegram_api_hash
   TELEGRAM_CHAT_ID=your_telegram_chat_id
   DVR_URL=http://your_dvr_url
   ```

## Usage

Here’s how you can use the program:

1. **Run the Motion Detection Script**:
   ```sh
   python motion_detection.py
   ```

2. **Example Code Snippet**:
   ```python
   from motion_detector import MotionDetector, TelegramNotifier

   # Initialize classes
   motion_detector = MotionDetector()
   telegram_notifier = TelegramNotifier()

   # Start motion detection loop
   while True:
       if motion_detector.detect_motion():
           telegram_notifier.send_notification("Motion detected!", "path/to/screenshot.jpg")
   ```

## Configuration

The script uses environment variables for configuration. Set the following in your `.env` file:

- `TELEGRAM_API_ID`: Your Telegram bot's API ID.
- `TELEGRAM_API_HASH`: Your Telegram bot's API hash.
- `TELEGRAM_CHAT_ID`: The chat ID where notifications will be sent.
- `DVR_URL`: URL of the DVR to monitor.

## Tests

This project does not include automated tests at this time. However, you can manually test motion detection and notification functionality by running the script and checking your Telegram chat.

## Project Structure

```
python-motion-detection/
├── .env.example
├── motion_detection.py
├── requirements.txt
└── README.md
```

- `motion_detection.py`: Main script for motion detection and notification.
- `requirements.txt`: List of project dependencies.
- `.env.example`: Example file to guide you on setting up environment variables.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeatureName`).
3. Make your changes and commit them (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeatureName`).
5. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Feel free to reach out if you have any questions or need further assistance! 🚀