/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      keyframes: {
        waveRise: {
          '0%': { height: '0%' },
          '100%': { height: '100%' },
        },
      },
      animation: {
        'wave-rise': 'waveRise linear forwards',
      },
      fontFamily: {
        sans: ['Poppins', 'sans-serif'],
      },
    },
  },
  plugins: [],
}