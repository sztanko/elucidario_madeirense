import { Container } from '@chakra-ui/react'
import { Platform } from './Platform'
import { Menu } from './Menu'

export const AppLayout = ({ children }) => {
  return (
    <>
      <Container maxW='container.xxl' centerContent>
        <Platform w={'100%'}>
          <Menu/>
        </Platform>
      </Container>
      <Container w='4xxl' maxW='container.xl' centerContent>
        <Platform mt={4}>{children}</Platform>
      </Container>
    </>
  )
}
