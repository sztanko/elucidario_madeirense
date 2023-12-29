import { useEffect, useState } from 'react'
import Fuse, { IFuseOptions } from 'fuse.js'

interface UseLoadSearchReturn<T> {
  documents: T[]
  loading: boolean
  error: Error | null
  search: Fuse<T> | null
}

const useLoadSearch = <T>(
  url: string,
  searchOptions: IFuseOptions<T>
): UseLoadSearchReturn<T> => {
  const [documents, setDocuments] = useState<T[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<Error | null>(null)
  const [search, setSearch] = useState<Fuse<T> | null>(null)

  // useEffect for fetching documents from the URL
  useEffect(() => {
    setLoading(true)
    fetch(url)
      .then(res => res.json())
      .then(
        result => {
          setDocuments(result)
          setSearch(new Fuse(result, searchOptions)) // use current documents
          setLoading(false)
        },
        (error: Error) => {
          setError(error)
          setLoading(false)
        }
      )
  }, [url, searchOptions]) // Only re-run the effect if url changes

  // useEffect for creating/updating Fuse instance when documents or searchKeys change
  /*
  useEffect(() => {
    if (documents.length > 0) {
      const options = {
        includeScore: true,
        threshold: 0.3,
        keys: searchKeys
      }
      setSearch(new Fuse(documents, options)) // use current documents
      setLoading(false)
    }
  }, [documents, searchKeys]) // Re-run the effect if documents or searchKeys change
*/
  return { documents, loading, error, search }
}

export default useLoadSearch
