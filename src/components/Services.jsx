// src/components/Services.jsx
import React from 'react';
import { Code, Server, LayoutPanelTop, Database, BarChart2, Brain } from 'lucide-react';
import { motion } from 'framer-motion';

const services = [
  {
    icon: <Code className="w-12 h-12 text-accent" />, 
    title: 'Web Development',
    description: 'Building modern, responsive, and user‑friendly websites.',
  },
  {
    icon: <Server className="w-12 h-12 text-accent" />, 
    title: 'Software Development',
    description: 'Creating software solutions for real‑world problems.',
  },
  {
    icon: <LayoutPanelTop className="w-12 h-12 text-accent" />, 
    title: 'UI/UX Design',
    description: 'Designing attractive and user‑friendly digital experiences.',
  },
  {
    icon: <Database className="w-12 h-12 text-accent" />, 
    title: 'Database Management',
    description: 'Designing and managing structured databases.',
  },
  {
    icon: <BarChart2 className="w-12 h-12 text-accent" />, 
    title: 'Data Analytics',
    description: 'Transforming raw data into meaningful insights.',
  },
  {
    icon: <Brain className="w-12 h-12 text-accent" />, 
    title: 'AI & Technology Solutions',
    description: 'Exploring AI‑powered applications and intelligent solutions.',
  },
];

export default function Services() {
  return (
    <section className="py-20 bg-darkBg/70 text-center" id="services">
      <h2 className="text-4xl font-bold text-primaryText mb-12">Our Services</h2>
      <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-3 max-w-6xl mx-auto">
        {services.map((svc, idx) => (
          <motion.div
            key={idx}
            whileHover={{ scale: 1.05 }}
            className="p-6 bg-secondaryBg rounded-lg border border-accent transition-shadow"
          >
            <div className="mb-4 flex justify-center">{svc.icon}</div>
            <h3 className="text-xl font-semibold text-primaryText mb-2">{svc.title}</h3>
            <p className="text-secondaryText">{svc.description}</p>
          </motion.div>
        ))}
      </div>
    </section>
  );
}

