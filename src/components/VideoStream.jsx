import React, { useEffect, useRef, useState } from "react";

const VideoStream = () => {
    const [socket, setSocket] = useState(null);
    const [processedFrame, setProcessedFrame] = useState(null);
    const [audio, setAudio] = useState(null);
    const videoRef = useRef(null);
    const canvasRef = useRef(null);
    
    const hasSpokenIntro = useRef(false); // Flag to check if the intro has been spoken

    // TTS function to speak the provided text
    const speak = (text) => {
        if ("speechSynthesis" in window) {
            const synth = window.speechSynthesis;
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = "en-US";
            synth.speak(utterance);
        } else {
            console.error("Text-to-Speech not supported in this browser.");
        }
    };

    // Speak initial message when the component mounts
    useEffect(() => {
        // Check if the intro has already been spoken
        if (!hasSpokenIntro.current) {
            const initialMessage = "Please close your eyes, cross your feet at the ankle, clasp your fingers and place it on your lap and observe your simple, natural breath";
            speak(initialMessage);
            hasSpokenIntro.current = true; // Set flag to true after speaking the intro
        }
    }, []); // This runs only once when the component is first mounted

    useEffect(() => {
        const ws = new WebSocket("ws://192.168.77.121:8000/ws/deep_learning_analysis/");
        setSocket(ws);

        ws.onopen = () => console.log("WebSocket connected");
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.processed_frame) {
                setProcessedFrame(data.processed_frame);
            }

            if (data.Audio && data.Audio.trim()) {
                setAudio(data.Audio);
            } else {
                setAudio(null);
            }
        };

        ws.onclose = () => console.log("WebSocket disconnected");
        ws.onerror = (error) => console.error("WebSocket error:", error);

        return () => ws.close();
    }, []);

    useEffect(() => {
        if (audio) {
            speak(audio); // Trigger TTS whenever `audio` state updates
        }
    }, [audio]); // Run this effect whenever the `audio` state changes

    useEffect(() => {
        const setupVideoStream = async () => {
            const video = videoRef.current;
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ video: true });
                if (video) {
                    video.srcObject = stream;
                    video.onloadedmetadata = () => {
                        // Ensure playback only starts after metadata is loaded
                        video.play().catch((err) => console.error("Error playing video:", err));
                    };
                }
            } catch (err) {
                console.error("Error accessing webcam:", err);
            }
        };

        setupVideoStream();
    }, []);

    const sendFrame = () => {
        const video = videoRef.current;
        const canvas = canvasRef.current;

        if (video && canvas) {
            const context = canvas.getContext("2d");
            context.drawImage(video, 0, 0, canvas.width, canvas.height);

            canvas.toBlob((blob) => {
                if (blob) {
                    const reader = new FileReader();
                    reader.onload = () => {
                        const frameData = reader.result.split(",")[1];
                        if (socket && socket.readyState === WebSocket.OPEN) {
                            socket.send(JSON.stringify({ frame_data: frameData }));
                        }
                    };
                    reader.readAsDataURL(blob);
                }
            }, "image/jpeg");
        }
    };

    useEffect(() => {
        const interval = setInterval(() => {
            if (videoRef.current && socket && socket.readyState === WebSocket.OPEN) {
                sendFrame();
            }
        }, 1000); // Sending frame every 1000 ms
        return () => clearInterval(interval);
    }, [socket]);

    return (
        <div>
            <video
                ref={videoRef}
                autoPlay
                playsInline
                muted
                style={{ display: "none", width: "640px", height: "480px" }}
            />
            <canvas ref={canvasRef} width="640" height="480" style={{ display: "none" }}></canvas>
            {processedFrame && (
                <img
                    src={`data:image/jpeg;base64,${processedFrame}`}
                    alt="Processed frame"
                />
            )}
            {/* {audio && <p>{audio}</p>} */}
        </div>
    );
};

export default VideoStream;
