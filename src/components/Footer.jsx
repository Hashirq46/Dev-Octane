// src/components/Footer.jsx
import React from 'react';
import { Linkedin, Instagram, Github, Facebook } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="bg-blackBg/80 text-secondaryText py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row justify-between items-center">
        {/* Logo & description */}
        <div className="flex items-center space-x-3 mb-4 md:mb-0">
          <img src="/logo.jpeg" alt="DevOctane logo" className="h-8 w-8 object-contain" />
          <span className="text-white font-semibold">DevOctane</span>
        </div>
        <p className="text-sm max-w-md text-center md:text-left mb-4 md:mb-0">
          Premium software development agency built by passionate university students.
        </p>
        {/* Social icons */}
        <div className="flex space-x-4">
          <a href="#" className="text-accent hover:text-white"><Linkedin className="w-5 h-5" /></a>
          <a href="https://www.instagram.com/team_dev_octane_09?hvrq=MWJqbGhhMHVzcXR4Zg%3D%3D&utm_source=qr" className="text-accent hover:text-white"><Instagram className="w-5 h-5" /></a>
          <a href="#" className="text-accent hover:text-white"><Github className="w-5 h-5" /></a>
          <a href="https://www.facebook.com/share/18wBmB7vbc/" className="text-accent hover:text-white"><Facebook className="w-5 h-5" /></a>
        </div>
      </div>
      <div className="mt-6 text-center text-xs text-secondaryText">
        © 2026 DevOctane. All Rights Reserved.<br />
        Designed with Innovation by DevOctane Team.
      </div>
    </footer>
  );
}



