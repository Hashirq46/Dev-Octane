// src/components/Contact.jsx
import React, { useState } from 'react';

export default function Contact() {
  const [form, setForm] = useState({ name: '', email: '', subject: '', message: '' });
  const [submitted, setSubmitted] = useState(false);
  const [errors, setErrors] = useState({});

  const validate = () => {
    const newErrors = {};
    if (!form.name.trim()) newErrors.name = 'Name is required';
    if (!form.email.trim()) newErrors.email = 'Email is required';
    else if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(form.email)) newErrors.email = 'Invalid email';
    if (!form.subject.trim()) newErrors.subject = 'Subject is required';
    if (!form.message.trim()) newErrors.message = 'Message is required';
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validate()) {
      // In demo we just show success, no real email sending.
      setSubmitted(true);
    }
  };

  return (
    <section className="py-20 bg-secondaryBg/70 text-center" id="contact">
      <h2 className="text-4xl font-bold text-primaryText mb-8">Contact Us</h2>
      <div className="max-w-xl mx-auto text-left">
        {submitted ? (
          <div className="p-6 bg-darkBg rounded-lg border border-primary text-primaryText">
            <p className="text-center">Thank you! Your message has been sent.</p>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-secondaryText mb-1" htmlFor="name">Full Name</label>
              <input
                id="name"
                name="name"
                type="text"
                value={form.name}
                onChange={handleChange}
                className="w-full px-3 py-2 bg-darkBg border border-primary rounded text-primaryText focus:outline-none"
              />
              {errors.name && <p className="text-sm text-accent mt-1">{errors.name}</p>}
            </div>
            <div>
              <label className="block text-secondaryText mb-1" htmlFor="email">Email Address</label>
              <input
                id="email"
                name="email"
                type="email"
                value={form.email}
                onChange={handleChange}
                className="w-full px-3 py-2 bg-darkBg border border-primary rounded text-primaryText focus:outline-none"
              />
              {errors.email && <p className="text-sm text-accent mt-1">{errors.email}</p>}
            </div>
            <div>
              <label className="block text-secondaryText mb-1" htmlFor="subject">Subject</label>
              <input
                id="subject"
                name="subject"
                type="text"
                value={form.subject}
                onChange={handleChange}
                className="w-full px-3 py-2 bg-darkBg border border-primary rounded text-primaryText focus:outline-none"
              />
              {errors.subject && <p className="text-sm text-accent mt-1">{errors.subject}</p>}
            </div>
            <div>
              <label className="block text-secondaryText mb-1" htmlFor="message">Message</label>
              <textarea
                id="message"
                name="message"
                rows={4}
                value={form.message}
                onChange={handleChange}
                className="w-full px-3 py-2 bg-darkBg border border-primary rounded text-primaryText focus:outline-none"
              />
              {errors.message && <p className="text-sm text-accent mt-1">{errors.message}</p>}
            </div>
            <button
              type="submit"
              className="w-full px-4 py-2 bg-accent text-primaryBg rounded hover:bg-opacity-80 transition"
            >
              Send Message
            </button>
          </form>
        )}
      </div>
    </section>
  );
}

