import { Menu, MenuButton, MenuItem, MenuList, Box } from '@chakra-ui/react'
import { ChevronDownIcon } from '@chakra-ui/icons'
import { useTranslation } from 'next-i18next'
import LanguageSwitchLink from '../LanguageSwitchLink'

import locales from '@/lib/locales'

export const LangSwitcher = ({ locale }) => {
  const { t } = useTranslation('menu')
  const langItems = locales.map(item => (
    <Box key={item} textAlign={'center'} pr={2}>
    <MenuItem  as={LanguageSwitchLink} locale={item}>
      {t(item)}
    </MenuItem>
    </Box>
  ))

  return (
    <Menu>
      <MenuButton
        // px={4}
        // py={2}
        pr={3}
        transition='all 0.2s'
        borderRadius='md'
        borderWidth='1px'
        minW={"40"}
        // _hover={{ bg: 'gray.400' }}
        // _expanded={{ bg: 'blue.400' }}
        _focus={{ boxShadow: 'outline' }}
        // display='flex' // Ensure the button contents are flexed
        // alignItems='left' // Align items vertically
        // justifyContent='space-between' // Distribute space between items
      >
        {t(locale)} <ChevronDownIcon />
      </MenuButton>
      <MenuList>{langItems}</MenuList>
    </Menu>
  )
}
