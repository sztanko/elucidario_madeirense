// components/LanguageSwitchLink.js
import languageDetector from '@/lib/i18n/languageDetector'
import { useRouter } from 'next/router'
import Link from 'next/link'

const LanguageSwitchLink = ({ locale, children, ...rest }) => {
  const router = useRouter()

  let href = rest.href || router.asPath
  let pName = router.pathname
  Object.keys(router.query).forEach(k => {
    if (k === 'locale') {
      pName = pName.replace(`[${k}]`, locale)
      return
    }
    const localeValue = router.query[k] as string
    pName = pName.replace(`[${k}]`, localeValue)
  })
  if (locale) {
    href = rest.href ? `/${locale}${rest.href}` : pName
  }

  return (
    <Link href={href} onClick={() => languageDetector.cache(locale)}>
      {children}
    </Link>
  )
}

export default LanguageSwitchLink
