import type { Glossary } from './Glossary'
import type { ArticleIndexItem } from './ArticleIndexItem'

export interface ArticleData extends ArticleIndexItem {
  body: string
  categories: string[]
  frequesias: string[]
  people: Glossary
  locations: Glossary
  years: Glossary
}
