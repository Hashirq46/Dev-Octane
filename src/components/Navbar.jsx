// src/components/Navbar.jsx
import React from 'react';
import { Menu, X } from 'lucide-react';

export default function Navbar() {
  const [open, setOpen] = React.useState(false);
  const links = [
    { name: 'Home', to: 'home' },
    { name: 'About Us', to: 'about' },
    { name: 'Our Services', to: 'services' },
    { name: 'Our Team', to: 'team' },
    { name: 'Contact', to: 'contact' },
  ];

  const renderLink = (link) => (
    <a
      key={link.to}
      href={`#${link.to}`}
      className="cursor-pointer text-secondaryText hover:text-accent transition-colors"
      onClick={() => setOpen(false)}
    >
      {link.name}
    </a>
  );

  return (
    <nav className="fixed inset-x-0 top-0 z-50 bg-blackBg bg-opacity-90 backdrop-blur-md border-b border-secondaryBg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between h-16">
        <div className="flex items-center space-x-2">
          <img src="/logo.jpeg" alt="DevOctane logo" className="h-8" />
          <span className="text-xl font-semibold text-white">DevOctane</span>
        </div>
        <div className="hidden md:flex space-x-6">
          {links.map(renderLink)}
        </div>
        <div className="md:hidden">
          <button onClick={() => setOpen(!open)} aria-label="Menu">
            {open ? <X className="w-6 h-6 text-white" /> : <Menu className="w-6 h-6 text-white" />}
          </button>
        </div>
      </div>
      {open && (
        <div className="md:hidden bg-blackBg border-t border-secondaryBg">
          <div className="px-2 pt-2 pb-3 space-y-1">
            {links.map(renderLink)}
          </div>
        </div>
      )}
    </nav>
  );
}

