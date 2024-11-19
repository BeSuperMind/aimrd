import React from 'react';
import TimerSelector from './TimerSelector';
import useStore from '../utils/useStore';
import { useNavigate } from 'react-router-dom';

const MeditatePage = () => {
  const setSessionDuration = useStore((state) => state.setSessionDuration);
  const setMusic = useStore((state) => state.setMusic);
  const navigate = useNavigate();

  const handleStart = (duration, music) => {
    setSessionDuration(duration);
    setMusic(music);
    navigate('/timer');
  };

  return (
    <div>
      <TimerSelector onStart={handleStart} />
    </div>
  );
};

export default MeditatePage;