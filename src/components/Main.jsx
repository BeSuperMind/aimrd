import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import mainImage from "../assets/main1.png";
import button1 from "../assets/mainbutton1.png";
import button2 from "../assets/mainbutton2.png";
import button3 from "../assets/mainbutton3.png";
import mainImage2 from "../assets/main2.png";

const Main = () => {
  const [profilePhoto, setProfilePhoto] = useState(null);
  const [userName, setUserName] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const name = localStorage.getItem('userName');
    const photo = localStorage.getItem('userPhoto');
    if (name) 
      setUserName(name);
    if (photo) 
      setProfilePhoto(photo);
  }, []);

  const handleSelfMeditationClick = () => {
    navigate('/meditate');
  };

  return (
    <div className='flex flex-col'>
      <div className='w-full h-24 bg-[#92B5FA] flex items-center justify-between px-4'>
        <div className='text-left text-sm'>
          <div className='text-black'>
            {userName ? `Welcome, ${userName}` : "Welcome"}
          </div>
          <div className='text-white'>
            How are you today?
          </div>
        </div>
        {profilePhoto && (
          <img 
            src={profilePhoto} 
            alt="User Profile" 
            className='rounded-full h-12 w-12 ml-auto' 
          />
        )}
      </div>
      <div className="bg-white p-4">
          <img
            src={mainImage}
            alt="Home Page Image"
            className="w-full rounded-md"
          />
      </div>
      <div className="bg-white p-4">
        <div className='flex items-center justify-between p-4'>
          <div onClick={handleSelfMeditationClick} className='cursor-pointer flex flex-col'>
            <img
              src={button1}
              alt="Home Page Image"
              className="w-20 rounded-md"
            />
            <p className='text-center text-sm'>Start <br /> Meditation</p>
          </div>
          <div className='flex flex-col'>
            <img
              src={button2}
              alt="Home Page Image"
              className="w-20 rounded-md"
            />
            <p className='text-center text-sm'>Join <br /> Meditation</p>
          </div>
          <div className='flex flex-col'>
            <img
              src={button3}
              alt="Home Page Image"
              className="w-20 rounded-md"
            />
            <p className='text-center text-sm'>Progress</p>
          </div>
        </div>
      </div>
      <div className="bg-white p-4">
        <p className='text-[#506FFF]'>Upcoming Events</p>
          <img
            src={mainImage2}
            alt="Home Page Image"
            className="w-full rounded-md pt-4"
          />
      </div>
    </div>
    
  );
}

export default Main;
