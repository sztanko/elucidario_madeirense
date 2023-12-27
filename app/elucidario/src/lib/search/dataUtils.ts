import fs from 'fs/promises'
import path from 'path'
import * as _ from 'lodash'
import { ArticleIndexItem } from '@/models/ArticleIndexItem'
import { ArticleData } from '@/models/ArticleData'

export const loadArticleIndex = async locale => {
  const articlesPath = process.env.ARTICLES_PATH
  try {
    const filePath = path.join(articlesPath, `index_${locale}.json`)
    const jsonData = await fs.readFile(filePath, 'utf8')
    const articleIndexRaw = JSON.parse(jsonData) as ArticleIndexItem[]
    const articleIndex = articleIndexRaw.map(a => ({
      title: a.title,
      id: a.id,
      original_title: a.original_title,
      fl: a.fl
    }))
    // console.info('loadArticleIndex', articleIndex)
    return { articleIndex, locale }
  } catch (error) {
    console.error('Failed to load article data', error)
    return { error: 'Failed to load article data' }
  }
}

export const loadArticle = async (id: string, locale: string) => {
  const articlesPath = process.env.ARTICLES_PATH
  try {
    const filePath = path.join(articlesPath, locale, `${id}.json`)
    const jsonData = await fs.readFile(filePath, 'utf8')
    const article: ArticleData = JSON.parse(jsonData)
    return { article }
  } catch (error) {
    console.error('Failed to load article data', error)
    return { error: 'Failed to load article data' }
  }
}

export const getAllArticlePaths = async () => {
  const articlesPath = process.env.ARTICLES_PATH

  const directoryNames = (
    await fs.readdir(articlesPath, { withFileTypes: true })
  )
    .filter(dirent => dirent.isDirectory())
    .map(dirent => dirent.name)

  let paths = []

  for (const dir of directoryNames) {
    const fullPath = path.join(articlesPath, dir)
    const fileNames = await fs.readdir(fullPath)

    const ids = fileNames
      .filter(fileName => fileName.endsWith('.json'))
      .map(fileName => fileName.replace('.json', ''))

    const localePaths = ids.map(id => ({
      params: {
        locale: dir,
        id: id
      }
    }))

    paths = [...paths, ...localePaths]
  }

  return {
    paths: paths,
    fallback: false
  }
}
