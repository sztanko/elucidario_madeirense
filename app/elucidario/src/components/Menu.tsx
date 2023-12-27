import { HStack, Box } from '@chakra-ui/react'
import { LoLink } from './LoLink'

export const Menu = () => {
  const menuItems = [
    {
      label: 'home',
      link: '/'
    },
    {
      label: 'all_articles',
      link: '/articles'
    },
    {
      label: 'about_the_author',
      link: '/about/author'
    },
    {
      label: 'about_project',
      link: '/about/project'
    }
  ]

  const items = menuItems.map(item => {
    return (
      <Box flex={1} key={item.label} textAlign={"center"}>
        <LoLink href={item.link}>{item.label}</LoLink>
      </Box>
    )
  })
  return (
    <HStack width='100%' spacing={4} justifyContent={"space-around"}>
      {items}
    </HStack>
  )
}
