const video = document.getElementById('webcam-feed');
const canvas = document.getElementById('output-canvas');
const context = canvas.getContext('2d');

navigator.mediaDevices
  .getUserMedia({ video: true })
  .then((stream) => {
    video.srcObject = stream;
  })
  .catch((error) => {
    console.error('Error accessing webcam:', error);
  });

video.addEventListener('play', () => {
  const { videoWidth, videoHeight } = video;
  canvas.width = videoWidth;
  canvas.height = videoHeight;

  const bufferCanvas = document.createElement('canvas');
  bufferCanvas.width = videoWidth;
  bufferCanvas.height = videoHeight;
  const bufferContext = bufferCanvas.getContext('2d');

  const processFrame = () => {
    bufferContext.drawImage(video, 0, 0, videoWidth, videoHeight);
    const frame = bufferContext.getImageData(0, 0, videoWidth, videoHeight);


// Apply your bird vision effect here
const birdVisionEffect = (frame) => {
    const uv_filter = new cv.Mat();
    cv.cvtColor(frame, uv_filter, cv.COLOR_BGR2BGRA);
    const gray = new cv.Mat();
    cv.cvtColor(uv_filter, gray, cv.COLOR_BGR2GRAY);
    const edges = new cv.Mat();
    cv.Canny(gray, edges, 60, 150);
    const edge_color = new cv.Mat();
    cv.applyColorMap(edges, edge_color, cv.COLORMAP_JET);
    const edge_mask = new cv.Mat();
    cv.threshold(edges, edge_mask, 50, 255, cv.THRESH_BINARY);
    const non_edge_mask = new cv.Mat();
    cv.bitwise_not(edge_mask, non_edge_mask);
    const bird_vision_frame = new cv.Mat();
    cv.bitwise_and(uv_filter, uv_filter, bird_vision_frame, non_edge_mask);
    cv.add(bird_vision_frame, edge_color, bird_vision_frame);
    cv.cvtColor(bird_vision_frame, bird_vision_frame, cv.COLOR_BGRA2BGR);
  
    uv_filter.delete(); // Don't forget to release Mats to avoid memory leaks
    gray.delete();
    edges.delete();
    edge_color.delete();
    edge_mask.delete();
    non_edge_mask.delete();
    return bird_vision_frame;
  };
  

  // Apply your motion detection effect here
const motionDetectionEffect = (frame, prev_frame) => {
  const motion_frame = new cv.Mat();
  cv.cvtColor(frame, motion_frame, cv.COLOR_BGR2GRAY);

  if (prev_frame !== null) {
    const frame_diff = new cv.Mat();
    cv.absdiff(prev_frame, motion_frame, frame_diff);
    cv.threshold(frame_diff, frame_diff, 15, 255, cv.THRESH_BINARY);

    // You can further process frame_diff as needed
    // E.g., display it, calculate motion metrics, etc.

    frame_diff.delete(); // Release the Mat
  }

  return motion_frame;
};


    context.putImageData(frame, 0, 0);
    requestAnimationFrame(processFrame);
  };

  processFrame();
});

const frame = bufferContext.getImageData(0, 0, videoWidth, videoHeight);

// Apply bird vision effect
const birdVisionFrame = birdVisionEffect(frame);

// Apply motion detection effect
const motionDetectionFrame = motionDetectionEffect(frame, prev_frame);

// Update the canvas with the results
context.putImageData(birdVisionFrame, 0, 0); // Display the Bird Vision effect
// Additionally, you can display motionDetectionFrame if needed

requestAnimationFrame(processFrame);
