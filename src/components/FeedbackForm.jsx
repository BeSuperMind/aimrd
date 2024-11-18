import React, { useState } from 'react';
import useStore from '../utils/useStore';
import { useNavigate } from 'react-router-dom';
import HRVGraph from './HRVGraph';

const FeedbackForm = () => {
  const resetSession = useStore((state) => state.resetSession);
  const sessionDuration = useStore((state) => state.sessionDuration); // Access session duration from store
  const [joy, setJoy] = useState(0);
  const [peace, setPeace] = useState(5);
  const [neutral, setNeutral] = useState(5);
  const navigate = useNavigate();

  const handleFeedbackSubmit = () => {
    resetSession();
    console.log({ joy, peace, neutral });
    
    navigate("/main");
  };

  return (
    <div className="flex flex-col items-center p-6 space-y-4">
      <h2 className="text-xl font-bold text-center">Congratulations!</h2>
      <p className="text-lg text-center">
        You have completed a session of {sessionDuration} minutes
      </p>

      <div className="relative flex items-center justify-center w-40 h-40 rounded-full bg-gradient-to-r from-indigo-500 to-purple-600">
        <div className="absolute inset-0 flex flex-col items-center justify-center bg-white rounded-full m-2">
          <span className="text-4xl">{sessionDuration}:00</span>
          <p className="text-xs">Session Completed</p>
        </div>
      </div>

      <p className="text-center mt-4">Tell us the Feedback about the session</p>

      <div className="w-full bg-gray-100 p-4 rounded-xl max-w-md space-y-4">
        <div>
          <label className="block text-sm font-medium mb-1">Joy</label>
          <input 
            type="range" 
            min="1" 
            max="5" 
            value={joy} 
            onChange={(e) => setJoy(Number(e.target.value))} 
            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-500"
          />
          <div className="flex justify-between mt-2 text-lg">
            <span>😡</span>
            <span>😞</span>
            <span>😐</span>
            <span>😊</span>
            <span>😍</span>
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Peace</label>
          <input 
            type="range" 
            min="0" 
            max="10" 
            value={peace} 
            onChange={(e) => setPeace(Number(e.target.value))} 
            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-500"
          />
        </div>

        <HRVGraph />

        <div>
          <label className="block text-sm font-medium mb-1">Thoughts</label>
          <input 
            type="range" 
            min="0" 
            max="10" 
            value={neutral} 
            onChange={(e) => setNeutral(Number(e.target.value))} 
            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-500"
          />
        </div>
      </div>

      <button 
        onClick={handleFeedbackSubmit} 
        className="px-4 py-2 bg-blue-500 text-white font-semibold rounded-lg mt-4 hover:bg-blue-600">
        Submit Feedback
      </button>
    </div>
  );
};

export default FeedbackForm;
