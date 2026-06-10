/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        dark: '#0A0A0A',
        card: '#111111',
        neonPink: '#FF2D95',
        neonPurple: '#9D4EDD',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      animation: {
        'glow': 'glow 2s ease-in-out infinite',
      },
      keyframes: {
        glow: {
          '0%, 100%': { textShadow: '0 0 5px #FF2D95' },
          '50%': { textShadow: '0 0 20px #9D4EDD' },
        }
      }
    },
  },
  plugins: [],
}