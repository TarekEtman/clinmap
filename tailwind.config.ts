import type { Config } from 'tailwindcss';

export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        kanit: ['Kanit', 'sans-serif']
      },
      colors: {
        labdark: '#0C0C0C',
        labtext: '#D7E2EA'
      }
    }
  },
  plugins: []
} satisfies Config;
