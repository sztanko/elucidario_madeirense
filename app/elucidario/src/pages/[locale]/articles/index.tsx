import Head from 'next/head'
import * as fsp from 'fs/promises'
import fs from 'fs'
import path from 'path'
import * as _ from 'lodash';

import { getStaticPaths, makeStaticProps } from '@/lib/i18n/getStatic'
import { ArticleIndex } from '@/components/article_index/ArticleIndex'
import { AppLayout } from '@/components/layout/AppLayout';

const getExtraProps = async ctx => {
  const { locale } = ctx.params
  // Get ARTICLES_PATH from environment variables
  const articlesPath = process.env.ARTICLES_PATH
  try {
    const filePath = path.join(articlesPath, `index_${locale}.json`)
    const jsonData = await fsp.readFile(filePath, 'utf8')
    const articleIndexRaw = JSON.parse(jsonData)
    const articleIndex = articleIndexRaw.map(a => ({title: a.title, id: a.id, original_title: a.original_title, fl: a.fl}))
    return { articleIndex, locale }
  } catch (error) {
    console.error('Failed to load article data', error)
    return { error: 'Failed to load article data' }
  }
}

const getStaticProps = makeStaticProps(['common'], getExtraProps)
export { getStaticPaths, getStaticProps }

export default function Index ({ articleIndex, locale }) {
  return <AppLayout><ArticleIndex articleIndex={articleIndex} locale={locale} /></AppLayout>
}
