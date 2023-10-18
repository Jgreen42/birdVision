from flask import Flask, render_template, Response
from neon_edges import get_frames
import cv2

app = Flask(__name__)

# Initialize the webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

@app.route('/')
def index():
    return render_template('index.html')

def generate_frames():
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        bird_vision_frame, motion_frame = get_frames(frame)
        if bird_vision_frame is not None and motion_frame is not None:
            ret, buffer = cv2.imencode('.jpg', bird_vision_frame)
            if not ret:
                continue
            bird_vision_frame = buffer.tobytes()
            ret, buffer = cv2.imencode('.jpg', motion_frame)
            if not ret:
                continue
            motion_frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + bird_vision_frame + b'\r\n\r\n')
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + motion_frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)