/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
 
    // Or if using `src` directory:
    "./src/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        Inter: ["Inter", "sans-serif"],
        Prompt: ["Prompt", "sans-serif"],
        Bungee: ["Bungee", "cursive"],
        ADLaM: ["ADLaM Display", "cursive"],
        PressStart: ["'Press Start 2P'", "cursive"],
        Gruppo: ["Gruppo", "sans-serif"],
        Dela: ["'Dela Gothic One'", "cursive"],
        Raleway: ["Raleway", "sans-serif"]
      },
      backgroundImage: {
      }
    },
  },
  plugins: [],
}