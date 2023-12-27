import Head from 'next/head'
import * as fsp from 'fs/promises'
import fs from 'fs'
import path from 'path'
import * as _ from 'lodash'

import { getStaticPaths, makeStaticProps } from '@/lib/i18n/getStatic'
import { ArticleIndex } from '@/components/article_index/ArticleIndex'
import { AppLayout } from '@/components/layout/AppLayout'
import { loadArticleIndex } from '@/lib/search/dataUtils'

const getExtraProps = async ctx => {
  const { locale } = ctx.params
  const { articleIndex } = await loadArticleIndex(locale)
  return { articleIndex, locale }
}

const getStaticProps = makeStaticProps(getExtraProps)
export { getStaticPaths, getStaticProps }

export default function Index ({ articleIndex, locale }) {
  return (
    <AppLayout>
      <ArticleIndex articleIndex={articleIndex} locale={locale} />
    </AppLayout>
  )
}
