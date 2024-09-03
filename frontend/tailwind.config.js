/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    colors: {},
    fontSize: {
      xs: ['0.75rem', { lineHeight: '0.875rem', letterSpacing: '' }], // 12/14px
      sm: ['0.875rem', { lineHeight: '1.125rem', letterSpacing: '' }], // 14/18px
      base: ['1rem', { lineHeight: '1.3rem', letterSpacing: '0.2px' }], // 16/20px
      lg: ['1.3rem', { lineHeight: '1.5rem', letterSpacing: '0.3px' }], // 20/24px
      xl: ['1.5rem', { lineHeight: '1.75rem', letterSpacing: '0.4px' }], // 24/28px
      '2xl': ['2.5rem', { lineHeight: '2.5rem', letterSpacing: '' }], // 40/40px
    },
    fontWeight: {
      medium: '400',
      semibold: '500',
      bold: '600',
    },
    fontFamily: {
      manrope: "'Manrope', sans-serif",
    },
    boxShadow: {
      custom: '0 16px 40px 10px rgba(20, 20, 20, 0.1)',
    },
    borderRadius: {
      sm: '0.625rem', // 10px
      md: '1rem', // 16px
      lg: '1.5rem', // 24px
      xl: '1.875rem', // 30px
    },
    extend: {},
  },
  plugins: [],
}
