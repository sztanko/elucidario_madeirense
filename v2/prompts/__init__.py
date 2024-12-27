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
    "alternative_name": "based on the content, suggest the best possible name for this article in english, if different from the original. Should not include 'Madeira' in it, as the whole encyclopedia is about this island.",
    "description": 'short description of article in english, one sentence, max 20 words. When summarizing an article, avoid starting with "this article" and go straight to the core content.',
    "begins_with": "exact first 30 characters of the article, first line only, so I can find it in the original text. if first line is shorter than 30 characters, use the whole line.",
    "ends_with": "exact last 30 characters of the article, last line only, so I can find it in the original text. if last line is shorter than 30 characters, use the whole line.",
    "is_reference": "is this article just a reference to another article? It is very short, and only contains something like 'V. <referenced article name>' or 'Vid. <referenced article name>' or '(V. este nome)'",
    "reference_name": "if yes, specify the name of the referenced article",
    "categories": """Up to 3 categories describing the article""",
}

descriptions_pt = {
    "name": "nome do artigo",
    "alternative_name": "com base no conteúdo, sugira o melhor nome possível para este artigo em português, se diferente do original. Não deve incluir 'Madeira' nele, pois toda a enciclopédia é sobre esta ilha.",
    "description": "descrição curta do artigo em português, em uma frase, no máximo 20 palavras. Ao resumir um artigo, evite frases como 'este artigo' e vá direto ao conteúdo principal.",
    "begins_with": "primeiros 30 caracteres exatos do artigo, apenas na primeira linha, para que eu possa encontrá-lo no texto original. se a primeira linha for mais curta que 30 caracteres, use a linha inteira.",
    "ends_with": "últimos 30 caracteres exatos do artigo, apenas na última linha, para que eu possa encontrá-lo no texto original. se a última linha for mais curta que 30 caracteres, use a linha inteira.",
    "is_reference": "este artigo é apenas uma referência para outro artigo? É muito curto e contém somente algo como 'V. <nome do artigo referenciado>' ou 'Vid. <nome do artigo referenciado>' ou '(V. este nome)'",
    "reference_name": "se sim, especifique o nome do artigo referenciado",
    "categories": "Até 3 categorias que descrevam o artigo",
}

if LANG == "en":
    descriptions = descriptions_en
else:
    descriptions = descriptions_pt

split_article_prompt_intro_en = """Following is a text of one or more articles from Elucidario Madeirense, an encyclopaedic work about Madeira.
Typically each article starts in a new paragraph with a title (short sentence, often with some clarification in parentheses), followed by period (.) and then the article body itself, that can be one or more paragraphs. In most cases, articles are follow each other in alphabetical order.
Output a list of objects, each containing information about one article. Infer boundaries of each article based on it's context and subject. Lists of historical dates should be a single article.
Make sure each object contains information only about one article. There cannot be any overlap between articles.

Each object should have the following keys:"""

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


split_article_prompt_intro_pt = """Segue-se abaixo um texto que pode conter um ou mais artigos do Elucidário Madeirense, uma obra enciclopédica sobre a Madeira.
Normalmente, cada artigo começa num novo parágrafo com um título (frase curta, por vezes com algum esclarecimento entre parênteses), seguido de um ponto (.) e, em seguida, o corpo do artigo em si, que pode abranger um ou mais parágrafos. Na maior parte das vezes, os artigos surgem em ordem alfabética.

Gere uma lista de objetos, em que cada objeto contenha informações acerca de um único artigo. Deduza os limites de cada artigo tendo em conta o seu contexto e tema. Listas de datas históricas devem ser consideradas um único artigo.
Ignore o texto introdutório e considere somente os artigos. Assegure-se de que cada objeto inclua informação de apenas um artigo. Não pode haver qualquer sobreposição entre artigos.

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
        ],
    ),
)

structure_schema = content.Schema(
            type=content.Type.OBJECT,
            required=["name", "description", "begins_with", "ends_with", "is_reference", "categories"],
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
                    description=descriptions["reference_name"]
                ),
                
                "categories": categories_schema            
            }
)

split_articles = {
    "prompt": f"""${split_article_prompt_into}
        "name" - ${descriptions["name"]}
        "alternative_name" - ${descriptions["alternative_name"]}
        "description" - ${descriptions["description"]}
        "begins_with" - ${descriptions["begins_with"]}
        "ends_with" - ${descriptions["ends_with"]}
        "is_reference" - ${descriptions["is_reference"]}
        "reference_name" - ${descriptions["reference_name"]}
        "categories" = ${descriptions["categories"]}
        """,
    "schema": content.Schema(
        type=content.Type.ARRAY,
        items=structure_schema)
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
    'reason': 'Short reasoning (up to 200 characters) in english explaining your decision on number of articles',
    'articles': 'List of articles in the text, with some information on start end end to find them. Max 3 items',
    "categories": """Up to 3 categories matching the article""",
    "is_reference": "is this article just a reference to another article? It is very short, and only contains something like 'V. <referenced article name>' or 'Vid. <referenced article name>' or '(V. este nome)'",
    "reference_name": "if yes, specify the name of the referenced article",
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
Split this article into thematic subpaarts, each subchapter should:
- have it's own subtitle
- should be 200-300 words, if possible

Return a list of objects, each containing the subtitle, first 30 characters of the subchapter, and last 30 characters of the subchapter.
"""

split_article_descriptions_en = {
    'subtitle': 'Title of the subchapter, in english',
    'begins_with': 'Exact first 30 characters of the article body, so I can find it using pythons str.find() method',
    'ends_with': 'Exact last 30 characters of the article body, so I can find it using pythons str.find() method',
    'short_summary': 'Very shortened version of the subchapter, max 150 characters, all in english',
    'category': f'Array of categories that could match this subarticle. Put down no more then three, ideally just one'
}

split_article_descriptions = split_article_descriptions_en if LANG == "en" else split_article_descriptions_en

class CategoryEnum(str, Enum):
    History = "History"
    People = "People"
    Geography = "Geography"
    Plants = "Plants"
    Animals = "Animals"
    Politics = "Politics"
    Economy = "Economy"
    Farming = "Farming"
    Travel = "Travel"
    Religion = "Religion"
    Arts = "Arts"
    Education = "Education"
    Places = "Places"
    Maritime = "Maritime"
    Health = "Health"
    Military = "Military"
    Transport = "Transport"
    Cuisine = "Cuisine"
    Language = "Language"
    Legal = "Legal"

class SubArticle(BaseModel):
    subtitle: str = Field(
        ...,
        description=split_article_descriptions["subtitle"]
    )
    begins_with: str = Field(
        ...,  # Required field
        description=split_article_descriptions["begins_with"]
    )
    ends_with: str = Field(
        ...,  # Required field
        description=split_article_descriptions["ends_with"]
    )
    short_summary: Optional[str] = Field(
        None,
        description=split_article_descriptions["short_summary"]
    )
    # full_text: str = Field(
    #     ...,
    #     description="Full content of the subarticle, should be exact quote of the original text"
    # )
    # categories: List[CategoryEnum] = Field(
    #     ...,  # Required field
    #     description=split_article_descriptions["category"]
    # )
    # is_reference: bool = Field(
    #     ...,  # Required field
    #     description="True if this article is a reference to another article. Reference articles are very short and contain only reference text."
    # )
    # reference_name: Optional[str] = Field(
    #     None,
    #     description="The name of the referenced article if this article is a reference."
    # )
    
    class Config:
        use_enum_values = True 

class SplitArticleSchema(BaseModel):
    subparts: List[SubArticle] = Field(
        ...,  # Required field
        description="A list of article segments, each defined by its attributes."
    )


split_article = {
    "prompt": split_article_prompt,
    "schema": SplitArticleSchema
}

context_clarification = """Should be Short (up to 200 characters) self-sufficent explanation, so that someone who is not familiar with the article can fully understand without reading the whole article."""

# =========================== 1) GEOGRAPHICAL LOCATIONS ===========================
list_locations_prompt = f"""Below is a text from Elucidario Madeirense, an encyclopaedic work about Madeira from 1930-ies.
Give me a list of geographical locations mentioned in this article.
Return a list of dicts, each dict containing the following:

"location" - name of the geographical location
"continent" - continent of the location.
"country" - country of the location.
"region" - region of the location
"frequesia" - frequesia, in which this location is located
"place" - place name, in which this location can be found
"type" - type of location (continent, country, island, city, area, frequesia, other place name)
"context" - what happened in this location in the context this article. {context_clarification}
"is_madeira" - true, if the location is in madeira
"is_significant" - true, if this location plays a significant role in this article, otherwise false
"""

class LocationTypeEnum(str, Enum):
    continent = "continent"
    country = "country"
    island = "island"
    city = "city"
    area = "area"
    frequesia = "frequesia"
    other = "other place name"

class LocationItem(BaseModel):
    location: str = Field(..., description="Name of the geographical location")
    continent: Optional[str] = Field(None, description="Continent")
    country: Optional[str] = Field(None, description="Country")
    region: Optional[str] = Field(None, description="Region")
    frequesia: Optional[str] = Field(None, description="Frequesia (administrative division)")
    place: Optional[str] = Field(None, description="Specific place name")
    type: LocationTypeEnum = Field(..., description="Type of the location")
    context: Optional[str] = Field(None, description=f"what happened in this location in the context this article. {context_clarification}")
    is_madeira: bool = Field(..., description="true, if the location is in Madeira")
    is_significant: bool = Field(..., description="Whether the location is significant in the article")

class LocationListSchema(BaseModel):
    items: List[LocationItem] = Field(..., description="List of all geographical locations mentioned")

list_locations = {
    "prompt": list_locations_prompt,
    "schema": LocationListSchema
}


# =========================== 2) PEOPLE MENTIONED ===========================
list_people_prompt = f"""Below is a text from Elucidario Madeirense, an encyclopaedic work about Madeira from 1930-ies.
Give me a list of people mentioned in this article.
Return list of dicts each dict containing the following:

"name" - name of the person
"title" - if person has a title (e.g. dr, ), put it down here
"context" - context in which this person is mentioned in this article. {context_clarification}
"is_significant" - true, if this person plays a significant role in this article, otherwise false
"""

class PersonItem(BaseModel):
    name: str = Field(..., description="Person's name")
    title: Optional[str] = Field(None, description="Person's title (e.g. Dr, Prof, etc.)")
    context: Optional[str] = Field(None, description=f"context in which this person is mentioned in this article. {context_clarification}")
    is_significant: bool = Field(..., description="Whether this person is significant in the article")

class PeopleListSchema(BaseModel):
    items: List[PersonItem] = Field(..., description="List of people mentioned")

list_people = {
    "prompt": list_people_prompt,
    "schema": PeopleListSchema
}


# =========================== 3) DATES OR DATE RANGES ===========================
list_dates_prompt = f"""Below is a text from Elucidario Madeirense, an encyclopaedic work about Madeira from 1930-ies.
Give me a list of dates or date ranges mentioned in this article. Ignore dates for which year cannot be deducted.
Return list of dicts each dict containing the following:

"is_range" - true, if this is a date range
"year" - year of this date (or beginning of the date range)
"month" - month of this date or beginning of the date range (1-12). Leave empty if not specified.
"day" - day of this date or beginning of the date range (1-31). Leave empty if not specified.
if this is a date range 
"year_to" - end year of this date range
"month_to" - end month of this date range (1-12). Leave empty if not specified.
"day_to" - end day of this date range (1-31). Leave empty if not specified.
"context" - what happened on this date in the context of the article. {context_clarification}
"is_significant" - true, if this date or date range plays a significant role in this article.
"""

class DateItem(BaseModel):
    is_range: bool = Field(..., description="True if this is a date range")
    year: Optional[int] = Field(None, description="Year of the date or start of the range")
    month: Optional[int] = Field(None, description="Month of the date or start of the range")
    day: Optional[int] = Field(None, description="Day of the date or start of the range")
    year_to: Optional[int] = Field(None, description="End year if this is a range")
    month_to: Optional[int] = Field(None, description="End month if this is a range")
    day_to: Optional[int] = Field(None, description="End day if this is a range")
    context: Optional[str] = Field(None, description=f"what happened on this date in the context of the article. {context_clarification}")
    is_significant: bool = Field(..., description="Whether this date or range is significant")

class DateListSchema(BaseModel):
    items: List[DateItem] = Field(..., description="List of dates or date ranges mentioned")

list_dates = {
    "prompt": list_dates_prompt,
    "schema": DateListSchema
}
