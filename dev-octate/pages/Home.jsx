import React, { useEffect } from 'react';

export function Home() {
  // Initialize Lucide icons when component mounts
  useEffect(() => {
    if (typeof lucide !== 'undefined' && lucide.createIcons) {
      lucide.createIcons();
    }
  }, []);

  const openModal = (name) => {
    document.getElementById('modal-title').innerText = name;
    document.getElementById('modal-content').innerText = 'Detailed profile information will be added later.';
    document.getElementById('modal').classList.remove('hidden');
  };
  const closeModal = () => document.getElementById('modal').classList.add('hidden');
  const showSuccess = () => document.getElementById('success-msg').classList.remove('hidden');

  return (
    <>
      {/* Navbar */}
      <nav className="sticky top-0 z-50 bg-primary-bg border-b border-secondary-bg">
        <div className="container mx-auto flex items-center justify-between px-4 py-3">
          <div className="flex items-center space-x-2">
            <svg className="w-8 h-8 text-accent" viewBox="0 0 100 100"><polygon points="50,5 95,27 95,73 50,95 5,73 5,27" fill="currentColor"/></svg>
            <span className="text-2xl font-bold text-white">DevOctane</span>
          </div>
          <ul className="hidden md:flex space-x-6 text-light-gray">
            <li><a href="#" className="hover:text-accent">Home</a></li>
            <li><a href="#about" className="hover:text-accent">About Us</a></li>
            <li><a href="#services" className="hover:text-accent">Our Services</a></li>
            <li><a href="#team" className="hover:text-accent">Our Team</a></li>
            <li><a href="#contact" className="hover:text-accent">Contact</a></li>
          </ul>
        </div>
      </nav>

      {/* Hero */}
      <section className="flex flex-col items-center justify-center text-center py-32 bg-primary-bg" id="home">
        <h1 className="text-5xl md:text-6xl font-extrabold text-white mb-4">Building Ideas. Developing Futures.</h1>
        <p className="text-lg text-light-gray max-w-2xl mx-auto mb-8">We are DevOctane, a team of passionate developers and technology enthusiasts turning innovative ideas into meaningful digital solutions.</p>
        <div className="flex space-x-4">
          <a href="#team" className="px-6 py-3 bg-accent text-primary-bg rounded hover:shadow-lg transition">Explore Our Team</a>
          <a href="#contact" className="px-6 py-3 border border-accent text-accent rounded hover:bg-accent hover:text-primary-bg transition">Get In Touch</a>
        </div>
        <div className="mt-6 text-sm text-light-gray">Student-Led Technology Startup | Est. 2026</div>
      </section>

      {/* About */}
      <section id="about" className="py-20 bg-secondary-bg text-center">
        <h2 className="text-4xl font-bold text-white mb-6">Who We Are</h2>
        <p className="text-light-gray max-w-3xl mx-auto mb-8">DevOctane is a student‑led technology startup founded by a team of nine passionate individuals. Our goal is to combine creativity, technical knowledge, and teamwork to develop innovative digital solutions. We believe in learning, building, and growing together while transforming ideas into practical technology.</p>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-4xl mx-auto">
          <div className="p-4 border border-accent rounded">
            <div className="text-2xl font-bold text-accent mb-2">09</div>
            <div className="text-light-gray">Team Members</div>
          </div>
          <div className="p-4 border border-accent rounded">
            <div className="text-2xl font-bold text-accent mb-2">Innovation</div>
            <div className="text-light-gray">Driven</div>
          </div>
          <div className="p-4 border border-accent rounded">
            <div className="text-2xl font-bold text-accent mb-2">Collaboration</div>
            <div className="text-light-gray">Development</div>
          </div>
          <div className="p-4 border border-accent rounded">
            <div className="text-2xl font-bold text-accent mb-2">Future</div>
            <div className="text-light-gray">Focused</div>
          </div>
        </div>
      </section>

      {/* Services */}
      <section id="services" className="py-20 bg-primary-bg text-center">
        <h2 className="text-4xl font-bold text-white mb-8">Our Services</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
          {[
            {icon: 'code', title: 'Web Development', desc: 'Building modern, responsive, and user‑friendly websites.'},
            {icon: 'cpu', title: 'Software Development', desc: 'Creating software solutions for real‑world problems.'},
            {icon: 'mouse-pointer', title: 'UI/UX Design', desc: 'Designing attractive and user‑friendly digital experiences.'},
            {icon: 'database', title: 'Database Management', desc: 'Designing and managing structured databases.'},
            {icon: 'bar-chart-2', title: 'Data Analytics', desc: 'Transforming raw data into meaningful insights.'},
            {icon: 'brain', title: 'AI & Technology Solutions', desc: 'Exploring AI‑powered applications and intelligent solutions.'},
          ].map((s) => (
            <div key={s.title} className="p-6 border border-accent rounded hover:shadow-lg transition">
              <svg className="w-12 h-12 mx-auto mb-4 text-accent" data-lucide={s.icon}></svg>
              <h3 className="text-xl font-semibold text-white mb-2">{s.title}</h3>
              <p className="text-light-gray">{s.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Team */}
      <section id="team" className="py-20 bg-secondary-bg text-center">
        <h2 className="text-4xl font-bold text-white mb-12">Our Team</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
          {[
            {name: 'Addan Mughal', role: 'Founder & Team Leader', desc: 'Leadership, Team Coordination and Project Management'},
            {name: 'Hashir Qureshi', role: 'Software Developer', desc: 'Web Development, Python, C++, Java, SQL, Data Analytics and Power BI'},
            {name: 'Basit Ali Kiani', role: 'Team Member', desc: 'Add specialization here'},
            {name: 'Muhammad Wajaht Javed', role: 'Team Member', desc: 'Add specialization here'},
            {name: 'Zeeshan Ahmed', role: 'Team Member', desc: 'Add specialization here'},
            {name: 'Shehla Ibara', role: 'Team Member', desc: 'Add specialization here'},
            {name: 'Sheikh Hasnain Khalid', role: 'Team Member', desc: 'Add specialization here'},
            {name: 'Haris Zaffer', role: 'Team Member', desc: 'Add specialization here'},
            {name: 'Asma Ashraf', role: 'Team Member', desc: 'Add specialization here'},
          ].map((m) => (
            <div key={m.name} className="bg-primary-bg border border-accent rounded p-6 text-center">
              <div className="w-24 h-24 bg-secondary-bg rounded-full mx-auto mb-4 flex items-center justify-center text-light-gray">Img</div>
              <h3 className="text-xl font-semibold text-white">{m.name}</h3>
              <p className="text-light-gray mb-2">{m.role}</p>
              <p className="text-light-gray text-sm mb-2">{m.desc}</p>
              <div className="flex justify-center space-x-4 mb-2">
                <a href="#" className="text-accent hover:opacity-80"><svg className="w-5 h-5" data-lucide="linkedin"></svg></a>
                <a href="#" className="text-accent hover:opacity-80"><svg className="w-5 h-5" data-lucide="github"></svg></a>
              </div>
              <button className="mt-2 px-4 py-2 border border-accent text-accent rounded hover:bg-accent hover:text-primary-bg" onClick={() => openModal(m.name)}>View Profile</button>
            </div>
          ))}
        </div>
      </section>

      {/* Mission & Vision */}
      <section className="py-20 bg-primary-bg text-center">
        <div className="max-w-5xl mx-auto grid md:grid-cols-2 gap-8">
          <div className="p-8 border border-accent rounded">
            <h3 className="text-2xl font-bold text-white mb-4">Our Mission</h3>
            <p className="text-light-gray">To develop innovative digital solutions through teamwork, creativity, and continuous learning.</p>
          </div>
          <div className="p-8 border border-accent rounded">
            <h3 className="text-2xl font-bold text-white mb-4">Our Vision</h3>
            <p className="text-light-gray">To become a technology‑driven company that transforms creative ideas into impactful digital products.</p>
          </div>
        </div>
      </section>

      {/* Why Choose Us */}
      <section className="py-20 bg-secondary-bg text-center">
        <h2 className="text-4xl font-bold text-white mb-8">Why Choose DevOctane?</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-6xl mx-auto">
          {[
            {icon: 'users', title: 'Collaborative Teamwork', txt: 'Synergy of nine driven developers.'},
            {icon: 'bulb', title: 'Creative Thinking', txt: 'Innovative solutions for every challenge.'},
            {icon: 'book-open', title: 'Continuous Learning', txt: 'Always evolving skill‑set.'},
            {icon: 'zap', title: 'Innovation & Quality', txt: 'Premium results with cutting‑edge tech.'},
          ].map((f) => (
            <div key={f.title} className="p-6 border border-accent rounded hover:shadow-lg transition">
              <svg className="w-12 h-12 mx-auto mb-4 text-accent" data-lucide={f.icon}></svg>
              <h4 className="text-lg font-semibold text-white mb-2">{f.title}</h4>
              <p className="text-light-gray">{f.txt}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Contact */}
      <section id="contact" className="py-20 bg-primary-bg text-center">
        <h2 className="text-4xl font-bold text-white mb-8">Contact Us</h2>
        <div className="max-w-xl mx-auto">
          <form onSubmit={(e) => { e.preventDefault(); showSuccess(); }} className="grid gap-4 text-left">
            <input type="text" placeholder="Full Name" className="w-full p-2 bg-secondary-bg border border-accent rounded text-white" required />
            <input type="email" placeholder="Email Address" className="w-full p-2 bg-secondary-bg border border-accent rounded text-white" required />
            <input type="text" placeholder="Subject" className="w-full p-2 bg-secondary-bg border border-accent rounded text-white" required />
            <textarea placeholder="Message" rows={4} className="w-full p-2 bg-secondary-bg border border-accent rounded text-white" required></textarea>
            <button type="submit" className="px-6 py-3 bg-accent text-primary-bg rounded hover:shadow-lg transition">Send Message</button>
          </form>
          <p id="success-msg" className="mt-4 text-accent hidden">Your message has been sent! (Demo only)</p>
        </div>
        <div className="mt-8 flex justify-center space-x-6 text-accent">
          <a href="#" title="LinkedIn"><svg className="w-6 h-6" data-lucide="linkedin"></svg></a>
          <a href="#" title="Instagram"><svg className="w-6 h-6" data-lucide="instagram"></svg></a>
          <a href="#" title="GitHub"><svg className="w-6 h-6" data-lucide="github"></svg></a>
          <a href="#" title="Facebook"><svg className="w-6 h-6" data-lucide="facebook"></svg></a>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-secondary-bg py-8 text-center text-light-gray">
        <div className="container mx-auto">
          <div className="flex justify-center mb-4">
            <svg className="w-8 h-8 text-accent" viewBox="0 0 100 100"><polygon points="50,5 95,27 95,73 50,95 5,73 5,27" fill="currentColor"/></svg>
          </div>
          <p className="mb-2">DevOctane – Innovative Software Development Agency</p>
          <nav className="flex justify-center space-x-6 mb-4">
            <a href="#" className="hover:text-accent">Home</a>
            <a href="#about" className="hover:text-accent">About Us</a>
            <a href="#services" className="hover:text-accent">Our Services</a>
            <a href="#team" className="hover:text-accent">Our Team</a>
            <a href="#contact" className="hover:text-accent">Contact</a>
          </nav>
          <p className="text-sm">© 2026 DevOctane. All Rights Reserved.</p>
          <p className="text-sm">Designed with Innovation by DevOctane Team.</p>
        </div>
      </footer>

      {/* Modal */}
      <div id="modal" className="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center hidden">
        <div className="bg-primary-bg p-6 rounded border border-accent max-w-lg w-full relative">
          <button className="absolute top-2 right-2 text-light-gray" onClick={closeModal}>✕</button>
          <h3 id="modal-title" className="text-2xl font-bold text-white mb-4"></h3>
          <p id="modal-content" className="text-light-gray"></p>
        </div>
      </div>
    </>
  );
}

