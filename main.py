<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Audio Recorder and Transcription</title>
</head>
<body>
    <h1>Record Audio and Transcribe</h1>

    <button id="start-record">Start Recording</button>
    <button id="stop-record" disabled>Stop Recording</button>

    <h2>Recorded Audio:</h2>
    <audio id="audio-playback" controls></audio>

    <h2>Transcription and Summary:</h2>
    <button id="transcribe" disabled>Transcribe</button>

    <h3>Transcription:</h3>
    <pre id="transcription"></pre>

    <h3>Summary:</h3>
    <pre id="summary"></pre>

    <script>
        let mediaRecorder;
        let audioChunks = [];
        let audioBlob;

        const startRecordBtn = document.getElementById('start-record');
        const stopRecordBtn = document.getElementById('stop-record');
        const transcribeBtn = document.getElementById('transcribe');
        const audioPlayback = document.getElementById('audio-playback');
        const transcriptionElem = document.getElementById('transcription');
        const summaryElem = document.getElementById('summary');

        // Start recording audio
        startRecordBtn.addEventListener('click', async () => {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);
            audioChunks = [];

            mediaRecorder.ondataavailable = (event) => {
                audioChunks.push(event.data);
            };

            mediaRecorder.onstop = () => {
                audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                const audioURL = URL.createObjectURL(audioBlob);
                audioPlayback.src = audioURL;
                transcribeBtn.disabled = false;
            };

            mediaRecorder.start();
            startRecordBtn.disabled = true;
            stopRecordBtn.disabled = false;
        });

        // Stop recording
        stopRecordBtn.addEventListener('click', () => {
            mediaRecorder.stop();
            stopRecordBtn.disabled = true;
            startRecordBtn.disabled = false;
        });

        // Transcribe the recorded audio
        transcribeBtn.addEventListener('click', async () => {
            const formData = new FormData();
            formData.append('file', audioBlob, 'recording.wav');

            try {
                const response = await fetch('http://127.0.0.1:8001/transcribe/', {
                    method: 'POST',
                    body: formData
                });

                if (response.ok) {
                    const data = await response.json();
                    transcriptionElem.textContent = data.transcription;
                    summaryElem.textContent = data.summary;
                } else {
                    transcriptionElem.textContent = "Error: Unable to transcribe.";
                    summaryElem.textContent = "";
                }
            } catch (error) {
                transcriptionElem.textContent = "Error: " + error.message;
                summaryElem.textContent = "";
            }
        });
    </script>
</body>
</html>
