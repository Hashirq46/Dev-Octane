// src/components/Hero.jsx
import React from 'react';
import { motion } from 'framer-motion';

export default function Hero() {
  return (
    <section className="hero-bg relative min-h-screen flex items-center justify-center text-center" id="home">
      {/* Background geometric shapes */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-1/4 left-1/4 w-72 h-72 bg-accent opacity-10 rounded-full animate-pulse" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 border-2 border-accent opacity-5 rounded-full animate-spin-slow" />
      </div>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="z-10 max-w-2xl space-y-6"
      >
        <h1 className="text-5xl md:text-6xl font-bold text-primaryText">Building Ideas. Developing Futures.</h1>
        <p className="text-lg text-secondaryText max-w-xl mx-auto">
          We are DevOctane, a team of passionate developers and technology enthusiasts turning innovative ideas into meaningful digital solutions.
        </p>
        <div className="flex justify-center space-x-4 mt-6">
          <a href="#team" className="px-6 py-2 bg-accent text-primaryBg rounded-md hover:bg-opacity-80 transition">
            Explore Our Team
          </a>
          <a href="#contact" className="px-6 py-2 bg-secondaryBg text-secondaryText border border-accent rounded-md hover:bg-accent hover:text-primaryBg transition">
            Get In Touch
          </a>
        </div>
        <div className="mt-4 text-sm text-secondaryText">
          Student-Led Technology Startup | Est. 2026
        </div>
      </motion.div>
    </section>
  );
}

