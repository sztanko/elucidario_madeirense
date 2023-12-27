import React, { ReactNode } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/router'

interface LinkComponentProps {
  children: ReactNode
  skipLocaleHandling?: boolean
  href?: string
  locale?: string
  [rest: string]: any
}

export const LoLink: React.FC<LinkComponentProps> = ({
  children,
  skipLocaleHandling,
  ...rest
}) => {
  const router = useRouter()
  // Ensure that locale is always treated as a single string
  const locale = (rest.locale || router.query.locale || '') as string

  let href = rest.href || router.asPath
  if (href.indexOf('http') === 0) skipLocaleHandling = true
  if (locale && !skipLocaleHandling) {
    // Ensure that the locale is a string when replacing
    href = href
      ? `/${locale}${href}`
      : router.pathname.replace('[locale]', locale)
  }

  return (
    <>
      <Link {...rest} href={href} >
        {children}
      </Link>
    </>
  )
}
