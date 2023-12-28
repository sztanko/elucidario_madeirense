import { NextRouter } from "next/router"

export const getI18nPath = (path, router: NextRouter) => {
    const locale = (router.query.locale || '') as string
    let href = path || router.asPath
    if (href.indexOf('http')! == 0 && locale) {
      href = href
        ? `/${locale}${href}`
        : router.pathname.replace('[locale]', locale)
    }
    return href
  }
  