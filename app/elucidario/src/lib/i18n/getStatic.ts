import { GetStaticProps } from 'next'
import { GetStaticPropsContext } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import i18nextConfig from '../../../next-i18next.config'

// See https://locize.com/blog/next-i18n-static/ for more details

export const getI18nPaths = () =>
  i18nextConfig.i18n.locales.map(lng => ({
    params: {
      locale: lng
    }
  }))

export const getStaticPaths = () => ({
  fallback: false,
  paths: getI18nPaths()
})

export async function getI18nProps (ctx, ns = ['common']) {
  const locale = ctx?.params?.locale
  let props = {
    ...(await serverSideTranslations(locale, ns))
  }
  // console.info('getI18nProps', props._nextI18Next.userConfig)
  return props
}

export function makeStaticProps (
  getExtraProps: (
    ctx: GetStaticPropsContext
  ) => Promise<{ [key: string]: any }> = async () => ({})
): GetStaticProps {
  return async function getStaticProps (ctx) {
    // Get the i18n props
    const i18nProps = await getI18nProps(ctx, ['common', 'menu'])

    // Get extra static props
    const extraProps = await getExtraProps(ctx)
    return {
      props: {
        ...i18nProps,
        ...extraProps // Merge the extra props
      }
    }
  }
}
