from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

LANG = "en"

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