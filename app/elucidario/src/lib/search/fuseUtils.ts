import Fuse, {FuseIndex} from 'fuse.js'

import { ArticleIndexItem } from '@/models/ArticleIndexItem'
import { ArticleData } from '@/models/ArticleData'

export const createSearchIndex = (data: ArticleIndexItem[]) => {
  const index = Fuse.createIndex(['title', 'original_title'], data)
  return index
}

export const createFullSearchIndex = (data: ArticleData[]) => {
  return Fuse.createIndex(['title', 'original_title', 'body'], data)
}


export const getFuseForIndex = (data: ArticleIndexItem[], index: FuseIndex<ArticleIndexItem>) => {    
    return new Fuse(data, {}, index)
    }
export const getFuseForFullIndex = (data: ArticleData[], index: FuseIndex<ArticleData>) => {
    return new Fuse(data, {}, index)
    }