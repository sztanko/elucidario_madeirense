import { getStaticPaths, makeStaticProps } from '@/lib/i18n/getStatic'
import { AboutProject } from '@/components/about/project/AboutProject'

const getStaticProps = makeStaticProps() // createSearchIndexProps)
export { getStaticPaths, getStaticProps }

export default function Home ({ locale }) {
  // Use NEXT_PUBLIC_WEB_PATH env varialbe as prefix
  const dataUrl = `${process.env.NEXT_PUBLIC_WEB_PATH}/index/index_${locale}.json`
  return <AboutProject locale={locale} />
}
