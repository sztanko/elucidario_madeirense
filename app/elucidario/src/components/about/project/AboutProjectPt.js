import { Text, Link, UnorderedList, ListItem } from '@chakra-ui/react'

export default function AboutProjectPt () {
  return (
    <>
      <Text mb={4}>
        Em apreço pelos momentos encantadores e pela calorosa hospitalidade que
        vivenciei na ensolarada ilha da Madeira e entre seus habitantes,
        sinto-me compelido por um dever sincero de preservar e disseminar as
        contribuições históricas de seus pensadores mais distintos na maneira
        mais acessível desta era digital. Este site é um empreendimento pessoal,
        realizado em meu tempo livre sem nenhum financiamento. É open source, e
        o código está disponível aqui:{' '}
        <Link
          href='https://github.com/sztanko/elucidario_madeirense'
          isExternal
        >
          https://github.com/sztanko/elucidario_madeirense
        </Link>
        .
      </Text>
      <Text mb={4}>
        Todos os artigos neste site são derivados das versões em PDF do livro,
        pois não tenho acesso ao original. Embora eu tenha me esforçado para
        corrigir a maioria dos erros resultantes do reconhecimento ótico de
        caracteres, não posso garantir que todos foram abordados.
        Ocasionalmente, alguns artigos se fundem em um.
      </Text>
      <Text mb={4}>
        Para formatação e subsequente tradução do texto, foram empregados
        Modelos de Linguagem Avançados como o ChatGPT e o Claude. Reconheço que
        nenhum método é infalível, e às vezes ocorrem erros significativos na
        tradução e no layout. No entanto, planejo reprocessar o conteúdo à
        medida que os modelos melhorarem. Todas as imagens também foram geradas
        usando tecnologia de IA.
      </Text>
      <Text mb={4}>
        Meu nome é Dimi, resido em Londres, Reino Unido, e sou profundamente
        fascinado pela cultura e história madeirense. Não sou historiador, nem
        falo português (embora esteja aprendendo). Sinta-se à vontade para
        entrar em contato comigo via e-mail em{' '}
        <Link href='mailto:info@elucidariomadeirense.pt'>info@elucidariomadeirense.pt</Link>.
      </Text>
      <Text mb={4}>Gostaria de estender minha gratidão a:</Text>
      <UnorderedList mb={4}>
        <ListItem>
          Duarte V R Afonso (
          <Link
            href='https://www.scribd.com/user/31817682/Duarte-V-R-Afonso'
            isExternal
          >
            https://www.scribd.com/user/31817682/Duarte-V-R-Afonso
          </Link>
          ) por ter disponibilizado as versões em PDF do livro original.
        </ListItem>
        <ListItem>
          Os desenvolvedores de Modelos de Linguagem Avançados modernos por me
          permitirem empreender tarefas que pareciam inatingíveis há apenas um
          ano atrás.
        </ListItem>
        <ListItem>
          Minha esposa e filho pela paciência sem limites que demonstraram
          enquanto eu desenvolvia este site.
        </ListItem>
      </UnorderedList>
    </>
  )
}
