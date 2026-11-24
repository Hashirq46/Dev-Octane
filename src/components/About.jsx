// src/components/About.jsx
import React from 'react';

export default function About() {
  return (
    <section className="py-20 hero-bg text-center" id="about">
      <h2 className="text-4xl font-bold text-primaryText mb-6">Who We Are</h2>
      <p className="max-w-3xl mx-auto text-secondaryText mb-10">
        DevOctane is a student‑led technology startup founded by a team of nine passionate individuals. Our goal is to combine creativity, technical knowledge, and teamwork to develop innovative digital solutions. We believe in learning, building, and growing together while transforming ideas into practical technology.
      </p>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6 max-w-4xl mx-auto">
        <div className="p-6 bg-darkBg rounded-lg border border-primary">
          <h3 className="text-xl font-semibold text-primaryText">09 Team Members</h3>
        </div>
        <div className="p-6 bg-darkBg rounded-lg border border-primary">
          <h3 className="text-xl font-semibold text-primaryText">Innovation Driven</h3>
        </div>
        <div className="p-6 bg-darkBg rounded-lg border border-primary">
          <h3 className="text-xl font-semibold text-primaryText">Collaborative Development</h3>
        </div>
        <div className="p-6 bg-darkBg rounded-lg border border-primary">
          <h3 className="text-xl font-semibold text-primaryText">Future Focused</h3>
        </div>
      </div>
    </section>
  );
}

