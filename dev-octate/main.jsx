import './src/index.css';
import React from 'react';
import { createRoot } from 'react-dom/client';
import { Home } from './pages/Home.jsx';

function App() {
  return <Home />;
}

const container = document.getElementById('root');
const root = createRoot(container);
root.render(<App />);
