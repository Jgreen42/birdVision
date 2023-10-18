import cv2
import numpy as np
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
            # You may need to encode the frames to base64 and send them to the template
            bird_vision_encoded = encode_image_to_base64(bird_vision_frame)
            motion_detection_encoded = encode_image_to_base64(motion_detection_frame)

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

if __name__ == '__main__':
    app.run(debug=True)


# import cv2
# import numpy as np

# def get_frames(frame):
#     # Bird Vision
#     uv_filter = frame.copy()
#     uv_filter[:, :, 2] += uv_filter[:, :, 1]
#     gray = cv2.cvtColor(uv_filter, cv2.COLOR_BGR2GRAY)
#     edges = cv2.Canny(gray, 60, 150)
#     edge_color = cv2.applyColorMap(edges, cv2.COLORMAP_JET)
#     _, edge_mask = cv2.threshold(edges, 50, 255, cv2.THRESH_BINARY)
#     non_edge_mask = cv2.bitwise_not(edge_mask)
#     bird_vision_frame = cv2.bitwise_and(frame, frame, mask=non_edge_mask)
#     bird_vision_frame += edge_color
#     bird_vision_rgb = cv2.cvtColor(bird_vision_frame, cv2.COLOR_BGR2RGB)

#     # Motion Detection
#     motion_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     if get_frames.prev_frame is not None:
#         frame_diff = cv2.absdiff(get_frames.prev_frame, motion_frame)
#         _, frame_diff = cv2.threshold(frame_diff, 15, 255, cv2.THRESH_BINARY)
#         return bird_vision_rgb, frame_diff

#     get_frames.prev_frame = motion_frame
#     return None, None

# get_frames.prev_frame = None