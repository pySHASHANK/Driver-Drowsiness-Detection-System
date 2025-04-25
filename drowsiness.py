import cv2
import serial
import time

# Connect to Arduino (change 'COMX' to the correct port)
try:
    arduino = serial.Serial('COM13', 9600)  # ← Replace 'COMX' with your Arduino's COM port (e.g., 'COM3', 'COM13')
    time.sleep(2)  # Wait for the serial connection to establish
    print(f"Successfully connected to Arduino on port {arduino.port}")
except serial.SerialException as e:
    print(f"Error connecting to Arduino: {e}")
    exit()

# Load Haar cascades for face and eye detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

cap = cv2.VideoCapture(0)  # Use 0 for the default webcam

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

score = 0
threshold = 5  # Number of frames without eyes to trigger alert

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame from webcam.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))
    eyes_detected = False

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=3, minSize=(20, 20))
        if len(eyes) > 0:
            eyes_detected = True
        break  # Only consider the first detected face

    if eyes_detected:
        score = max(0, score - 1)
        arduino.write(b'0')  # Eyes open → no alert
    else:
        score += 1
        if score > threshold:
            arduino.write(b'1')  # Eyes closed → alert
        else:
            arduino.write(b'0')

    cv2.imshow("Drowsiness Detection", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # Press ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
if 'arduino' in locals() and arduino.is_open:
    arduino.close()
    print("Serial port closed.")