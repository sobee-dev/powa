/** @type {import('tailwindcss').Config} */

module.exports = {
  content: ["./templates/**/*.html"],
  safelist: [
    'animate-pan',
    'animate-zoom-slow',
    'animate-fadeIn',
    'animate-slideInUp',
  ],
  theme: {
    extend: {
      keyframes: {
        slide: {
          '0%': { transform: 'translateX(100%)' },
          '100%': { transform: 'translateX(-100%)' },
        },
      },
      animation: {
        slide: 'slide 15s linear infinite',
      },
      fontFamily: {
        roboto: ['Roboto', 'Sansita'],
      }
    }
  },
  plugins: [],
}