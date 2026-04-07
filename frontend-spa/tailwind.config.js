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
          DEFAULT: "#0B1F33",
          accent: "#06286F",
          deep: "#041120",
        },
        amber: {
          DEFAULT: "#F2AD3D",
          hover: "#D9921E",
          soft: "#C8A66B",
        },
        text: {
          primary: "#ffffff",
          secondary: "rgba(248, 245, 239, 0.75)",
          muted: "rgba(248, 245, 239, 0.5)",
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
