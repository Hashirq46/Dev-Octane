// src/components/WhyChoose.jsx
import React from 'react';
import { Users, Lightbulb, BookOpen, Zap } from 'lucide-react';

const features = [
  { icon: <Users className="w-12 h-12 text-accent" />, title: 'Collaborative Teamwork' },
  { icon: <Lightbulb className="w-12 h-12 text-accent" />, title: 'Creative Thinking' },
  { icon: <BookOpen className="w-12 h-12 text-accent" />, title: 'Continuous Learning' },
  { icon: <Zap className="w-12 h-12 text-accent" />, title: 'Innovation & Quality' },
];

export default function WhyChoose() {
  return (
    <section className="py-20 bg-darkBg/70 text-center" id="why">
      <h2 className="text-4xl font-bold text-primaryText mb-12">Why Choose DevOctane?</h2>
      <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-4 max-w-6xl mx-auto">
        {features.map((f, i) => (
          <div key={i} className="p-6 bg-secondaryBg rounded-lg border border-accent">
            <div className="mb-4 flex justify-center">{f.icon}</div>
            <h3 className="text-xl font-semibold text-primaryText">{f.title}</h3>
          </div>
        ))}
      </div>
    </section>
  );
}


