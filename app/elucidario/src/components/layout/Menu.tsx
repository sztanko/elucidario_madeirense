import { HStack, Box } from '@chakra-ui/react'

import { useTranslation } from 'next-i18next'
import { LoLink } from '../LoLink'
import { SearchBox } from '../search/SearchBox'

export const Menu = ({ locale }) => {
  const { t } = useTranslation('menu')
  const dataUrl=`${process.env.NEXT_PUBLIC_WEB_PATH}/index/index_${locale}.json`
  const menuConfig = [
    {
      label: 'home',
      link: '/'
    },
    {
      label: 'all_articles',
      link: '/articles'
    },
    {
      label: 'about_author',
      link: '/about/author'
    },
    {
      label: 'about_project',
      link: '/about/project'
    }
  ]

  const menuItems = menuConfig.map(item => {
    return (
      <Box flex={1} key={item.label} textAlign={'center'}>
        <LoLink href={item.link}>{t(item.label)}</LoLink>
      </Box>
    )
  })
  return (
    <HStack width='100%' spacing={4} justifyContent={'space-around'}>
      {menuItems}
      <Box width='25%'>
        <SearchBox dataUrl={dataUrl} />
      </Box>
    </HStack>
  )
}
