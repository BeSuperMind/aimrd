import { create } from 'zustand';

const useStore = create((set) => ({
  sessionDuration: 10,
  music: 'Silence', 
  setSessionDuration: (duration) => set({ sessionDuration: duration }),
  setMusic: (music) => set({ music }),
  resetSession: () => set({ sessionDuration: 10, music: 'Silence' }),
}));

export default useStore;
