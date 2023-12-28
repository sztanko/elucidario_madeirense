import { useMemo } from 'react'
import Fuse from 'fuse.js'
import { ArticleIndexItem } from '@/models/ArticleIndexItem'

function useSearch (documents: ArticleIndexItem[]) {
  const fuse = useMemo(() => {
    const options = {
      includeScore: true,
      threshold: 0.3,
      keys: ['title', 'original_title']
    }

    return new Fuse(documents, options)
  }, [documents])

  return fuse
}

export default useSearch
