"""
Install an additional SDK for JSON schema support Google AI Python SDK

$ pip install google.ai.generativelanguage
"""

import os
import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import content
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

LANG = "en" # "en" or "pt"

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
    "alternative_name": "based on the content, suggest the best possible name for this article in portuguese, if different from the original. Should not include 'Madeira' in it, as the whole encyclopedia is about this island.",
    "description": 'short description of article in portuguese, one sentence, max 20 words. When summarizing an article, avoid starting with "this article" and go straight to the core content.',
    "begins_with": "exact first 30 characters of the article, first line only, so I can find it in the original text. if first line is shorter than 30 characters, use the whole line.",
    "ends_with": "exact last 30 characters of the article, last line only, so I can find it in the original text. if last line is shorter than 30 characters, use the whole line.",
    "is_reference": "is this article just a reference to another article? It is very short, and only contains something like 'V. <referenced article name>' or 'Vid. <referenced article name>' or '(V. este nome)'",
    "reference": "Name of the referenced article. Typically references to other articles look like V. <referenced article name>' or 'Vid. <referenced article name>' or '(V. este nome)'",
    "references": "List of all references to other articles",
    "categories": """Up to 3 categories describing the article""",    
}

descriptions_pt = {
    "name": "nome do artigo",
    "alternative_name": "com base no conteúdo, sugira o melhor nome possível para este artigo em português, se diferente do original. Não deve incluir 'Madeira' nele, pois toda a enciclopédia é sobre esta ilha.",
    "description": "descrição curta do artigo em português, em uma frase, no máximo 20 palavras. Ao resumir um artigo, evite frases como 'este artigo' e vá direto ao conteúdo principal.",
    "begins_with": "primeiros 30 caracteres exatos do artigo, apenas na primeira linha, para que eu possa encontrá-lo no texto original. se a primeira linha for mais curta que 30 caracteres, use a linha inteira.",
    "ends_with": "últimos 30 caracteres exatos do artigo, apenas na última linha, para que eu possa encontrá-lo no texto original. se a última linha for mais curta que 30 caracteres, use a linha inteira.",
    "is_reference": "este artigo é apenas uma referência para outro artigo? É muito curto e contém somente algo como 'V. <nome do artigo referenciado>' ou 'Vid. <nome do artigo referenciado>' ou '(V. este nome)'",
    "reference": "se sim, especifique o nome do artigo referenciado",
    "categories": "Até 3 categorias que descrevam o artigo",
}

if LANG == "en":
    descriptions = descriptions_en
else:
    descriptions = descriptions_pt

structure_article_prompt_intro_en = """Following is a text of an article from Elucidario Madeirense, an encyclopaedic work about Madeira.
Return an object containing some metadata about the article, including categories, references, and other information.

Object should have the following keys:"""

structure_article_prompt_intro_pt = """Segue-se um texto de um artigo do Elucidário Madeirense, uma obra enciclopédica sobre a Madeira.
Retorna um objeto contendo metadados sobre o artigo. 
O objeto deve conter as seguintes chaves:"""


html_article_prompt_intro_en = """Following is a text of one or more articles from Elucidario Madeirense, an encyclopaedic work about Madeira.
There might be one or more articles in the text enclosed by <body>. You would need to split the text into individual articles.  Infer boundaries of each article based on their content.
Each article starts with a title (short sentence, often with some clarification in parentheses), followed by a period (.) and then the article body itself, that can be one or more paragraphs. In most cases, articles are follow each other in alphabetical order.

Each object should have the following keys:
"""

html_article_prompt_intro_pt = """Segue-se um texto contendo um ou mais artigos do Elucidário Madeirense, uma obra enciclopédica sobre a Madeira. 
Pode haver um ou mais artigos no texto, delimitados por <body>. Deves repartir o texto em artigos separados, inferindo os limites de cada um pelo conteúdo. 
Cada artigo começa com um título (frase curta, às vezes com alguma explicação entre parênteses), seguido dum ponto final (.) e depois vem o corpo do artigo, que pode ter um ou mais parágrafos. 
Na maioria das vezes, os artigos surgem em sequência alfabética.

Cada objeto deve conter as seguintes chaves:"""




if LANG == "en":
    split_article_prompt_into = html_article_prompt_intro_en
else:
    split_article_prompt_into = html_article_prompt_intro_pt

if LANG == "en":
    CATEGORIES_TEXT = CATEGORIES_TEXT_EN
else:
    CATEGORIES_TEXT = CATEGORIES_TEXT_PT

categories_schema = content.Schema(
    type=content.Type.ARRAY,
    description=descriptions["categories"] + "\n" + CATEGORIES_TEXT,
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
            "Other"
        ],
    ),
)

structure_schema = content.Schema(
            type=content.Type.OBJECT,
            required=["name", "description", "is_reference", "references", "categories"],
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
                "references": content.Schema(
                    type=content.Type.ARRAY,
                    description=descriptions["references"],
                    items=content.Schema(
                        type=content.Type.STRING,
                        description=descriptions["reference"]
                    ),
                ),
                "is_reference": content.Schema(
                    type=content.Type.BOOLEAN,
                    description=descriptions["is_reference"],
                ),
                "categories": categories_schema            
            }
)

add_structure = {
    "prompt": f"""${structure_article_prompt_intro_en}
        "name" - ${descriptions["name"]}
        "alternative_name" - ${descriptions["alternative_name"]}
        "description" - ${descriptions["description"]}
        "is_reference" - ${descriptions["is_reference"]}
        "references" - ${descriptions["references"]}
        "categories" = ${descriptions["categories"]}
        """,
    "schema": structure_schema
}


multi_article_detector_prompt_en = """Below is a text that contains most likely one, but sometimes AT MOST three articles from Elucidario Madeirense, an encyclopaedic work about Madeira.
Can you tell if this text contains one or more articles?
Articles are different only if they are discussing completely different topics not related to each other.
If text is discussing same topic but followed by special cases of the same topic (e.g. taking place in different date or location, it is still one article.
If there are more then one articles, those will start with a title (short sentence, often with some clarification in parentheses),
followed by a period (.) and then the article body itself, that can be one or more paragraphs.  But not all short sentences like this are beginnings of new articles. 
Articles follow each other mostly in alphabetical order. Articles cannot have the same name.
Most likely, it is a single article.
Provide information about the articles in structured format.
"""

multi_article_detector_prompt_pt = """Abaixo está um texto que contém um ou dois ou talvez até três artigos do Elucidário Madeirense, uma obra enciclopédica sobre a Madeira.
Pode dizer se este texto contém um ou mais artigos?
Se houver mais de um artigo, esses começarão com um título (uma frase curta, muitas vezes com alguma clarificação entre parênteses),
seguido de um ponto (.) e depois o corpo do artigo, que pode ser um ou mais parágrafos. Terão um tópico completamente diferente.
Os artigos geralmente seguem uns aos outros em ordem alfabética.
Forneça informações sobre os artigos em formato estruturado.
"""
multi_article_detector_prompt = multi_article_detector_prompt_en if LANG == "en" else multi_article_detector_prompt_pt

article_detector_descriptions_en = {
    'name': 'Name of the article',
    'begins_with': 'Exact first 30 characters of the article body, so I can find it in the original text',
    'ends_with': 'Exact last 30 characters of the article body, so I can find it in the original text',
    'reason': 'Short reasoning (up to 200 characters) in portuguese explaining your decision on number of articles',
    'articles': 'List of articles in the text, with some information on start end end to find them. Max 3 items',    
}

article_detector_descriptions_pt = {
    'name': 'Nome do artigo',
    'begins_with': 'Primeiros 30 caracteres exatos do corpo do artigo, para que eu possa encontrá-lo no texto original',
    'ends_with': 'Últimos 30 caracteres exatos do corpo do artigo, para que eu possa encontrá-lo no texto original',
    'reason': 'Caso haja mais de um artigo, a tua justificação em inglês do porquê acreditas que sim.',
    'articles': 'Lista de artigos no texto, juntamente com algumas informações para os encontrar',    
}

article_detector_descriptions = article_detector_descriptions_en if LANG == "en" else article_detector_descriptions_pt

multi_article_detector_list_schema = content.Schema(
    type=content.Type.ARRAY,
    description=article_detector_descriptions["articles"],
    items=content.Schema(
        type=content.Type.OBJECT,
        required=["name", "begins_with", "ends_with"],
        properties={
            "name": content.Schema(
                type=content.Type.STRING,
                description=article_detector_descriptions["name"],
            ),
            "begins_with": content.Schema(
                type=content.Type.STRING,
                description=article_detector_descriptions["begins_with"],
            ),
            "ends_with": content.Schema(
                type=content.Type.STRING,
                description=article_detector_descriptions["ends_with"],
            ),
            # DO NOT GET MORE STUFF, IT WILL BECOME WILD
            # "is_reference": content.Schema( 
            #     type=content.Type.BOOLEAN,
            #     description=descriptions["is_reference"],
            # ),
            # "reference_name": content.Schema(
            #     type=content.Type.STRING,
            #     description=descriptions["reference_name"],
            # ),
            # "categories": categories_schema   
        },
    ),
)

multi_article_detector_schema = content.Schema(
    type=content.Type.OBJECT,
    required=["articles", "reason"],
    properties= {
        "reason": content.Schema(
            type=content.Type.STRING,
            description=article_detector_descriptions["reason"],
        ),
        "articles": multi_article_detector_list_schema
    }
)


detect_articles = {
    "prompt": f"""${multi_article_detector_prompt}""",
    "schema": multi_article_detector_schema
}


split_article_prompt = """Below is a text that contains one article from Elucidario Madeirense, an encyclopaedic work about Madeira from 1930-ies.
Split this article into thematic subchapters, each subchapter should:
- be at least 1500 characters long (300 words minimum)
- have it's own subtitle that follows the style in which the article is written in
Come up with the most appropriate way to split the article, based on it's topic and content.
Return a list of objects, each containing the subtitle, first 30 characters of the subchapter, and last 30 characters of the subchapter.
"""

split_article_descriptions_en = {
    'subtitle': 'Title of the subchapter, in portuguese',
    'begins_with': 'Exact first 30 characters of the article body, so I can find it using pythons str.find() method',
    'ends_with': 'Exact last 30 characters of the article body, so I can find it using pythons str.find() method',
    'short_summary': 'Very shortened version of the subchapter, max 150 characters, all in portuguese',
    'category': f'Array of categories that could match this subarticle. Put down no more then three, ideally just one'
}

split_article_descriptions = split_article_descriptions_en if LANG == "en" else split_article_descriptions_en

# We do NOT define CategoryEnum here. Instead, we just use the already-defined `categories_schema` variable elsewhere.
# Leave everything else (especially prompt strings) exactly as it is.

# ---------------------- SubArticle / SplitArticleSchema ----------------------
SubArticle_schema = content.Schema(
    type=content.Type.OBJECT,
    required=["subtitle", "begins_with", "ends_with"],
    properties={
        "subtitle": content.Schema(
            type=content.Type.STRING,
            description=split_article_descriptions["subtitle"]
        ),
        "begins_with": content.Schema(
            type=content.Type.STRING,
            description=split_article_descriptions["begins_with"]
        ),
        "ends_with": content.Schema(
            type=content.Type.STRING,
            description=split_article_descriptions["ends_with"]
        ),
        "short_summary": content.Schema(
            type=content.Type.STRING,
            description=split_article_descriptions["short_summary"]
        ),
        # The following are commented out in the original code snippet
        # "full_text": content.Schema(
        #     type=content.Type.STRING,
        #     description="Full content of the subarticle, should be exact quote of the original text"
        # ),
        # "categories": categories_schema,
        # "is_reference": content.Schema(
        #     type=content.Type.BOOLEAN,
        #     description="True if this article is a reference to another article. Reference articles are very short and contain only reference text."
        # ),
        # "reference_name": content.Schema(
        #     type=content.Type.STRING,
        #     description="The name of the referenced article if this article is a reference."
        # ),
    },
)

SplitArticleSchema_schema = content.Schema(
    type=content.Type.OBJECT,
    required=["subparts"],
    properties={
        "subparts": content.Schema(
            type=content.Type.ARRAY,
            description="A list of article segments, each defined by its attributes.",
            items=SubArticle_schema
        )
    }
)

split_article = {
    "prompt": split_article_prompt,
    "schema": SplitArticleSchema_schema
}

context_clarification = """Should be Short (up to 200 characters) self-sufficent explanation in portuguese, so that someone who is not familiar with the article can fully understand without reading the whole article. Should be mentioned directly. Ideally, mention date, location and people involved in the event."""

# =========================== 1) GEOGRAPHICAL LOCATIONS ===========================
list_locations_prompt = f"""Below is a text from Elucidario Madeirense, an encyclopaedic work about Madeira from 1930-ies.
Give me a list of geographical locations (proper nouns only) mentioned in this article. 
If the extracted location is part of a broader area mentioned (e.g., a region, county, or administrative division), do not list the broader area separately unless it is the only location specified.
Each extracted location should be unique and specific, avoiding redundancy by omitting overlapping or encompassing areas unless explicitly mentioned without a more specific location.
For example, If the text says "Rabaçal, located in the municipality of Calheta," extract Rabaçal as Location with Calheta as municipality and do not make a separate entry for Calheta only.
Ignore madeiran locations for which it is not possible to determine the frequesia.
Omit a location if not enough specific information is provided about it in the article to create an informative context.
If the event related to this location also has a date and or people involved, include those in the context as well.
All names should be in portuguese.
Return a list of dicts, each dict containing the following:

"location" - name of the geographical location. Proper noun only.
"continent" - continent of the location.
"country" - country of the location.
"municipality" - municipality of the location, madeira locations only
"frequesia" - frequesia, in which this location is located, madeira locations only
"place" - place name or area as specific as possible (proper noun), in which this location can be found
"type" - type of location (continent, country, island, city, area, frequesia, other place name)
"context" - what happened in this location in the context this article. {context_clarification}
"is_madeira" - true, if the location is in madeira
"is_significant" - true, if this location plays a significant role in this article, otherwise false. Only one location can be marked as significant.
"""

infer_location_clarification = "If not mentioned, but you can infer it from the context based on your knowledge, put it down."

LocationItem_schema = content.Schema(
    type=content.Type.OBJECT,
    required=["location", "type", "is_madeira", "is_significant"],
    properties={
        "location": content.Schema(
            type=content.Type.STRING,
            description="Name of the geographical location in portuguese. Modern name, if possible."
        ),
        "continent": content.Schema(
            type=content.Type.STRING,
            description=f"Continent. {infer_location_clarification}"
        ),
        "country": content.Schema(
            type=content.Type.STRING,
            description=f"Country. {infer_location_clarification}"
        ),
        "frequesia": content.Schema(
            type=content.Type.STRING,
            description=f"Frequesia (Madeira only). {infer_location_clarification}",
            enum=[    
                # Calheta
                "Arco da Calheta", "Calheta", "Estreito da Calheta", "Fajã da Ovelha",
                "Jardim do Mar", "Paúl do Mar", "Prazeres",

                # Câmara de Lobos
                "Câmara de Lobos", "Curral das Freiras", "Estreito de Câmara de Lobos",
                "Jardim da Serra", "Quinta Grande",

                # Funchal
                "Imaculado Coração de Maria", "Monte", "Santa Luzia", "Santa Maria Maior",
                "Santo António", "São Gonçalo", "São Martinho", "São Pedro", "Sé", "Nossa Senhora do Calhau",

                # Machico
                "Água de Pena", "Caniçal", "Machico", "Porto da Cruz", "Santo António da Serra (Machico/Santa Cruz)",

                # Ponta do Sol
                "Canhas", "Madalena do Mar", "Ponta do Sol",

                # Porto Moniz
                "Achadas da Cruz", "Porto Moniz", "Ribeira da Janela", "Seixal",

                # Ribeira Brava
                "Campanário", "Ribeira Brava", "Serra de Água", "Tabua",

                # Santa Cruz
                "Caniço", "Camacha", "Gaula", "Santa Cruz", "Santo António da Serra (Machico/Santa Cruz)",

                # Santana
                "Arco de São Jorge", "Faial", "Ilha", "Santana", "São Jorge",

                # São Vicente
                "Boaventura", "Ponta Delgada", "São Vicente"
                
                # Porto Santo
                "Porto Santo"
            ]
        ),
        "municipality": content.Schema(
            type=content.Type.STRING,
            description=f"Municipality. {infer_location_clarification}",
            enum = [
                "Calheta", "Câmara de Lobos", "Funchal", "Machico", "Ponta do Sol", "Porto Moniz", "Ribeira Brava",
                "Santa Cruz", "Santana", "São Vicente", "Porto Santo"
            ]
        ),
        "place": content.Schema(
            type=content.Type.STRING,
            description=f"Specific place name. {infer_location_clarification}"
        ),
        "type": content.Schema(
            type=content.Type.STRING,
            enum=[
                "continent",
                "country",
                "island",
                "city",
                "area",
                "municipality",
                "frequesia",
                "other place name"
            ],
            description="Type of the location"
        ),
        "context": content.Schema(
            type=content.Type.STRING,
            description=f"What happened in this location in the context of this article. {context_clarification}"
        ),
        "is_madeira": content.Schema(
            type=content.Type.BOOLEAN,
            description="true, if the location is in Madeira"
        ),
        "is_significant": content.Schema(
            type=content.Type.BOOLEAN,
            description="Whether the location is significant in the article. Only one location can be marked as significant."
        ),
    },
)

LocationListSchema_schema = content.Schema(
    type=content.Type.OBJECT,
    required=["items"],
    properties={
        "items": content.Schema(
            type=content.Type.ARRAY,
            description="List of all geographical locations mentioned. Proper nouns only.",
            items=LocationItem_schema
        )
    }
)

list_locations = {
    "prompt": list_locations_prompt,
    "schema": LocationListSchema_schema
}

# =========================== 2) PEOPLE MENTIONED ===========================
list_people_prompt = f"""Below is a text from Elucidario Madeirense, an encyclopaedic work about Madeira from 1930-ies.
Give me a list of people mentioned in this article.
Each extracted person should be unique and specific. It also should explain who that person was.
Only include max 15 most important personas.
Omit a person if not enough specific information is provided about it in the article to create an informative context.
Return list of dicts each dict containing the following:

"name" - name of the person
"title" - if person has a title (e.g. dr, ), put it down here
"context" - context in which this person is mentioned in this article. {context_clarification}
"is_significant" - true, if this person plays a significant role in this article, otherwise false. Only one person can be marked as significant.
"""

PersonItem_schema = content.Schema(
    type=content.Type.OBJECT,
    required=["name", "is_significant", "context"],
    properties={
        "name": content.Schema(
            type=content.Type.STRING,
            description="Person's name"
        ),
        "title": content.Schema(
            type=content.Type.STRING,
            description="Person's title (e.g. Dr, Prof, etc.)"
        ),
        "context": content.Schema(
            type=content.Type.STRING,
            description=f"""Context in which this person is mentioned in this article. 
                Should follow this pattern: <who they are>, <what happened with them or what they did, based on the article>, <other information mentioned about them>.
                {context_clarification}"""
        ),
        "is_significant": content.Schema(
            type=content.Type.BOOLEAN,
            description="Whether this person is significant in the article. Only one person can be marked as significant."
        ),
    },
)

PeopleListSchema_schema = content.Schema(
    type=content.Type.OBJECT,
    required=["items"],
    properties={
        "items": content.Schema(
            type=content.Type.ARRAY,
            description="List of people mentioned. Proper nouns only.",
            items=PersonItem_schema
        )
    }
)

list_people = {
    "prompt": list_people_prompt,
    "schema": PeopleListSchema_schema
}

# =========================== 3) DATES OR DATE RANGES ===========================
list_dates_prompt = f"""Below is a text from Elucidario Madeirense, an encyclopaedic work about Madeira from 1930-ies.
Give me a list of dates or date ranges mentioned in this article. Ignore dates for which year cannot be deducted.
Each extracted date should be unique and specific to this article.
Only include max 20 most important dates.
Omit a date if not enough specific information is provided about it in the article to create an informative context.
If the event that has a date also has a location, include the location in the context as well.
Do not include dates where year is not known.
Return list of dicts each dict containing the following:

"is_range" - true, if this is a date range
"year" - year of this date (or beginning of the date range)
"month" - month of this date or beginning of the date range (1-12). Leave empty if not specified.
"day" - day of this date or beginning of the date range (1-31). Leave empty if not specified.
if this is a date range 
"year_to" - end year of this date range. Only include if this is a date range.
"month_to" - end month of this date range (1-12). Leave empty if not specified.
"day_to" - end day of this date range (1-31). Leave empty if not specified.
"context" - summary of what happened on this date in the context of the article. {context_clarification}
"is_significant" - true, if this date or date range plays a significant role in this article. Only one date can be marked as significant.
"""

DateItem_schema = content.Schema(
    type=content.Type.OBJECT,
    required=["is_range", "is_significant", "context", "year"],
    properties={
        "is_range": content.Schema(
            type=content.Type.BOOLEAN,
            description="True if this is a date range"
        ),
        "year": content.Schema(
            type=content.Type.INTEGER,
            description="Year of the date or start of the range"
        ),
        "month": content.Schema(
            type=content.Type.INTEGER,
            description="Month of the date or start of the range"
        ),
        "day": content.Schema(
            type=content.Type.INTEGER,
            description="Day of the date or start of the range"
        ),
        "year_to": content.Schema(
            type=content.Type.INTEGER,
            description="End year if this is a range"
        ),
        "month_to": content.Schema(
            type=content.Type.INTEGER,
            description="End month if this is a range"
        ),
        "day_to": content.Schema(
            type=content.Type.INTEGER,
            description="End day if this is a range"
        ),
        "context": content.Schema(
            type=content.Type.STRING,
            description=f"what happened on this date in the context of the article. {context_clarification}"
        ),
        "is_significant": content.Schema(
            type=content.Type.BOOLEAN,
            description="Whether this date or range is significant"
        ),
    },
)

DateListSchema_schema = content.Schema(
    type=content.Type.OBJECT,
    required=["items"],
    properties={
        "items": content.Schema(
            type=content.Type.ARRAY,
            description="List of dates or date ranges mentioned",
            items=DateItem_schema
        )
    }
)

list_dates = {
    "prompt": list_dates_prompt,
    "schema": DateListSchema_schema
}


schmea_for_translation = {
    "list_locations": list_locations,
    "list_people": list_people,
    "list_dates": list_dates,
    "split_article": split_article,
    "detect_articles": detect_articles,
    "add_structure": add_structure
}