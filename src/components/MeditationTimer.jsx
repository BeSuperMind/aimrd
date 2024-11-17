import React, { useState, useEffect, useRef } from 'react';
import useStore from '../utils/useStore';
import { useNavigate } from 'react-router-dom';
import testMusic from '../assets/test.mp3';
import testMusic2 from '../assets/test2.mp3';
import VideoStream from './VideoStream';
import VideoStream2 from './VideoStream2';

const MeditationTimer = () => {
  const sessionDuration = useStore((state) => state.sessionDuration);
  const music = useStore((state) => state.music);
  const [timeLeft, setTimeLeft] = useState(sessionDuration * 60);
  const [isRunning, setIsRunning] = useState(false);
  const [isMuted, setIsMuted] = useState(false);
  const navigate = useNavigate();
  const audioRef = useRef(null);

  // Mapping for music selection
  const musicFiles = {
    'Music 1': testMusic,
    'Music 2': testMusic2,
    'Silence': null,
  };

  // Initialize the audio file when 'Music 1' or 'Music 2' is selected
  useEffect(() => {
    if (music !== 'Silence' && musicFiles[music]) {
      if (!audioRef.current) {
        audioRef.current = new Audio(musicFiles[music]);
        audioRef.current.loop = true;
      }
    } else {
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current = null;
      }
    }

    return () => {
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current = null;
      }
    };
  }, [music]);

  // Update mute state of audio
  useEffect(() => {
    if (audioRef.current) {
      audioRef.current.muted = isMuted;
    }
  }, [isMuted]);

  // Timer logic
  useEffect(() => {
    let interval;
    if (isRunning && timeLeft > 0) {
      interval = setInterval(() => setTimeLeft((prev) => prev - 1), 1000);
    } else if (timeLeft === 0) {
      if (audioRef.current) audioRef.current.pause();
      navigate('/feedback');
    }
    return () => clearInterval(interval);
  }, [isRunning, timeLeft, navigate]);

  // Logic to play/pause music based on the timer state
  useEffect(() => {
    if (isRunning) {
      if (audioRef.current && audioRef.current.paused) {
        audioRef.current.play();
      }
    } else {
      if (audioRef.current && !audioRef.current.paused) {
        audioRef.current.pause();
      }
    }
  }, [isRunning]);

  // Format time for display
  const formatTime = (time) => {
    const minutes = Math.floor(time / 60);
    const seconds = time % 60;
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <button className="absolute top-6 left-6 text-2xl" onClick={() => navigate(-1)}>
        &larr;
      </button>
      <h1 className="text-2xl font-bold mb-4">Meditation Timer</h1>

      <div className="relative w-48 h-48 rounded-full overflow-hidden bg-gray-200 shadow-lg">
        <div
          className="absolute bottom-0 w-full bg-indigo-500"
          style={{
            height: `${(1 - timeLeft / (sessionDuration * 60)) * 100}%`,
            animation: isRunning
              ? `wave-rise ${(sessionDuration * 60)}s linear forwards`
              : 'none',
          }}
        ></div>
        <div className="absolute inset-0 flex items-center justify-center z-10">
          <span className="text-3xl font-semibold">{formatTime(timeLeft)}</span>
        </div>
      </div>

      <p className="text-xl mt-4">Song Title: {music}</p>

      <div className="flex gap-4 mt-6">
        {music !== 'Silence' && (
          <button onClick={() => setIsMuted(!isMuted)} className="text-indigo-500">
            {isMuted ? 'Unmute' : 'Mute'}
          </button>
        )}
        <button onClick={() => setIsRunning(!isRunning)} className="text-indigo-500">
          {isRunning ? 'Pause' : 'Start'}
        </button>
      </div>
      <div className='flex'>
        <VideoStream />
        <VideoStream2 />
      </div>
    </div>
  );
};

export default MeditationTimer;
