// tailwind.config.cjs
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        // Brand palette
        primary: "#00E6A0",        // Emerald Green
        secondary: "#00CFA6",      // Teal
        accent: "#4DFFC3",         // Neon Mint
        // Backgrounds
        blackBg: "#050B0B",        // Main background (deep black)
        darkBg: "#0B1515",         // Secondary background
        // Text colors
        primaryText: "#FFFFFF",    // White
        secondaryText: "#B8C5C2", // Light Gray
        // Preserve any older names that might be used elsewhere
        primaryBg: "#050B0B",
        secondaryBg: "#0B1515",
        accentOld: "#38D9A9",
      },
      fontFamily: {
        // Use Inter – fallback to system sans‑serif
        sans: ["Inter", "ui-sans-serif", "system-ui"],
      },
      boxShadow: {
        neon: "0 0 8px rgba(0,230,160,.6), 0 0 20px rgba(0,230,160,.4)",
      },
      animation: {
        "spin-slow": "spin 20s linear infinite",
        "fade-in": "fadeIn 0.8s ease-out forwards",
      },
      keyframes: {
        fadeIn: {
          "0%": { opacity: "0", transform: "translateY(20px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
      },
    },
  },
  plugins: [],
};
