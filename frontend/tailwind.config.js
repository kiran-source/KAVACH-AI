/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        soc: {
          dark: '#080c14',
          card: '#0f172a',
          border: '#1e293b',
          cyan: '#06b6d4',
          teal: '#14b8a6',
          danger: '#ef4444',
          warning: '#f59e0b',
          success: '#10b981'
        }
      }
    },
  },
  plugins: [],
}

