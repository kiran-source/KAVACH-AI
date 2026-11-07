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
        // Deep Midnight Navy Palette & Surfaces
        navy: {
          950: '#060911',
          900: '#090e1a',
          850: '#0d1424',
          800: '#131c31',
          750: '#18243e',
          700: '#1f2e4e',
          600: '#2c3f68',
        },
        // Cybernetic Accent Spectrum
        cyan: {
          400: '#22d3ee',
          500: '#06b6d4',
          600: '#0891b2',
        },
        threat: {
          critical: '#ef4444',
          high: '#f97316',
          medium: '#f59e0b',
          guarded: '#3b82f6',
          low: '#10b981',
          info: '#64748b'
        },
        // Legacy soc mapping for backward compatibility
        soc: {
          dark: '#070a13',
          card: '#0d1424',
          elevated: '#131c31',
          border: 'rgba(255, 255, 255, 0.08)',
          cyan: '#06b6d4',
          teal: '#14b8a6',
          danger: '#ef4444',
          warning: '#f59e0b',
          success: '#10b981'
        }
      },
      fontFamily: {
        sans: ['Inter', 'Plus Jakarta Sans', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['Fira Code', 'JetBrains Mono', 'Menlo', 'monospace']
      },
      boxShadow: {
        'glow-cyan': '0 0 20px -3px rgba(6, 182, 212, 0.25)',
        'glow-crimson': '0 0 20px -3px rgba(239, 68, 68, 0.25)',
        'card-depth': '0 4px 20px -2px rgba(0, 0, 0, 0.5), 0 0 0 1px rgba(255, 255, 255, 0.05)',
        'elevated-depth': '0 8px 30px -4px rgba(0, 0, 0, 0.6), 0 0 0 1px rgba(255, 255, 255, 0.08)',
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'fade-in': 'fadeIn 0.2s ease-out',
        'slide-up': 'slideUp 0.25s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(8px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        }
      }
    },
  },
  plugins: [],
}

