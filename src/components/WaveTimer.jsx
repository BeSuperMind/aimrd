import React, { useState, useEffect } from 'react';

const WaveTimer = () => {
  const totalDuration = 2 * 60; // 2 minutes in seconds
  const [timeLeft, setTimeLeft] = useState(totalDuration);
  const [running, setRunning] = useState(false);

  useEffect(() => {
    let interval = null;
    if (running && timeLeft > 0) {
      interval = setInterval(() => {
        setTimeLeft((prevTime) => prevTime - 1);
      }, 1000);
    } else if (timeLeft === 0) {
      setRunning(false);
    }

    return () => clearInterval(interval);
  }, [running, timeLeft]);

  const handleStart = () => {
    if (!running) setRunning(true);
  };

  const formatTime = (time) => {
    const minutes = Math.floor(time / 60);
    const seconds = time % 60;
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };

  return (
    <div className="relative w-52 h-52 rounded-full overflow-hidden bg-gray-200 flex flex-col justify-center items-center shadow-lg">
      <div
        className={`absolute bottom-0 w-[200%] bg-blue-500 bg-opacity-60 rounded-full z-10 ${
          running
            ? 'animate-wave-rise'
            : ''
        }`}
        style={{
          animationDuration: `${totalDuration}s`,
          animationTimingFunction: 'linear',
          animationFillMode: 'forwards',
        }}
      >
        <div className="absolute top-0 left-0 w-full h-[2px] bg-blue-600"></div>
      </div>
      <div className="relative z-20 text-gray-700 text-xl font-bold">
        <p>{formatTime(timeLeft)}</p>
      </div>
      <div className="relative z-30 mt-4">
        <button
          onClick={handleStart}
          className="px-4 py-2 bg-blue-500 text-white rounded transition hover:bg-blue-700"
        >
          Start
        </button>
      </div>
    </div>
  );
};

export default WaveTimer;
