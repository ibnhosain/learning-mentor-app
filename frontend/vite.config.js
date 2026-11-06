import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['icon-192.png', 'icon-512.png'],
      manifest: {
        name: 'Learning Mentor — ওয়েব শিক্ষা',
        short_name: 'লার্নিং মেন্টর',
        description: 'ধাপে ধাপে Web Development শিখি',
        start_url: '/',
        display: 'standalone',
        orientation: 'portrait',
        background_color: '#1e40af',
        theme_color: '#1e40af',
        lang: 'bn',
        icons: [
          { src: '/icon-192.png', sizes: '192x192', type: 'image/png' },
          { src: '/icon-512.png', sizes: '512x512', type: 'image/png', purpose: 'any maskable' },
        ],
      },
      workbox: {
        globPatterns: ['**/*.{js,css,html,ico,png,svg}'],
        runtimeCaching: [
          {
            urlPattern: /^https:\/\/learning-mentor-app\.onrender\.com\/api\/.*/i,
            handler: 'NetworkFirst',
            options: { cacheName: 'api-cache', networkTimeoutSeconds: 90 },
          },
        ],
      },
    }),
  ],
})
