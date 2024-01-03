import { useTranslation } from 'next-i18next'
import { HStack, Tag, TagProps } from '@chakra-ui/react'

type CategoriesProps = TagProps & {
  categories: string[]
}

export const Categories = ({ categories, ...rest }: CategoriesProps) => {
  const { t } = useTranslation('common')
  const categoryList = categories.map(category => (
    <Tag key={category} {...rest}>
      {t(category)}
    </Tag>
  ))
  // const people
  return (
    <HStack justifyContent={'flex-end'} flexWrap={'wrap'}>
      {categoryList}
    </HStack>
  )
}
