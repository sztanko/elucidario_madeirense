import { Container } from '@chakra-ui/react'
import { Platform } from './Platform'
import { TopMenu } from './TopMenu'

export const AppLayout = ({ locale, children }) => {
  return (
    <>
      <Container maxW={['100%', 'container.xxl']} centerContent padding={0}>
        <Platform w={'100%'} margin={0} padding={0}>
          <TopMenu locale={locale}/>
        </Platform>
      </Container>
      <Container centerContent border="none" mt={8} maxW={{ base: "100%", lg: "80%" }}>
        <Platform mt={4}>{children}</Platform>
      </Container>
    </>
  )
}
