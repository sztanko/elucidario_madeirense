import languageDetector from 'next-language-detector'
import i18nextConfig from '../../../next-i18next.config'

// See https://locize.com/blog/next-i18n-static/ for more details

export default languageDetector({
  supportedLngs: i18nextConfig.i18n.locales,
  fallbackLng: i18nextConfig.i18n.defaultLocale
})
