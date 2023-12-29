import { getStaticPaths, makeStaticProps } from '@/lib/i18n/getStatic'
import { ArticleIndex } from '@/components/article_index/ArticleIndex'
import { AppLayout } from '@/components/layout/AppLayout'
import { loadArticleIndex } from '@/lib/search/dataUtils'

const getArticleIndexProps = async ctx => {
  const { locale } = ctx.params
  const { articleIndex } = await loadArticleIndex(locale)
  return { articleIndex, locale }
}

const getStaticProps = makeStaticProps(getArticleIndexProps)
export { getStaticPaths, getStaticProps }

export default function Index ({ articleIndex, locale }) {
  return (
    <AppLayout locale={locale}>
      <ArticleIndex articleIndex={articleIndex} locale={locale} showLetters={true} />
    </AppLayout>
  )
}
