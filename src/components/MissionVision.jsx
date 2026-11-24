// src/components/MissionVision.jsx
import React from 'react';

export default function MissionVision() {
  return (
    <section className="py-20 bg-secondaryBg/70 text-center" id="mission">
      <div className="max-w-4xl mx-auto space-y-12">
        {/* Mission */}
        <div>
          <h2 className="text-3xl font-bold text-primaryText mb-4">Our Mission</h2>
          <p className="text-secondaryText max-w-3xl mx-auto">
            To develop innovative digital solutions through teamwork, creativity, and continuous learning.
          </p>
        </div>
        {/* Vision */}
        <div>
          <h2 className="text-3xl font-bold text-primaryText mb-4">Our Vision</h2>
          <p className="text-secondaryText max-w-3xl mx-auto">
            To become a technology‑driven company that transforms creative ideas into impactful digital products.
          </p>
        </div>
      </div>
    </section>
  );
}

