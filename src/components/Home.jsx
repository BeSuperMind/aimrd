import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import homeImg1 from "../assets/home1.png";
import homeImg2 from "../assets/home2.png";
import homeImg3 from "../assets/home3.png";
import SignInWithGoogle from "../utils/SignInWithGoogle";

const slides = [
  {
    image: homeImg1,
    title: "WELCOME",
    text: "Meditation is the key to\nunlocking the door to peace",
  },
  {
    image: homeImg2,
    title: "WELCOME",
    text: "The best time to meditate is now",
  },
  {
    image: homeImg3,
    title: "WELCOME",
    text: "Do meditation, Stay focus\nLive a happy life",
  },
];

const slideVariants = {
  hidden: {
    x: "100%", // Start off-screen to the right
    opacity: 0,
  },
  visible: {
    x: 0, // Slide into view
    opacity: 1,
    transition: { duration: 0.8, ease: "easeInOut" },
  },
  exit: {
    x: "-100%", // Exit off-screen to the left
    opacity: 0,
    transition: { duration: 0.8, ease: "easeInOut" },
  },
};

const Home = () => {
  const [currentSlide, setCurrentSlide] = useState(0);

  const handleNextClick = () => {
    if (currentSlide < slides.length - 1) {
      setCurrentSlide(currentSlide + 1);
    }
  };

  return (
    <div className="bg-white flex flex-col items-center justify-center min-h-screen font-sans">
      {/* Slide Container */}
      <div className="overflow-hidden w-full max-w-lg p-6">
        <AnimatePresence mode="wait">
          {/* Current Slide with Animation */}
          <motion.div
            key={currentSlide}
            variants={slideVariants}
            initial="hidden"
            animate="visible"
            exit="exit"
            className="flex flex-col items-center text-center"
          >
            <img
              src={slides[currentSlide].image}
              alt={slides[currentSlide].title}
              className="w-full rounded-md"
            />
            <h2 className="text-4xl mt-4">{slides[currentSlide].title}</h2>
            <p className="text-sm mt-2">
              {slides[currentSlide].text.split("\n").map((line, index) => (
                <span key={index}>
                  {line}
                  <br />
                </span>
              ))}
            </p>
          </motion.div>
        </AnimatePresence>
      </div>

      {/* Button Section */}
      <div className="w-full max-w-lg p-6 text-center">
        {currentSlide < slides.length - 1 ? (
          <button
            onClick={handleNextClick}
            className="bg-[#335AE2] w-full h-12 text-white py-2 px-4 rounded-3xl"
          >
            Next
          </button>
        ) : (
          <SignInWithGoogle />
        )}
      </div>
    </div>
  );
};

export default Home;