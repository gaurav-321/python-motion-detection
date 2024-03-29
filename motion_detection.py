import threading
import time
import cv2
import numpy as np
import ping3 as ping3
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
inputvid = os.getenv("INPUTVID")
last_msg = time.time()
bot_token = os.getenv("BOT_TOKEN")
shut_time = 60


def send_photo(image):
    """Send a photo to the specified chat with an optional caption."""
    url = f'https://api.telegram.org/bot{bot_token}/sendPhoto'
    # Encode the image as a binary file in memory.
    _, img_encoded = cv2.imencode('.jpg', image)

    # Convert the encoded image to bytes.
    img_bytes = img_encoded.tobytes()

    # Create a dictionary with the photo data and chat_id.
    files = {'photo': ('image.jpg', img_bytes)}
    params = {
        'chat_id': os.getenv("CHAT_ID"),
        'caption': "Detected Motion at {}".format(time.ctime()),
    }

    response = requests.post(url, params=params, files=files)
    print(response.text)
    return response


def send_text(text):
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    params = {
        'chat_id': os.getenv("CHAT_ID"),
        'text': text,
    }
    res = requests.post(url, params=params)
    print(res.text)


def send_msg(photo):
    global last_msg
    if time.time() - last_msg > 10:
        # send telegram message
        threading.Thread(target=send_photo, args=(photo,)).start()
        print("Sending msg")
        last_msg = time.time()


class LimitedList:
    def __init__(self):
        self.items = []

    def add(self, item):
        if len(self.items) < 10:
            self.items.append(item)
        else:
            del self.items[0]
            self.items.append(item)

    def remove(self, item):
        if item in self.items:
            self.items.remove(item)
        else:
            print(f"{item} not found in the list.")

    def get_sum(self):
        return sum(self.items)


def dvr_online(ip_address="192.168.1.100", timeout=3):
    """
    Check if an IP address is pingable.

    Args:
        ip_address (str): The IP address to ping.
        timeout (float): Maximum time to wait for a response (in seconds).

    Returns:
        bool: True if the IP is reachable, False otherwise.
    """

    response_time = ping3.ping(ip_address)

    if response_time is not None:
        print(f"Host {ip_address} is reachable. Response time: {response_time} ms")
        return True
    else:
        print(f"Host {ip_address} is not reachable.")
        return False


def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # Left mouse button clicked
        print(f"Mouse clicked at (x={x}, y={y})")


"""cv2.namedWindow("frame")
cv2.setMouseCallback("frame", mouse_callback)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))"""


def merge_overlapping_contours(contours):
    merged_contours = []

    for contour in contours:
        if cv2.contourArea(contour) < 1200:
            continue  # Skip small contours

        # Check if this contour overlaps with any merged contour
        overlap = False
        for merged_contour in merged_contours:
            if cv2.contourArea(merged_contour) < 1500:
                continue  # Skip small merged contours

            # Use bounding rectangles to check for overlap (you can also use other methods)
            x1, y1, w1, h1 = cv2.boundingRect(contour)
            x2, y2, w2, h2 = cv2.boundingRect(merged_contour)

            if x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2:
                overlap = True
                break

        if not overlap:
            merged_contours.append(contour)

    return merged_contours


while True:
    if dvr_online():
        shut_time = 60
        send_text("Dvr is Online")
        try:
            cap = cv2.VideoCapture(inputvid)
            fgbg = cv2.createBackgroundSubtractorMOG2(
                history=200,  # Use 200 previous frames for the background model
                varThreshold=40,  # Set a lower threshold for foreground detection
                detectShadows=False
            )
            list_contour = LimitedList()
            val = 0
            while True:
                # Read a frame from the video feed
                ret, orig_img = cap.read()
                frame = orig_img.copy()
                # crop frame
                frame = frame[228:575, 550:780]
                if not ret:
                    break  # Break the loop if no frame is read (end of video)
                # Apply background subtraction to detect moving objects
                fgmask = fgbg.apply(frame)

                # Apply some morphological operations to clean up the mask
                fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel=None, iterations=4)
                # Find contours in the binary mask
                contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                contours = [contour for contour in contours if cv2.contourArea(contour) >= 800]
                # contours = merge_overlapping_contours(contours)
                list_contour.add(len(contours))
                if list_contour.get_sum() >= 5:
                    for contours in contours:
                        x, y, w, h = cv2.boundingRect(contours)
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
                    orig_img[228:575, 550:780] = frame
                    cv2.rectangle(orig_img, (550, 228), (780, 575), (0, 255, 0), 1)
                    send_msg(orig_img)
                cv2.imshow('frame', orig_img)

                # Press 'q' to exit the loop
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            # Release video capture and close all OpenCV windows
            cap.release()
            cv2.destroyAllWindows()

        except Exception as e:
            send_text("Got following error: " + str(e))
            continue
    else:
        send_text(f"Dvr is Offline, sleeping for {shut_time} seconds")
        time.sleep(shut_time)
        shut_time += 60
        continue
