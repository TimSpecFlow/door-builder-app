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
        // Gold — luxury brand accent (matches static site #c9a962 / #a88b4a)
        primary: {
          50: '#faf7f0',
          100: '#f4ecd9',
          200: '#e9d8b0',
          300: '#ddc186',
          400: '#d3b174',
          500: '#c9a962',
          600: '#a88b4a',
          700: '#87703b',
          800: '#66542d',
          900: '#45391e',
        },
        // Charcoal — deep neutral (matches static site #1a1a1a / #2d2d2d)
        accent: {
          50: '#f5f5f5',
          100: '#e5e5e5',
          200: '#cccccc',
          300: '#a3a3a3',
          400: '#737373',
          500: '#555555',
          600: '#333333',
          700: '#2d2d2d',
          800: '#1a1a1a',
          900: '#0d0d0d',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        serif: ['"Playfair Display"', 'Georgia', 'serif'],
      },
      backdropBlur: {
        xs: '2px',
      },
      animation: {
        'float': 'float 6s ease-in-out infinite',
        'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        glow: {
          '0%': { boxShadow: '0 0 5px rgba(201, 169, 98, 0.2)' },
          '100%': { boxShadow: '0 0 20px rgba(201, 169, 98, 0.4)' },
        },
      },
    },
  },
  plugins: [],
}
