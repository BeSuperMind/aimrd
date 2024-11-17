import React, { useState } from 'react';
import homeImg1 from "../assets/home1.png";
import homeImg2 from "../assets/home2.png";
import homeImg3 from "../assets/home3.png";
import SignInWithGoogle from '../utils/SignInWithGoogle';

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

const Home = () => {
  const [currentSlide, setCurrentSlide] = useState(0);

  const handleNextClick = () => {
    if (currentSlide < slides.length - 1) {
      setCurrentSlide(currentSlide + 1);
    }
  };

  return (
    <div className="bg-white flex flex-col items-center justify-center min-h-screen font-sans">
      <div className="overflow-hidden">
        <div className="bg-white p-6">
          <img
            src={slides[currentSlide].image}
            alt={slides[currentSlide].title}
            className="w-full rounded-md"
          />
        </div>
        <div className="bg-white p-6 text-center">
          <h2 className="text-4xl mb-4">{slides[currentSlide].title}</h2>
          <p className="text-sm mb-4">
            {slides[currentSlide].text.split('\n').map((line, index) => (
              <span key={index}>
                {line}
                <br />
              </span>
            ))}
          </p>
          {currentSlide < slides.length - 1 ? (
            <button
              onClick={handleNextClick}
              className="bg-[#335AE2] w-full h-20 text-white py-2 px-4 rounded-3xl"
            >
              Next
            </button>
          ) : (
            <SignInWithGoogle />
          )}
        </div>
      </div>
    </div>
  );
};

export default Home;
