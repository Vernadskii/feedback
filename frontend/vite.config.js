import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import eslint from 'vite-plugin-eslint'
import tailwindcss from 'tailwindcss'

export default defineConfig({
  plugins: [react(), eslint(), tailwindcss()],
  server: {
    port: 5173,
    host: '0.0.0.0',
  },
  resolve: {
    alias: {
      components: '/src/components',
      pages: '/src/pages',
    },
  },
})
