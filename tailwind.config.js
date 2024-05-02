/** @type {import('tailwindcss').Config} */
import animatePlugin from "tailwindcss-animate";

export default {
  content: ["backend/templates/**/*.html", "backend/components/**/*.jinja"],
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
      backgroundImage: {
        rainbow: "url('/static/img/rainbow.png')",
      },
    },
    keyframes: {
      "accordion-down": {
        from: { height: "0" },
        to: { height: "var(--radix-accordion-content-height)" },
      },
      "accordion-up": {
        from: { height: "var(--radix-accordion-content-height)" },
        to: { height: "0" },
      },
    },
    animation: {
      "accordion-down": "accordion-down 0.2s ease-out",
      "accordion-up": "accordion-up 0.2s ease-out",
    },
  },
  plugins: [animatePlugin],
};
