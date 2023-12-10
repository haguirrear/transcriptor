/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["templates/*.html"],
  theme: {
    extend: {
      height: {
        'minus-footer': 'calc(100vh - 60px)',
      }
    },
  },
  plugins: [],
}

