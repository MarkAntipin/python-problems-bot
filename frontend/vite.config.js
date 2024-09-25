import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  optimizeDeps: {
    exclude: [".vite"],
  },
  server: {
    watch: {
        usePolling: true,
    },
    host: true, // Here
    strictPort: true,
    port: 5173,
  }
})
