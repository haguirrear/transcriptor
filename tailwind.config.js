/** @type {import('tailwindcss').Config} */

module.exports = {
  content: ["templates/**/*.html"],
  theme: {
    fontFamily: {
      sans: [
        "Inter",
        "ui-sans-serif",
        "system-ui",
        "-apple-system",
        "BlinkMacSystemFont",
        "Segoe\\ UI",
        "Roboto",
        "Helvetica\\ Neue",
        "Arial",
        "Noto\\ Sans",
        "sans-serif",
        "Apple\\ Color\\ Emoji",
        "Segoe\\ UI\\ Emoji",
        "Segoe\\ UI\\ Symbol",
        "Noto\\ Color\\ Emoji",
      ],
    },
    extend: {
      height: {
        "minus-footer": "calc(100vh - 60px)",
      },
    },
  },
  plugins: [],
};
