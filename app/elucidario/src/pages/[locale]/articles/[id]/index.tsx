import Head from 'next/head'
import { GetStaticPropsContext } from 'next'
import { getAllArticlePaths } from '@/lib/search/dataUtils'

import { makeStaticProps } from '@/lib/i18n/getStatic'
import { Article } from '@/components/article/Article'
import { AppLayout } from '@/components/layout/AppLayout'
import { loadArticle } from '@/lib/search/dataUtils'

const getArticleProps = async (ctx: GetStaticPropsContext) => {
  const id = ctx.params.id as string
  const locale = ctx.params.locale as string
  const { article } = await loadArticle(id, locale)
  return { article, locale }
}

const getStaticProps = makeStaticProps(getArticleProps)
export { getAllArticlePaths as getStaticPaths, getStaticProps }

export default function Index ({ article, locale }) {
  return (
    <>
      <Head>
        <title>{`${article['title']} - Elucidario Madeirense`}</title>
        <meta name='viewport' content='width=device-width, initial-scale=1' />
      </Head>
      <AppLayout locale={locale}>
        <Article article={article} />
      </AppLayout>
    </>
  )
}
