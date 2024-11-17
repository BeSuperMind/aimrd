import React from 'react'
import { AiFillHome } from "react-icons/ai";
import { RiCompassFill } from "react-icons/ri";
import { IoStatsChart } from "react-icons/io5";
import { IoIosSettings } from "react-icons/io";

const Footer = () => {
  return (
    <footer className='w-full h-24 p-8 flex items-center justify-between opacity-40'>
        <AiFillHome className='h-8 w-8'/>
        <RiCompassFill className='h-8 w-8'/>
        <IoStatsChart className='h-8 w-8' />
        <IoIosSettings className='h-8 w-8'/>
    </footer>
  )
}

export default Footer;