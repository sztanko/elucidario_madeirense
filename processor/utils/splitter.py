from bs4 import BeautifulSoup
import logging
import re

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
 

def build_chunk(title, id, body_content):
    return f"<div class='article' id='a_{id}'><h1>{title}</h1><div class='article-body'>{body_content}</div></div>"


def split_html(html, size_threshold):
    """
    Splits the HTML string into chunks, each smaller than the specified size threshold.
    Ensures that top level HTML tags are not split in half.

    :param html: HTML content as a string
    :param size_threshold: Maximum size of each chunk
    :return: List of strings, each representing a chunk of the original HTML
    """
    soup = BeautifulSoup(html, "html.parser")
    chunks = []
    current_chunk = ""
    # logging.info(f"Size threshold: {size_threshold}")
    # logging.info(f"Total elements: {len(soup.contents)}")

    for element in soup.contents:
        # Convert the element to string if it is a NavigableString
        str_element = str(element)
        # logging.info(str_element)
        # logging.info(f"Current element size: {len(str_element)}")
        if len(str_element) > size_threshold:
            logging.info(f"Element size {len(str_element)} is larger than {size_threshold}, so splitting it recursively")
            logging.info(str_element)
            # chunks += split_html(str_element, size_threshold)
            # continue
        if len(current_chunk) + len(str_element) <= size_threshold:
            current_chunk += str_element
        else:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = str_element

    # Add the last chunk if it exists
    if current_chunk:
        chunks.append(current_chunk)

    logging.info(f"Split {len(html)} chars into {len(chunks)} chunks")
    return chunks

def split(text, regex_pattern):
    parts = re.split(f'({regex_pattern})', text)
    # Rejoin the split parts, alternating between non-matched and matched parts
    result = []
    for non_matched, matched in zip(parts[0::2], parts[1::2] + ['']):
        result.append(non_matched)
        if matched:  # Only add the matched part if it's not empty
            result.append(matched)
    return result



def split_markdown(markdown, size_threshold):
    # Let's first split by H2 headers
    splits_by_header = split(markdown, "##")
    out = []
    for h in splits_by_header:
        if len(h) <= size_threshold:
            out.append(h)
        else:
            paragraphs = split(h, "\n\n")
            for p in paragraphs:
                if len(p) <= size_threshold:
                    out.append(p)
                else:
                    out += split(p, r'\b\w{5,}\.\s(?=[A-Z])') #r'\.\s(?=[A-Z])')
    return merge_small_chunks(out, size_threshold)

def merge_small_chunks(chunks, size_threshold):
    """
    Merges small tet chunks to maximize their size up to the specified size threshold,
    while keeping the chunks' order.

    :param chunks: List of text chunks as strings
    :param size_threshold: Maximum size of each merged chunk
    :return: List of strings, each representing a merged chunk of HTML
    """
    merged_chunks = []
    current_chunk = ""

    for chunk in chunks:
        if len(current_chunk) + len(chunk) <= size_threshold:
            current_chunk += chunk
            # logging.info(f"Current chunk size: {len(current_chunk)}")
        else:
            if current_chunk:
                merged_chunks.append(current_chunk)
            current_chunk = chunk

    # Add the last chunk if it exists
    if current_chunk:
        merged_chunks.append(current_chunk)
    logging.info(f"Merged {len(chunks)} chunks into {len(merged_chunks)} chunks")
    return merged_chunks


def split_article(html_string, size_threshold):
    if len(html_string) <= size_threshold:
        return [html_string]
    soup = BeautifulSoup(html_string, "html.parser")
    title = soup.find("h1").string
    article = soup.find("div", class_="article")
    body = article.find("div", class_="article_body")
    id = article.attrs["id"][2:]
    body_html = body.decode_contents()
    # logging.info(f"Body size: {len(body_html)}")
    # logging.info(body_html)
    # logging.info("------------------------")
    if "<h2>" in body_html:
        header_splits = body_html.split("<h2>")
        split_by_header = [header_splits[0]] + ["<h2>" + h for h in header_splits[1:]]
        logging.info(f"Split by headers: {len(split_by_header)}")
    else:
        split_by_header = [body_html]
        logging.info("No headers found")

    chunks = []
    for pg in split_by_header:
        if len(pg) <= size_threshold:
            chunks.append(pg)
            # logging.info(f"Chunk size: {len(pg)} is smaller then {size_threshold}, so leaving it as it is ")
        else:
            logging.info(f"Splitting {len(pg)} chars into chunks")
            chunks += split_html(pg, size_threshold)

    merged_chunks = merge_small_chunks(chunks, size_threshold)
    chunk_html = [build_chunk(title, id, chunk) for chunk in merged_chunks]
    
    for chunk in chunk_html:
        logging.info(f"FINAL Chunk size: {len(chunk)}")
    logging.info(f"Returning {len(chunk_html)} chunks")
    return chunk_html


if __name__ == "__main__":
    banco_test = "Têm agencias na Madeira as seguintes instituições de credito continentais: Banco de Portugal, Banco Nacional Ultramarino e Companhia Geral de Credito Predial Português. Não existe agora nenhum banco com sede na Madeira, mas além das referidas agencias, há no Funchal diversas casas que fazem em maior ou menor escala as operações proprias dos estabelecimentos bancarios.\n\nA agencia do Banco de Portugal já existia em 1876, estando então a cargo do negociante João José Rodrigues Leitão, que viera para a Madeira em 1853, mas como este negociante falisse em 1878, foi a mesma agencia entregue a Tomás Antonio Gomes, que dela tomou posse a 15 de Julho desse ano.\n\nPor causa da falencia de João José Rodrigues Leitão, esteve na Madeira o Director do Banco de Portugal Henrique de Barros Gomes, que conseguiu que entre o negociante falido e os seus credores se celebrasse um contrato bastante favoravel aquele estabelecimento de credito. Por esse contracto todos os bens do negociante falido foram hipotecados ao Banco, garantindo este aos demais credores o embôlso de 50 por cento dos seus creditos pagos em três prestações. Antes da falencia, o penhor a favor do Banco era constituido especialmente por vinhos, aos quais fora dado o valor de 102.464.408 réis.\n\nDesde os principios de 1888 que a agencia do Banco de Portugal nesta ilha é caixa do tesouro pelas operações a fazer com o Estado, isto de harmonia com o estabelecido do contracto de 10 de Dezembro de 1887. Nos primeiros tempos, isto é, antes da constituição definitiva da agencia com as atribuições que lhe foram dadas pelo mesmo contrato, serviu de agente provisorio do Banco nesta ilha o antigo tesoureiro pagador Raimundo Sieuve de Meneses.\n\nDe 1904 até o presente têm sido agentes do Banco de Portugal nesta ilha os seguintes funcionarios: Comendador Luiz de Freitas Branco, Henrique Augusto Vieira de Castro, Eduardo Martins da Silveira, Fernando Ferro, Conselheiro Henrique de Sá Nogueira, Francisco Camilo Meira, Raul Rodrigues Cohen e Antonio Noronha de Barros. O Banco há muitos anos que mantém dois agentes seus na direcção dos negocios da sua agencia na Madeira.\n\nA agencia do Banco de Portugal no Funchal, além de ser caixa do Governo, faz emprestimos sobre papéis de credito, compra e vende cambiais, saca e desconta letras, passa cartas de credito, etc.. Também recebe depositos, mas não paga por eles juro algum.\n\nA filial do Banco Nacional Ultramarino foi instalada a 10 de Fevereiro de 1919, e faz as mesmas operações bancarias da agencia do Banco de Portugal, com a diferença apenas de pagar um certo juro pelos depositos a prazo e à ordem que recebe. Em ambas estas agencias a taxa do juro é 6 por cento.\n\nO Banco Commercial de Lisboa esteve representado outrora nesta ilha pela firma comercial Freitas & Macedo, que faliu em 1881, e o primeiro agente da Companhia Geral de Credito Predial Português foi o já mencionado João José Rodrigues Leitão. O Banco Nacional Ultramarino possuía um representante na Madeira antes da criação da filial a que já nos referimos, tendo sido o falecido negociante Luiz Gomes da Conceição quem primeiro desempenhou aqui este cargo.\n\nA 1 de Junho de 1875 instalou se no Funchal o Banco Commercial da Madeira, sociedade anonima de responsabilidade limitada, tendo os seus estatutos a data de 25 de Abril de 1875. Segundo estes estatutos, os fins do banco eram: emitir notas ao portador, pagaveis em ouro ou prata; receber depositos em conta corrente e a prazo fixo, abonando juros aos depositantes; descontar letras de cambio e da terra, titulos comerciais e á ordem e titulos do estado e de quaisquer estabelecimentos publicos; fazer emprestimos sobre hipotecas, titulos da divida publica, acções de bancos e companhias e objectos de ouro e prata; tomar letras de cambio e de risco maritimo; fazer liquidações de heranças e operações de credito agricola e industrial, etc., etc..\n\nSegundo os mesmos estatutos, o capital social era de 1:200 contos divididos em acções de 100$000 réis, devendo a emissão do capital ser feita em duas series de 600 contos cada uma, constituindo a primeira serie, já emitida em 24 de Abril de 1875, o fundo inicial destinado às operações do banco. A maior parte das acções tinha sido tomada na cidade do Porto.\n\nFizeram parte da primeira direcção do banco os cidadãos João de Sales Caldeira, Carlos Bianchi e José Paulo dos Santos, e do primeiro conselho fiscal os cidadãos William Hinton, Manuel Inisio da Costa Lira, Roberto Wilkinson, Antonio Caetano Aragão e Manuel Figueira de Chaves. O primeiro presidente da assembleia geral foi Severiano Alberto de Freitas Ferraz.\n\nDos relatorios que temos presentes relativos às gerencias do Banco Commercial da Madeira, vê se que o activo e passivo deste estabelecimento foi o seguinte nos anos abaixo designados:\n\n| Ano  | Valor, réis          |\n|------|------------------|\n| 1877 | 1.273.156.226 |\n| 1879 | 1.195.087.258 *  |\n| 1884 | 1.170.142.412 *  |\n| 1885 | 1.167.733.507 *  |\n| 1856 | 1.194.311.844 *  |\n\nO banco teve 39.942.732 réis de lucros em 1877 e 32.851.757 réis em 1879, distribuindo no primeiro destes anos a quantia de réis 36.000.000 pelos accionistas, e no segundo a quantia de 28.125.000 réis. Em 1884, 1885 e 1886 já o banco não distribuíu dividendo, havendo no segundo destes anos 6:000 acções emitidas, sendo 3:197 nominativas e 2803 ao portador.\n\nO Banco Commercial da Madeira dissolveu se em 1887, com prejuízos para os accionistas, tendo concorrido bastante para este resultado o estarem mal garantidos muitos dos seus capitais. A desvalorização que sofreram as propriedades em virtude da molestia que devastou os canaviais, agravou bastante a situação do banco, a qual, como se vê do relatorio apresentado em assembleia geral de 29 de Janeiro de 1880, não era já muito prospera em 1879, devido ao retraimento de capitais, provocado pela lei da unificação da moeda. Já no ano de 1878 tinha a extraordinaria alta dos cambios obstado à transferencia de fundos, operação esta que dera anteriormente excelentes vantagens ao banco.\n\nEm 1800 recomendou o governo da metropole numas instruções que dirigiu ao Governador e Capitão General D. José Manuel da Camara, a criação duma caixa de credito na Madeira, e em 1 de Julho de 1824 enviou o Governador e Capitão General D. Manuel de Portugal e Castro uma representação ao governo central, pedindo a criaçao dum banco no Funchal. Tais estabelecimentos não chegaram a ser criados, e o mesmo aconteceu com outros da mesma natureza que se pretendeu fundar mais tarde nesta cidade. No numero 169 do Imparcial, de 1843, vem publicado na integra um projecto de regulamento para a criação dum banco na Madeira, e no numero 145 e seguintes do jornal A Ordem, de 1854, encontra se o projecto apresentado ao governo para a criação dum banco comercial e agricola na ilha.\n\nA Comissão Administrativa da Santa Casa da Misericordia resolveu em 1873, de harmonia com o disposto na lei de 22 de Junho de 1867, fundar nesta cidade um banco de credito agricola e industrial com a importancia dos seus capitãis mutuados, admitindo accionistas para com o produto das acções elevar o capital do banco, mas a pesar de ter havido para este fim uma reunião no Palacio de São Lourenço no dia 10 de Julho do mesmo ano, em que se estabeleceu que as acções fossem de 20:000 réis cada uma e que a subscrição fosse aberta imediatamente, não chegou a referida instituição a ser uma realidade, por motivos que inteiramente desconhecemos.\n\nEm 1886 aconselhou o falecido Conde do Canavial a criação dum banco industrial na Madeira para emprestar dinheiro a juro modico à industria e à agricultura, mas essa ideia, já apresentada em 1879 pelo mesmo titular, não foi aproveitada, com o que bastante sofreu a nossa terra, onde era grande a falta de recursos pecuniarios, devido à falencia de cinco das mais importantes casas comerciais, com um prejuízo de cêrca de 1:600 contos, e à crise agricola provocada pelo desaparecimento da cana sacarina.\n\nHouve tempos em que a Santa Casa da Misericordia e a Caixa dos Orfãos emprestavam dinheiro ao juro de 5 por cento; eram porém tão diminutas as quantias de que essas instituições podiam dispor, que bem poucos eram aqueles que conseguiam obter capitais para as suas transações, em condições tão vantajosas. Os particulares exigiam quasi sempre o juro de 12 e 15 por cento, e não faltava quem tomasse dinheiro a vintém por pataca ao mês, juro este correspondente a 24 por cento ao ano.\n\nHa quarenta anos os bancos emprestavam dinheiro a 8 por cento, tendo o emprestado antes disso a 12 por cento, e ainda hoje é frequente fazerem se emprestimos e descontos na primeira destas condições, a pesar das agencias do Banco de Portugal e do Banco Nacional Ultramarino terem estabelecido desde há muito o juro de 6 por cento para as transacções que realizam. Certas formalidades exigidas pelas agencias destes bancos, e ainda outras circunstancias, dão motivo a que nem todos possam aproveitar se das vantagens que elas oferecem, sendo a falta de capitais baratos uma das causas da nossa industria e agricultura lutarem por vezes com graves embaraços, e de certas iniciativas uteis que de longe em longe aparecem, nem sempre serem coroadas de prospero resultado.\n\nAs casas bancarias estabelecidas agora no Funchal são as de Blandy Brothers & C., Henrique Figueira da Silva, Reid Castro & C.a, Rocha Machado & Ca e Sardinha & C.a. Estas casas que realizam as operações bancarias exigidas pelo comercio do Funchal, e ainda outras, estão todas em estado bastante prospero, devido à sua excelente administração e à confiança de que gozam no mercado (1922).\n\nSobre a maneira como em antigos tempos se faziam transferencias de fundos ou se obtinha dinheiro por emprestimo para satisfazer compromissos comerciais, nada de positivo podemos dizer, mas é licito supor que fossem. Os flamengos os primeiros que se entregaram aqui a operações bancarias, seguindo se lhes os ingleses que, como é sabido, adquiriram grande proponderancia nos negocios da Ilha, do meado do seculo XVII em diante.\n\nAs varias tentativas que se fizeram desde 1800 até 1873 para a fundação de estabelecimentos de credito na Madeira, mostram que havia o desejo de criar para o comercio, para a industria e para a agricultura madeirenses vantagens de que estas classes não gozavam,sendo na verdade para estranhar que nenhuma dessas tentativas desse resultado, quando é sabido que os agiotas que então abundavam na ilha raras vezes emprestavam dinheiro com interesse inferior a 10, 12 e 15 por cento, o que constituía uma exploração a que convinha pôr termo.\n\nEm 23 de Junho de 1920 abriu o Banco da Madeira, que ficou instalado provisoriamente no rés do chão dum prédio à rua do Comercio. O capital, que a principio era de 100.000.000, foi elevado depois a 200.000.000 e finalmente à quantia de 400.000.000, tendo a data de 7 de Janeiro de 1921 o decreto que autorizou a constituição definitiva do mesmo Banco."
    
    single_body_text="Data do meado do século XV a criação das vilas e municípios do Funchal, Machico e Porto Santo, sendo estas localidades as capitais das três capitanias em que foi dividido o arquipelago madeirense. A capitania do Funchal, e particularmente a sua sede, que era a vila do mesmo nome, tomou desde os tempos primitivos da colonização um notável incremento e cresceu rapidamente em prosperidades, formando-se dentro dela povoações importantes, que em breve atingiram grande desenvolvimento, impondo-se deste modo a necessidade da criação de municípios autónomos, para comodidade dos povos e boa administração dos negócios públicos. Foi o que aconteceu com a instituição das vilas e municípios da Ponta do Sol e da Calheta. A primeira foi criada em 1501, e com bons fundamentos se conjectura que a segunda fosse criada aproximadamente pela mesma época. E para lamentar que não haja noticia do diploma que elevou a vila da freguesia da Calheta. O alvará régio que criou a vila da Ponta do Sol está tombado no arquivo municipal do Funchal, e também dele existe copia no arquivo da câmara daquela vila. Acerca do diploma respeitante á Calheta, diz o dr. Alvaro Rodrigues de Azevedo: “Da carta que elevou o lugar da Calheta a Villa Nova da Calheta não existe registo na respectiva Câmara, porque os antigos paços do Concelho e archivo originário forão destruídos pelo mar, segundo o Presidente da mesma Câmara informa em oficio de 30 de outubro deste anno de 1871; também não está registada no archivo da Câmara do Funchal; e em nenhum dos manuscriptos que possuímos vem copiada. Só na Breve Noticia de Paulo Perestrello, pag. 54, achamos nota de que a Calheta fora feita villa em 1511, O que é manifesto erro, talvez typographico; porque do diploma infra se mostra que a Villa Nova da Calheta já o era em agosto de 1502”. O Diploma infra a que aqui se faz referência, é uma resposta, datada de 16 de Agosto de 1502, contendo algumas instruções dirigidas pelo monarca á câmara municipal do Funchal. Em vários escritos se alude á frase, que se tornou bastante conhecida - á sua muito amada villa da Calheta - e que se atribue ao rei D. Manuel I, numa carta dirigida á câmara deste município. Não conhecemos o documento em que essa frase vem exarada e nem podemos assegurar que ela seja de uma legitima autenticidade. A ser verdadeira, quereria certamente o monarca venturoso referir-se á distinta fidalguia desta vila ou município, pois é sabido que houve ali uma numerosa pléiade de nobres cavaleiros, muitos dos quais se distinguiram valorosamente em Africa, na Índia e no Brasil. Da predilecção de D. Manuel I pela vila da Calheta, existe uma prova eloquente no rico sacrario oferecido á sua igreja matriz e a que já nos referimos no artigo consagrado a esta freguesia. Desejando o monarca galardoar os serviços prestados pelo 51. capitão-donatario do Funchal Simão Gonçalves da Câmara, e ainda honrar nele os feitos e acções heróicas dos seus maiores, e querendo também dar maior lustre á rica e importante casa de que ele era o representante, agraciou-o com o título de conde, pelo alvará régio de 20 de Agosto de 1576, sendo a vila da Calheta, pela sua importância e nobres tradições, escolhida para sede do novo condado. Este título, como noutro lugar se dirá, foi encorporado no marquesado de Castelo Melhor, sendo os respectivos titulares também condes da Calheta, até que o decreto de 15 de Outubro de 1910 aboliu todos os títulos nobiliarquicos. E interessante o trecho de Gaspar Frutuoso, que em seguida transcrevemos, relativamente aos pontos que deixamos referidos: “Neste logar da Calheta, mais abaixo chegado a huma fermosa ribeira, se fundou a Villa, que tomou o nome da Calheta, a mais fértil de todas as da ilha, por ter mayor comarca. He esta villa tão nobre em seus moradores, como abastada pelos muitos e baratos mantimentos que nella se achão. Desta sahiram em companhia dos capitães do Funchal muitos e nobres cavalleiros a servir El-Rey á sua custa nos logares de Africa, e nos socorros que os capitães levaram: onde todos, além de darem mostras de suas pessoas, gastaram muito do seu, porque eram ricos, pelas grossas fazendas que neste termo ha, como a do Arco tão afamada, e outras, que andão agora divididas por diversos herdeiros. Esta Villa da Calheta e seu termo foi o condado do Illustrissimo Capitam Simão Gonçalves da Câmara, Conde desta Villa Nova da Calheta, como se dirá em seu logar”. Como já vimos no artigo Alfândegas, foi esta vila sede duma pequena delegação aduaneira ou posto fiscal, como então se chamava, e ali se arrecadou primitivamente o imposto sobre o açúcar, que depois passou a ser cobrado na alfândega do Funchal. Houve na Calheta os cargos de quintador e escrivão dos quintos, cujas atribuições consistiam na aplicação dos tributos que recaíam sobre o açucar que ali se fabricava. Estes logares foram extintos por alvará régio de 30 de Julho de 1686. Na câmara desta vila deixou o juiz de fora dr. Antonio Rodrigues Veloso de Oliveira exaradas umas instruções sobre cousas agrícolas, verdadeiramente notáveis para a época, e de que têm sido publicados vários trechos em alguns jornais madeirenses. “Versam, diz-se algures, sobre a cultura da vinha e outras plantas - o castanheiro nos baldios, as árvores de frutos nos logares abrigados, os algodoeiros junto ao mar, as amoreiras nas estradas e logares públicos, os pinhais nas terras incapazes de outra produção, os vegetais usados nas pharmacias, as searas de milho, a criação de gados, de prados artificiais, bardos de resguardo e outros alvitres”. Estas instruções ainda hoje se lêem com algum aproveitamento. Na área deste concelho fica o conhecido e muito visitado sítio do Rabaçal, a que consagraremos um desenvolvido artigo. O actual concelho da Calheta, criado em 1835, e o antigo município ou vila, não se diferenciam muito sensivelmente no que diz respeito á extensão das suas áreas. Desde 1835 até o presente, tem no entretanto tido algumas variantes, dalgumas das quais podemos dar noticia. Em 1849 foi suprimido o concelho do Porto do Moniz que também tinha sido criado em 1835, e as freguesias das Achadas da Cruz e Ponta do Pargo passaram a fazer parte do Concelho da Calheta, mas de novo estas paróquias se encorporaram no concelho do Porto do Moniz, quando este foi restaurado em 1855. O decreto de 26 de Junho de 1871 desagregou a freguesia da Ponta do Pargo do concelho do Porto do Moniz e anexou-a ao da Calheta. Em 1895 passou o concelho do Porto do Moniz, por uma nova supressão, sendo anexado aos concelhos da Calheta e S. Vicente, para novamente ser restaurado no ano de 1898. Tem este concelho as freguesias da Calheta, Estreito da Calheta, Arco da Calheta, Prazeres, Jardim do Mar, Paul do Mar, Fajã da Ovelha e Ponta do Pargo. Como acima fica dito, a criação da vila da Ponta do Sol data de 1501, conjecturando o ilustre comentador das Saudades da Terra que a da Calheta teria sido em época aproximada á desse ano. Hoje pode precisar-se a data exacta dessa criação, depois que no ano de 1900 o dr. Damião Peres publicou uma segunda edição da obra de Gaspar Frutuoso, enriquecendo-a com algumas valiosas anotações. Numa delas, a pag. 118 e ss., vem integralmente transcrita a carta regia de I de Julho de 1502, que criou a vila da Calheta e que é documento sobremaneira interessante."
    
    text = single_body_text
    chunks = split_markdown(text, 3000)
        
    print("ORIGINAL:")
    print(text)
    print("\n\n\n")
    print("Chunks:")
    for chunk in chunks:
        print(f"-------- {len(chunk)}")
        print(chunk)
    print(len(chunks))