const path = require('path');
const createNextIntlPlugin = require('next-intl/plugin');

const withNextIntl = createNextIntlPlugin('./i18n.ts');

/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    appDir: true,
  },
  images: {
    domains: [
      'lh3.googleusercontent.com', // Google profile images
      'avatars.githubusercontent.com', // GitHub profile images (if needed)
    ],
  },
  webpack: (config, { buildId, dev, isServer, defaultLoaders, webpack }) => {
    config.resolve.alias = {
      ...config.resolve.alias,
      '@': path.resolve(__dirname, './app'),
      '@lib': path.resolve(__dirname, './lib'),
      '@utils': path.resolve(__dirname, './utils'),
    };
    
    // Ensure proper module resolution
    config.resolve.modules = [
      ...config.resolve.modules,
      path.resolve(__dirname, './app'),
      path.resolve(__dirname, './lib'),
      path.resolve(__dirname, './utils'),
    ];
    
    return config;
  },
};

module.exports = withNextIntl(nextConfig);
