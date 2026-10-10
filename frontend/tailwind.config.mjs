/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        ink: {
          DEFAULT: '#171717',
          90: 'rgba(23, 23, 23, 0.90)',
          80: 'rgba(23, 23, 23, 0.80)',
          60: 'rgba(23, 23, 23, 0.60)',
          40: 'rgba(23, 23, 23, 0.40)',
          24: 'rgba(23, 23, 23, 0.24)',
          14: 'rgba(23, 23, 23, 0.14)',
          8: 'rgba(23, 23, 23, 0.08)',
          4: 'rgba(23, 23, 23, 0.04)',
        },
        paper: {
          DEFAULT: '#F7F6F2',
          90: 'rgba(247, 246, 242, 0.90)',
          80: 'rgba(247, 246, 242, 0.80)',
          60: 'rgba(247, 246, 242, 0.60)',
          20: 'rgba(247, 246, 242, 0.20)',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
      },
      maxWidth: {
        container: '1200px',
        reading: '720px',
      },
      borderRadius: {
        sm: '2px',
        DEFAULT: '4px',
      },
    },
  },
  plugins: [],
};
