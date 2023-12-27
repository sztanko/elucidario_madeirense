import Head from 'next/head'
import { GetStaticPropsContext } from 'next'
import * as fsp from 'fs/promises'
import fs from 'fs'
import path from 'path'

import { makeStaticProps } from '@/lib/i18n/getStatic'
import { Article } from '@/components/article/Article'
import { ArticleData } from '@/models/ArticleData'

const getExtraProps = async (ctx: GetStaticPropsContext) => {
  const { id } = ctx.params
  const locale = ctx.params.locale as string;
  // Get ARTICLES_PATH from environment variables
  // console.info('process.env.ARTICLES_PATH', process.env.ARTICLES_PATH)
  const articlesPath = process.env.ARTICLES_PATH
  try {
    const filePath = path.join(articlesPath, locale, `${id}.json`)
    const jsonData = await fsp.readFile(filePath, 'utf8')
    const article: ArticleData = JSON.parse(jsonData)

    return { article }
  } catch (error) {
    console.error('Failed to load article data', error)
    return { error: 'Failed to load article data' }
  }
}

const getStaticPaths = async () => {
  const articlesPath = process.env.ARTICLES_PATH
  // console.info('articlesPath', articlesPath)
  // Directories only
  const directoryNames = fs
    .readdirSync(articlesPath)
    .filter(fileName =>
      fs.statSync(path.join(articlesPath, fileName)).isDirectory()
    )
  // console.info('directoryNames', directoryNames)
  let paths = []

  for (const dir of directoryNames) {
    const fullPath = path.join(articlesPath, dir)
    const fileNames = fs.readdirSync(fullPath)

    const ids = fileNames
      .filter(fileName => fileName.endsWith('.json')) // Ensure only JSON files
      .map(fileName => fileName.replace('.json', '')) // Remove the .json extension to get ID

    const localePaths = ids.map(id => ({
      params: {
        locale: dir, // the directory name is the locale
        id: id // the file name (without .json) is the id
      }
    }))

    paths = [...paths, ...localePaths]
  }

  return {
    paths: paths,
    fallback: false // can be true, false or 'blocking'
  }
}

const getStaticProps = makeStaticProps(['common'], getExtraProps)
export { getStaticPaths, getStaticProps }

export default function Index ({ article }) {
  return <Article article={article} />
}
