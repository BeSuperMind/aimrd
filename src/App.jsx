import React from "react";
import { Routes, Route } from "react-router-dom";
import Home from "./components/Home";
import Main from "./components/Main";
import AppLayout from "./utils/AppLayout";
import MeditatePage from "./components/MeditatePage";
import MeditationTimer from "./components/MeditationTimer";
import FeedbackForm from "./components/FeedbackForm";

function App() {
  return (
    <div className="bg-gray-100 min-h-screen flex justify-center items-center">
      <div className="w-full max-w-sm bg-white shadow-lg rounded-lg overflow-hidden">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/main" element={<AppLayout />}>
            <Route index element={<Main />} />
          </Route>
          <Route path="/meditate" element={<AppLayout />}>
            <Route index element={<MeditatePage />} />
          </Route>
          <Route path="/timer" element={<AppLayout />}>
            <Route index element={<MeditationTimer />} />
          </Route>
          <Route path="/feedback" element={<AppLayout />}>
            <Route index element={<FeedbackForm />} />
          </Route>
        </Routes>
      </div>
    </div>
  );
}

export default App;
