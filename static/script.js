const video = document.getElementById('webcam-feed');
const birdVisionCanvas = document.getElementById('bird-vision-canvas');
const motionDetectionCanvas = document.getElementById('motion-detection-canvas');

navigator.mediaDevices
  .getUserMedia({ video: true })
  .then((stream) => {
    video.srcObject = stream;

    const contextBirdVision = birdVisionCanvas.getContext('2d');
    const contextMotionDetection = motionDetectionCanvas.getContext('2d');
    
    let prevFrame = null;

    const processFrame = () => {
      const width = video.videoWidth;
      const height = video.videoHeight;

      birdVisionCanvas.width = width;
      birdVisionCanvas.height = height;
      motionDetectionCanvas.width = width;
      motionDetectionCanvas.height = height;

      contextBirdVision.drawImage(video, 0, 0, width, height);
      
      // Implement bird vision effect here
      
      if (prevFrame) {
        contextMotionDetection.drawImage(video, 0, 0, width, height);
        const currentFrame = contextMotionDetection.getImageData(0, 0, width, height).data;
        
        // Implement motion detection logic here
        
        prevFrame = currentFrame;
      }
      
      requestAnimationFrame(processFrame);
    };

    processFrame();
  })
  .catch((error) => {
    console.error('Error accessing webcam:', error);
  });
