/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  i18n: {
    locales: ['en', 'pt', 'de', 'ru', 'ua'],
    defaultLocale: 'en'
  }
}

module.exports = nextConfig
