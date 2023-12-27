/** @type {import('next').NextConfig} */

const nextConfig = {
  output: 'export',
  reactStrictMode: true,
  /*i18n: {
    locales: ['en', 'pt', 'de', 'ru', 'ua'],
    defaultLocale: 'en'
  }*/
  // Use WEB_PATH env variable
  basePath: process.env.WEB_PATH || '',
}

module.exports = nextConfig
