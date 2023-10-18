import cv2
import numpy as np

def get_frames(frame):
    # Bird Vision
    uv_filter = frame.copy()
    uv_filter[:, :, 2] += uv_filter[:, :, 1]
    gray = cv2.cvtColor(uv_filter, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 60, 150)
    edge_color = cv2.applyColorMap(edges, cv2.COLORMAP_JET)
    _, edge_mask = cv2.threshold(edges, 50, 255, cv2.THRESH_BINARY)
    non_edge_mask = cv2.bitwise_not(edge_mask)
    bird_vision_frame = cv2.bitwise_and(frame, frame, mask=non_edge_mask)
    bird_vision_frame += edge_color
    bird_vision_rgb = cv2.cvtColor(bird_vision_frame, cv2.COLOR_BGR2RGB)

    # Motion Detection
    motion_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if get_frames.prev_frame is not None:
        frame_diff = cv2.absdiff(get_frames.prev_frame, motion_frame)
        _, frame_diff = cv2.threshold(frame_diff, 15, 255, cv2.THRESH_BINARY)
        return bird_vision_rgb, frame_diff

    get_frames.prev_frame = motion_frame
    return None, None

get_frames.prev_frame = None