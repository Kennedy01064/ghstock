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
          DEFAULT: "#1e293b",
          accent: "#263244",
          deep: "#0f172a",
        },
        amber: {
          DEFAULT: "#F2AD3D",
          hover: "#D9921E",
          soft: "#C8A66B",
        },
        text: {
          primary: "#ffffff",
          secondary: "rgba(248, 245, 239, 0.85)",
          muted: "rgba(248, 245, 239, 0.6)",
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
