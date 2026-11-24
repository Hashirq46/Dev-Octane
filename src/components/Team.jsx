// src/components/Team.jsx
import React, { useState } from 'react';
import { teamMembers as team } from '../data/teamMembers.js';
import { X, Linkedin, ExternalLink } from 'lucide-react';

export default function Team() {
  const [selected, setSelected] = useState(null);

  return (
    <section className="py-20 bg-secondaryBg/70 text-center" id="team">
      <h2 className="text-4xl font-bold text-primaryText mb-12">Our Team</h2>
      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 max-w-6xl mx-auto">
        {team.map((member) => (
          <div
            key={member.name}
            className="bg-darkBg rounded-lg border border-primary p-4 flex flex-col items-center cursor-pointer hover:shadow-lg transition-shadow"
            onClick={() => setSelected(member)}
          >
            <img src={member.img} alt={member.name} className="w-32 h-32 rounded-full mb-4" />
            <h3 className="text-xl font-semibold text-primaryText">{member.name}</h3>
            <p className="text-secondaryText mb-2">{member.role}</p>
            <button className="mt-auto px-4 py-2 bg-accent text-primaryBg rounded hover:bg-opacity-80 transition">
              View Profile
            </button>
          </div>
        ))}
      </div>

      {/* Modal */}
      {selected && (
        <div className="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center z-50">
          <div className="bg-darkBg rounded-lg w-11/12 md:w-2/3 lg:w-1/2 p-6 relative">
            <button
              className="absolute top-2 right-2 text-white"
              onClick={() => setSelected(null)}
            >
              <X className="w-6 h-6" />
            </button>
            <div className="flex flex-col md:flex-row items-center">
              <img src={selected.img} alt={selected.name} className="w-48 h-48 rounded-full mb-4 md:mb-0 md:mr-6" />
              <div className="text-left">
                <h3 className="text-2xl font-bold text-primaryText">{selected.name}</h3>
                <p className="text-secondaryText mb-2">{selected.role}</p>
                <p className="text-secondaryText mb-4"><strong>Specialization:</strong> {selected.desc}</p>
                <p className="text-secondaryText mb-4">{selected.intro}</p>
                <div className="flex space-x-4 text-accent">
                  <a href={selected.linkedin} target="_blank" rel="noopener noreferrer" title="LinkedIn profile"><Linkedin className="w-6 h-6" /></a>

                  {selected.portfolio && (
                    <a href={selected.portfolio} target="_blank" rel="noopener noreferrer"><ExternalLink className="w-6 h-6" /></a>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </section>
  );
}

