import React from 'react'
import {
  HStack,
  Box,
  Menu,
  MenuButton,
  IconButton,
  MenuList,
  MenuItem,
  Text,
  Flex
} from '@chakra-ui/react'
import { HamburgerIcon, ChevronDownIcon } from '@chakra-ui/icons'
import { useTranslation } from 'next-i18next'
import { LoLink } from '../LoLink'
import { SearchBox } from '../search/SearchBox'
import { useBreakpointValue } from '@chakra-ui/media-query'
import { LangSwitcher } from './LangSwitcher'
import { HomeIcon } from './HomeIcon'
import { SearchIcon, ViewIcon, InfoOutlineIcon, AtSignIcon } from '@chakra-ui/icons'

export const TopMenu = ({ locale }) => {
  const { t } = useTranslation('menu')
  const dataUrl = `${process.env.NEXT_PUBLIC_WEB_PATH}/index/index_${locale}.json`
  const iconProps = {mr: 2, height: 6, width: 6, verticalAlign: 'middle'}
  const menuConfig = [
    { label: t('home'), link: '/', icon: <HomeIcon {...iconProps}/> },
    { label: t('all_articles'), link: '/articles', icon: <ViewIcon {...iconProps}/> },
    { label: t('advanced_search'), link: '/search', icon: <SearchIcon {...iconProps}/>  },
    { label: t('about_author'), link: '/about/author', icon: <InfoOutlineIcon {...iconProps}/>  },
    { label: t('about_project'), link: '/about/project', icon: <AtSignIcon {...iconProps}/>  }
  ]

  // const homeIcon = <LoLink href='/' pl={3}><HomeIcon ml={3} width="25px" height="25px"/></LoLink>
  const isMobile = useBreakpointValue({ base: true, lg: false })
  const langSwitcher = <LangSwitcher locale={locale} />

  const menuItems = menuConfig.map(item => (
    <Box flex={1} key={item.label} textAlign={'center'}>
      <LoLink href={item.link}>{item.icon} {item.label}</LoLink>
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
                  {item.icon} {t(item.label)}
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
