/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    darkMode: "class",
    theme: {
        extend: {
            colors: {
                "primary": "#13ec13",
                "primary-dark": "#0eb80e",
                "primary-light": "#e0fde0",
                "background-light": "#f6f8f6",
                "background-dark": "#102210",
                "surface-light": "#ffffff",
                "surface-dark": "#1a331a",
                "text-main": "#1e293b",
                "text-muted": "#64748b",
            },
            fontFamily: {
                "display": ["Public Sans", "sans-serif"]
            },
            borderRadius: {
                "lg": "0.5rem",
                "xl": "0.75rem",
                "2xl": "1rem",
            },
        },
    },
    plugins: [],
}
