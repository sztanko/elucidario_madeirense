"""
Install an additional SDK for JSON schema support Google AI Python SDK

$ pip install google.ai.generativelanguage
"""

import os
import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import content

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model


CATEGORIES_TEXT_EN = """Up to 3 categories describing the article, must be one of the following:
            History - Encompasses historical events, cultural practices, traditions, and societal structures.
            People - Focuses on the lives of notable individuals from Madeira.
            Geography - Covers landforms, geographical locations, and geological aspects.
            Plants - Deals with the plant life of Madeira, including trees, flowers, and other vegetation.
            Animals - Focuses on the animal life of Madeira, including birds, insects, and marine creatures.
            Politics - Covers political structures, governance, and administrative bodies.
            Economy - Includes articles about industries, commerce, and trade practices.
            Farming - Covers farming practices, crops, and agricultural techniques.
            Travel - Focuses on aspects related to tourism, travel, and points of interest for visitors.
            Religion - Encompasses religious practices, beliefs, and folk traditions.
            Arts - Covers the artistic expressions, architecture and buildings of Madeira.
            Education - Includes information about educational institutions and scientific studies.
            Places - Focuses on specific places, towns, and regions within Madeira.
            Maritime - Covers the aspects of maritime activities, fishing and navigation.
            Health - Relates to health, diseases, and medical practices.
            Military -  Includes articles related to military events, fortifications, and defense structures.
            Transport - Covers roads, waterways and other forms of infrastructure.
            Cuisine -  Includes articles about local cuisine, beverages and their production.
            Language - Focuses on linguistic aspects of the archipelago, and the literary works
            Legal - Includes information about the government and legal systems of Madeira."""

CATEGORIES_TEXT_PT = """Até 3 categorias que descrevam o artigo, tem de ser uma das seguintes:

            History - Abrange acontecimentos históricos, práticas culturais, tradições e estruturas sociais.
            People - Concentra-se nas vidas de pessoas notáveis da Madeira.
            Geography - Cobre as formações da terra, localizações geográficas e aspetos geológicos.
            Plants - Trata da flora da Madeira, incluindo árvores, flores e outras plantas.
            Animals - Enfoca a fauna da Madeira, incluindo pássaros, insetos e criaturas marinhas.
            Politics - Abrange a estrutura política, a governação e órgãos administrativos.
            Economy - Inclui artigos sobre indústrias, comércio e práticas de negócios.
            Farming - Cobre práticas agrícolas, culturas e técnicas de plantação.
            Travel - Centra-se nos aspetos relacionados com turismo, viagens e pontos de interesse para visitantes.
            Religion - Envolve práticas religiosas, crenças e tradições populares.
            Arts - Cobre expressões artísticas, arquitetura e edifícios da Madeira.
            Education - Inclui informações sobre instituições de ensino e estudos científicos.
            Places - Foca-se em locais específicos, vilas e regiões da Madeira.
            Maritime - Abrange atividades marítimas, pesca e navegação.
            Health - Relaciona-se com saúde, doenças e práticas médicas.
            Military - Inclui artigos sobre eventos militares, fortificações e estruturas de defesa.
            Transport - Cobre estradas, vias fluviais e outras formas de infraestrutura.
            Cuisine - Inclui artigos sobre a culinária local, bebidas e sua produção.
            Language - Centra-se nos aspetos linguísticos do arquipélago, bem como em obras literárias.
            Legal - Inclui informações acerca do governo e dos sistemas legais na Madeira."""

descriptions_en = {
    "name": "article name",
    "alternative_name": "based on the contect, suggest the best possible name for this article in portuguese, if different from the original. Should not include 'Madeira' in it, as the whole encyclopedia is about Madeira.",
    "description": 'short description of article in english, one sentence, max 20 words. When summarizing an article, avoid starting with "this article" and go straight to the core content.',
    "length": "approximate length of the article, in characters",
    "begins_with": "exact first 30 characters of the article, first line only, so I can find it in the original text. if first line is shorter than 30 characters, use the whole line.",
    "ends_with": "exact last 30 characters of the article, last line only, so I can find it in the original text. if last line is shorter than 30 characters, use the whole line.",
    "is_reference": "is this article just a reference to another article? It is very short, and only contains something like 'V. <referenced article name>' or 'Vid. <referenced article name>' or '(V. este nome)'",
    "reference_name": "if yes, specify the name of the referenced article",
    "categories": CATEGORIES_TEXT_EN,
}

descriptions_pt = {
    "name": "nome do artigo",
    "alternative_name": "com base no conteúdo, sugira o melhor nome possível para este artigo em português, se diferente do original. Não deve incluir 'Madeira' nele, pois toda a enciclopédia é sobre Madeira.",
    "description": "descrição curta do artigo em português, em uma frase, no máximo 20 palavras. Ao resumir um artigo, evite frases como 'este artigo' e vá direto ao conteúdo principal.",
    "length": "comprimento aproximado do artigo, em caracteres",
    "begins_with": "primeiros 30 caracteres exatos do artigo, apenas na primeira linha, para que eu possa encontrá-lo no texto original. se a primeira linha for mais curta que 30 caracteres, use a linha inteira.",
    "ends_with": "últimos 30 caracteres exatos do artigo, apenas na última linha, para que eu possa encontrá-lo no texto original. se a última linha for mais curta que 30 caracteres, use a linha inteira.",
    "is_reference": "este artigo é apenas uma referência para outro artigo? É muito curto e contém somente algo como 'V. <nome do artigo referenciado>' ou 'Vid. <nome do artigo referenciado>' ou '(V. este nome)'",
    "reference_name": "se sim, especifique o nome do artigo referenciado",
    "categories": CATEGORIES_TEXT_EN,
}

descriptions = descriptions_en

split_article_prompt_intro_en = """Attached part of a text of Elucidario Madeirense, an encyclopedic work, containing thousands of articles.
        Output a list of dicts, each dict containing information about the article. Ignore introductory text and only consider articles.

        Each row should have the following keys:"""

split_article_prompt_intro_pt = """Trecho de um texto do Elucidário Madeirense, uma obra enciclopédica que contém milhares de artigos.
        Retorna uma lista de dicionários, cada um contendo informações sobre o artigo. Ignora o texto introdutório e considera apenas os artigos.

        Cada linha deve ter as seguintes chaves:"""

split_articles = {
    "prompt": f"""${split_article_prompt_intro_en}
        "name" - ${descriptions["name"]}
        "alternative_name" - ${descriptions["alternative_name"]}
        "description" - ${descriptions["description"]}
        "length" - ${descriptions["length"]}
        "begins_with" - ${descriptions["begins_with"]}
        "ends_with" - ${descriptions["ends_with"]}
        "is_reference" - ${descriptions["is_reference"]}
        "reference_name" - ${descriptions["reference_name"]}
        "categories" = ${descriptions["categories"]}
        """,
    "schema": content.Schema(
        type=content.Type.ARRAY,
        items=content.Schema(
            type=content.Type.OBJECT,
            enum=[],
            required=["name", "description", "length", "begins_with", "ends_with", "is_reference", "categories"],
            properties={
                "name": content.Schema(
                    type=content.Type.STRING,
                    description=descriptions["name"],
                ),
                "alternative_name": content.Schema(
                    type=content.Type.STRING,
                    description=descriptions["alternative_name"],
                ),
                "description": content.Schema(
                    type=content.Type.STRING,
                    description=descriptions["description"],
                ),
                "length": content.Schema(
                    type=content.Type.INTEGER,
                    description=descriptions["length"],
                ),
                "begins_with": content.Schema(
                    type=content.Type.STRING,
                    description=descriptions["begins_with"],
                ),
                "ends_with": content.Schema(
                    type=content.Type.STRING,
                    description=descriptions["ends_with"],
                ),
                "is_reference": content.Schema(
                    type=content.Type.BOOLEAN,
                    description=descriptions["is_reference"],
                ),
                "reference_name": content.Schema(
                    type=content.Type.STRING,
                    description=descriptions["reference_name"],
                ),
                "categories": content.Schema(
                    type=content.Type.ARRAY,
                    description="Up to three categories describing the article, chosen from a predefined list.",
                    items=content.Schema(
                        type=content.Type.STRING,
                        enum=[
                            "History",
                            "People",
                            "Geography",
                            "Plants",
                            "Animals",
                            "Politics",
                            "Economy",
                            "Farming",
                            "Travel",
                            "Religion",
                            "Arts",
                            "Education",
                            "Places",
                            "Maritime",
                            "Health",
                            "Military",
                            "Transport",
                            "Cuisine",
                            "Language",
                            "Legal",
                        ],
                    ),
                ),
            },
        ),
    ),
}
