from .step import Step
from google.ai.generativelanguage_v1beta.types import content

perfix_suffix_schema = content.Schema(
    type=content.Type.OBJECT,
    required = ["begins_with", "ends_with"],
    properties = {
    "begins_with": content.Schema(
                        type=content.Type.STRING,
                        description='Exact first 30 characters of the article body, so I can find it in the original text',
                    ),
    "ends_with": content.Schema(
                        type=content.Type.STRING,
                        description='Exact last 30 characters of the article body, so I can find it in the original text',
                    )
    }
)

workflow = [
    Step(
        name="extract_articles",
        descripion="Detect if this article is in reality more then one article",
        prompt="""
            Following is a text of one or more articles from Elucidario Madeirense, an encyclopaedic work about Madeira.
            There might be one or more articles in the text enclosed by <body>. 
            You would need to split the text into individual articles. 
            Infer boundaries of each article based on their content.
            Each article starts with a title (short sentence, 
            often with some clarification in parentheses), followed by a period (.) and then the article body itself, 
            that can be one or more paragraphs. 
            In most cases, articles are follow each other in alphabetical order.
            """,
        output_tags=["name"],
        output_schema=content.Schema(
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
                },
            ),
        ),
    )
]
