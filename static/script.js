const video = document.getElementById('video-stream');

function startVideo() {
    fetch('/video_feed')
        .then(response => {
            const reader = response.body.getReader();
            const decoder = new TextDecoder('utf-8');

            return new ReadableStream({
                start(controller) {
                    return pump();

                    function pump() {
                        return reader.read().then(({ done, value }) => {
                            if (done) {
                                controller.close();
                                return;
                            }
                            controller.enqueue(value);
                            return pump();
                        });
                    }
                }
            });
        })
        .then(stream => new Response(stream))
        .then(response => response.blob())
        .then(blob => {
            const url = URL.createObjectURL(blob);
            video.src = url;
        });
}

startVideo();