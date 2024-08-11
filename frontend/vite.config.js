import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import eslint from 'vite-plugin-eslint'

export default defineConfig({
  plugins: [react(), eslint()],
  server: {
    port: 5173,
    host: '0.0.0.0'
  },
  resolve: {
    alias: {
      assets: '/src/assets'
    }
  }
})
