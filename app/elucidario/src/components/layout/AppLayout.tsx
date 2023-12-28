import { Container } from '@chakra-ui/react'
import { Platform } from './Platform'
import { Menu } from './Menu'

export const AppLayout = ({ locale, children }) => {
  return (
    <>
      <Container maxW='container.xxl' centerContent>
        <Platform w={'100%'}>
          <Menu locale={locale}/>
        </Platform>
      </Container>
      <Container w='container.xl' centerContent>
        <Platform mt={4}>{children}</Platform>
      </Container>
    </>
  )
}
