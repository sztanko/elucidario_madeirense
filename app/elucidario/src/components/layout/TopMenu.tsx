import React from 'react'
import {
  HStack,
  Box,
  Menu,
  MenuButton,
  IconButton,
  MenuList,
  MenuItem,
  Flex
} from '@chakra-ui/react'
import { HamburgerIcon, ChevronDownIcon } from '@chakra-ui/icons'
import { useTranslation } from 'next-i18next'
import { LoLink } from '../LoLink'
import { SearchBox } from '../search/SearchBox'
import { useBreakpointValue } from '@chakra-ui/media-query'
import { LangSwitcher } from './LangSwitcher'

export const TopMenu = ({ locale }) => {
  const { t } = useTranslation('menu')
  const dataUrl = `${process.env.NEXT_PUBLIC_WEB_PATH}/index/index_${locale}.json`
  const menuConfig = [
    { label: 'home', link: '/' },
    { label: 'all_articles', link: '/articles' },
    { label: 'advanced_search', link: '/search' },
    { label: 'about_author', link: '/about/author' },
    { label: 'about_project', link: '/about/project' }
  ]

  const isMobile = useBreakpointValue({ base: true, lg: false })
  const langSwitcher = <LangSwitcher locale={locale} />

  const menuItems = menuConfig.map(item => (
    <Box flex={1} key={item.label} textAlign={'center'}>
      <LoLink href={item.link}>{t(item.label)}</LoLink>
    </Box>
  ))
  const searchBox = <SearchBox dataUrl={dataUrl} />

  return (
    <Flex width='100%' justifyContent={'space-between'} m={0}>
      {!isMobile ? (
        <>
          <HStack spacing={4} flex={3}>
            {menuItems}
          </HStack>{' '}
          <HStack flex={1}>
          {searchBox} {langSwitcher}
          </HStack>
        </>
      ) : (
        <>
          <Menu>
            <MenuButton
              as={IconButton}
              icon={<HamburgerIcon />}
              variant='outline'
            />
            <MenuList>
              {menuConfig.map(item => (
                <MenuItem key={item.label} as={LoLink} href={item.link}>
                  {t(item.label)}
                </MenuItem>
              ))}
            </MenuList>
          </Menu>
          {searchBox}
          {langSwitcher}
        </>
      )}
    </Flex>
  )
}
