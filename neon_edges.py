import cv2
from flask import Flask, render_template, Response
from your_module import get_frames  # Import your frame processing function

app = Flask(__name)

# OpenCV camera capture
cap = cv2.VideoCapture(0)

def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break

        bird_vision_frame, motion_detection_frame = get_frames(frame)

        # Check if frames are not None
        if bird_vision_frame is not None and motion_detection_frame is not None:
            # Convert frames to JPEG format
            bird_vision_encoded = cv2.imencode('.jpg', bird_vision_frame)[1].tobytes()
            motion_detection_encoded = cv2.imencode('.jpg', motion_detection_frame)[1].tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + bird_vision_encoded + b'\r\n\r\n')
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + motion_detection_encoded + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main':
    app.run(debug=True)