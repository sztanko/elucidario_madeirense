import json
from collections import defaultdict

def validate_response(response):
    for keys in ["title", "id", "references", "categories", "freguesias", "years", "locations", "people", "body"]:
        if keys not in response:
            print(f"Error: {keys} not in response")
            print(response)
            raise Exception(f"Error: {keys} not in response")
    if not isinstance(response["title"], str):
        print(f"Error: title = {response['title']} is not a string")
        print(response)
        raise Exception(f"Error: title = {response['title']} is not a string")
    if not isinstance(response["id"], int):
        print(f"Error: id = {response['id']} is not an integer")
        print(response)
        raise Exception(f"Error: id = {response['id']} is not an integer")


def union_dicts(chunks, field):
    array_of_dicts = [chunk.get(field) or {} for chunk in chunks]
    out = defaultdict(list)
    for chunk in array_of_dicts:
        for k, v in chunk.items():
            out[k].append(v)
    return dict([(k, "\n\n".join(out[k])) for k in out])


def get_json(response):
    # print(response)
    print(f"Response length: {len(response)}")
    try:
        data = json.loads(response)
        if "a" not in data:
            print("Error: 'a' not in data")
            print(response)
            raise Exception("Error: 'a' not in data")
        if not isinstance(data["a"], list):
            print("Error: 'a' is not a list")
            print(response)
            raise Exception("Error: 'a' is not a list")
    except json.decoder.JSONDecodeError as e:
        print("Error: JSONDecodeError")
        print(response)
        raise e
    for a in data["a"]:
        validate_response(a)
    return data["a"]


def unify_chunks(chunks):
    return {
        "title": chunks[0]["title"],
        "id": chunks[0]["id"],
        "references": list(set([ref for chunk in chunks for ref in chunk.get("references") or []])),
        "categories": list(set([cat for chunk in chunks for cat in chunk.get("categories") or []])),
        "freguesias": list(set([freg for chunk in chunks for freg in chunk.get("freguesias") or []])),
        "years": union_dicts(chunks, "years"),
        "locations": union_dicts(chunks, "locations"),
        "people": union_dicts(chunks, "people"),
        "body": "\n\n".join([chunk["body"] for chunk in chunks]),
    }


def group_articles(articles, threshold):
    groups = []
    current_group = []
    current_length = 0

    for article in articles:
        article_length = len(article)
        if article_length > threshold:
            # If the current group has articles, add it to groups
            if current_group:
                groups.append(current_group)
                current_group = []
                current_length = 0
            # Add the large article as its own group
            groups.append([article])
        else:
            if current_length + article_length > threshold:
                # Current group exceeds threshold, start a new group
                groups.append(current_group)
                current_group = [article]
                current_length = article_length
            else:
                # Add article to current group
                current_group.append(article)
                current_length += article_length

    # Add the last group if it's not empty
    if current_group:
        groups.append(current_group)

    return groups