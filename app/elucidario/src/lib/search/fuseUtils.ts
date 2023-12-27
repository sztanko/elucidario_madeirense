import Fuse, { FuseIndex } from 'fuse.js'
import type { FuseIndexRecords } from 'fuse.js'
import { ArticleIndexItem } from '@/models/ArticleIndexItem'
import { ArticleData } from '@/models/ArticleData'

type FuseIndexJSON = {
  keys: readonly string[]
  records: FuseIndexRecords
}

export const createSearchIndex = (data: ArticleIndexItem[]): FuseIndexJSON => {
  const index = Fuse.createIndex(['title', 'original_title'], data)
  return index.toJSON()
}

export const createFullSearchIndex = (data: ArticleData[]): FuseIndexJSON => {
  return Fuse.createIndex(['title', 'original_title', 'body'], data).toJSON()
}

export const getFuseForIndex = (
  data: ArticleIndexItem[],
  indexJSON: FuseIndexJSON
) => {
  const index: FuseIndex<ArticleIndexItem> = Fuse.parseIndex(indexJSON)
  return new Fuse(data, {}, index)
}
export const getFuseForFullIndex = (
  data: ArticleData[],
  indexJSON: FuseIndexJSON
) => {
  const index: FuseIndex<ArticleData> = Fuse.parseIndex(indexJSON)
  return new Fuse(data, {}, index)
}
