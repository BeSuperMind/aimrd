import React, { useState } from 'react';
import useStore from '../utils/useStore';
import { useNavigate } from 'react-router-dom';

const TimerSelector = ({ onStart }) => {
  const [duration, setDuration] = useState(60);
  const [music, setMusic] = useState('Silence');
  const { setMusic: setStoreMusic } = useStore();
  const navigate = useNavigate();

  const handleMusicSelection = (track) => {
    setMusic(track);
    setStoreMusic(track);
  };

  return (
    <div className="font-sans text-left p-6">
      <button className="text-xl absolute top-6 left-6" onClick={() => navigate(-1)}>&larr;</button>

      <div className="flex items-center justify-center mt-8 mb-6">
        <div className="relative w-36 h-36 rounded-full border-8 border-indigo-300 flex items-center justify-center">
          <span className="text-lg font-semibold text-gray-700">Select</span>
        </div>
      </div>

      <h2 className="text-lg font-semibold text-gray-700 mb-4">Select time</h2>
      <div className="flex gap-2 flex-wrap mb-6">
        {[60, 45, 30, 15, 10, 5, 2, 1].map((time) => (
          <button
            key={time}
            onClick={() => setDuration(time)}
            className={`px-4 py-2 rounded-full font-medium ${duration === time ? 'bg-indigo-300 text-white' : 'bg-indigo-100 text-gray-700'}`}
          >
            {time} Min
          </button>
        ))}
      </div>

      <div className="flex justify-between">
        <h2 className="text-lg font-semibold text-gray-700 mb-4">Select music</h2>
        <div className="flex justify-center gap-4 mb-6">
          <button className="text-2xl text-indigo-500">🎵</button>
        </div>
      </div>

      <h2 className="text-lg font-semibold text-gray-700 mb-4">Playlist</h2>
      <div className="border-t border-b border-gray-200 divide-y">
        {['Silence', 'Music 1', 'Music 2'].map((track, index) => (
          <button
            key={track}
            onClick={() => handleMusicSelection(track)}
            className={`w-full py-4 flex items-center justify-between ${music === track ? 'bg-indigo-50' : ''}`}
          >
            <div>
              <p className="text-gray-800">{track}</p>
              <p className="text-sm text-gray-500">Artist . 3.14</p>
            </div>
            {/* {index === 2 && (
              <div className="text-gray-500">
                ▶
              </div>
            )} */}
          </button>
        ))}
      </div>

      <button className="mt-4 text-gray-500 text-sm">See more</button>
      <br />
      <button
        onClick={() => onStart(duration, music)}  // Start session with music
        className="mt-6 bg-indigo-500 text-white px-6 py-3 rounded-full font-medium"
      >
        Start Session
      </button>
    </div>
  );
};

export default TimerSelector;
