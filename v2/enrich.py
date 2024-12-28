import re
import json
import sys
from datetime import datetime
import yaml
from llms import gemini
from llms.utils import extract_article_content
from prompts import list_dates, list_locations, list_people, split_article as split_article_config

sample_articles = [
    "Tesoura (Forficula auricularia)",
    "Arco de São Jorge (Freguesia do)",
    "Abelha (Apis mellifica)",
    "Abastecimento de águas da cidade",
    "Datas da História da Madeira",
    "Levadas",
    "Atouguia",
    "Lombo do Atouguia",
    "Arco da Calheta (Freguesia do)",
    "Calheta (Freguesia de)",
    "Colombo (Cristovão)",
    "Cristovão Colombo na Madeira",
    "Bancos",
    "Bancos na Madeira",
    "Bang up",
    "Bordados",
    "Bordalo (Francisco Maria)",
    "Selvagens",
    "Varoes Ilustres",
    "Madeirenses que se distinguiram fora da ilha",
    "Sé Catedral do Funchal",
    "Sé Catedral"
    
]

ignore_enrichment_list = {
    "dates": ["Datas da História da Madeira"],
    "locations": ["Datas da História da Madeira", "Levadas"],
    "people": [] # "Datas da História da Madeira", "Varoes Ilustres", "Madeirenses que se distinguiram fora da ilha"]
}

def split_article(name, content):
    sys.stderr.write(f"Splitting article: {name}\n")
    text = f"""<article>
    <name>{name}</name>
    <content>{content}</content>
    </article>"""
    
    splits_response = gemini.run_llm(split_article_config, text)
    splits = json.loads(splits_response.text)["subparts"]
    for split in splits:
        yield split

def get_additional_info(title, subtitle, content):
    sys.stderr.write(f"Getting additional info for: {subtitle}\n")
    text = f"""<article>
    <title>{title}</title>
    <subtitle>{subtitle}</subtitle>
    <content>{content}</content>
    </article>"""
    
    enrichments = {
        "dates": list_dates,
        "locations": list_locations,
        "people": list_people
    }
    additional_info = {}
    
    for enrichment_type, p in enrichments.items():
        if title in ignore_enrichment_list[enrichment_type]:
            sys.stderr.write(f"Ignoring enrichment for {enrichment_type}: {title}\n")
            additional_info[enrichment_type] = []
            continue
        sys.stderr.write(f"{enrichment_type}\n")
        response = gemini.run_llm(p, text)
        try: 
            response_json = json.loads(response.text)
        except:
            sys.stderr.write(f"Error: {response.text}\n")
            response_json = {}
        additional_info[enrichment_type] = response_json.get("items", [])
        
    return additional_info

def load_articles(file_name):
    sys.stderr.write(f"Loading articles from: {file_name}\n")
    with open(file_name, 'r') as file:
        articles = yaml.load(file, Loader=yaml.FullLoader)
        sys.stderr.write(f"Loaded {len(articles)} articles\n")
        for article_chunks in articles:
            original_name = article_chunks["original_name"]
            for article in article_chunks["articles"]:
                yield article["name"], article["content"]



def enrich_articles(file_name):
    articles = load_articles(file_name)
    for name, content in articles:
        if False or name in sample_articles:
            article = {}
            article["name"] = name
            article["splits"] = []
            subpart_length = 0
            if len(content) < 2000:
                splits  = [
                    {
                        "full_text": content,
                        "word_count": len(content.split()),
                        "subtitle": name
                    }
                ]
            else:
                splits = list(split_article(name, content))
            sys.stderr.write(f"Article: {name} has {len(splits)} splits\n")
            for i in range(len(splits)):
                split = splits[i]
                subtitle = split['subtitle']
                if 'full_text' not in split:
                    next_starts_with = splits[i+1]['begins_with'] if i+1 < len(splits) else None
                    sub_content = extract_article_content(content, split['begins_with'], split['ends_with'], next_starts_with)
                    split['full_text'] = sub_content
                    split['word_count'] = len(sub_content.split())
                else:
                    sub_content = split['full_text']
                additional_info = get_additional_info(name, subtitle, sub_content)
                split['additional_info'] = additional_info
                subpart_length += len(split['full_text'])                
                article["splits"].append(split)            
            article["sum_length"] = subpart_length
            article["original_length"] = len(content)            
            yield article

def main(file_name: str, out_file_name):
    out = []
    for article in enrich_articles(file_name):
        out.append(article)
    with open(out_file_name, "w") as f:
        f.write(yaml.dump(out, Dumper=yaml.Dumper, default_flow_style=False, allow_unicode=True))
        sys.stderr.write(f"Written {len(out)} articles to {out_file_name}\n")
        # yaml.dump(out, Dumper=yaml.Dumper, default_flow_style=False, allow_unicode=True)
        
if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])