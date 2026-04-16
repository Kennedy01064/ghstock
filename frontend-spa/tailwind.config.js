/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        navy: {
          DEFAULT: "#ffffff",
          accent: "#ffffff",
          deep: "#f1f5f9",
        },
        amber: {
          DEFAULT: "#F2AD3D",
          hover: "#D9921E",
          soft: "#C8A66B",
        },
        text: {
          primary: "#0f172a",
          secondary: "#475569",
          muted: "#94a3b8",
        },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        display: ["Manrope", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [],
}
