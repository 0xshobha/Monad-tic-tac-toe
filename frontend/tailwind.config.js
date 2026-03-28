/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'delhi-purple': '#581c87',
        'delhi-orange': '#f97316',
        'delhi-yellow': '#fbbf24',
      },
    },
  },
  plugins: [],
}
