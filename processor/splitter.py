from bs4 import BeautifulSoup
import json


def build_chunk(title, body_content):
    return f"<div class='article' id='a_{{id}}'><h1>{title}</h1><div class='article-body'>{body_content}</div></div>"


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
    print(f"Size threshold: {size_threshold}")
    print(f"Total elements: {len(soup.contents)}")

    for element in soup.contents:
        # Convert the element to string if it is a NavigableString
        str_element = str(element)
        # print(str_element)
        print(f"Current element size: {len(str_element)}")
        if len(current_chunk) + len(str_element) <= size_threshold:
            current_chunk += str_element
        else:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = str_element

    # Add the last chunk if it exists
    if current_chunk:
        chunks.append(current_chunk)

    print(f"Split {len(html)} chars into {len(chunks)} chunks")
    return chunks


def merge_small_chunks(chunks, size_threshold):
    """
    Merges small HTML chunks to maximize their size up to the specified size threshold,
    while keeping the chunks' order.

    :param chunks: List of HTML chunks as strings
    :param size_threshold: Maximum size of each merged chunk
    :return: List of strings, each representing a merged chunk of HTML
    """
    merged_chunks = []
    current_chunk = ""

    for chunk in chunks:
        if len(current_chunk) + len(chunk) <= size_threshold:
            current_chunk += chunk
            print(f"Current chunk size: {len(current_chunk)}")
        else:
            if current_chunk:
                merged_chunks.append(current_chunk)
            current_chunk = chunk

    # Add the last chunk if it exists
    if current_chunk:
        merged_chunks.append(current_chunk)
    print(f"Merged {len(chunks)} chunks into {len(merged_chunks)} chunks")
    for chunk in merged_chunks:
        print(f"Chunk size: {len(chunk)}")
    return merged_chunks


def split_article(html_string, size_threshold):
    if len(html_string) <= size_threshold:
        return [html_string]
    soup = BeautifulSoup(html_string, "html.parser")
    title = soup.find("h1").string
    body = soup.find("div", class_="article").find("div", class_="article_body")
    body_html = body.decode_contents()
    if "<h2>" in body_html:
        split_by_header = ["<h2>" + art for art in html_string.split("<h2>")]
        print(f"Split by headers: {len(split_by_header)}")
    else:
        split_by_header = [body_html]
        print("No headers found")

    chunks = []
    for pg in split_by_header:
        if len(pg) <= size_threshold:
            chunks.append(pg)
            print(f"Chunk size: {len(pg)} is smaller then {size_threshold}, so leaving it as it is ")
        else:
            print(f"Splitting {len(pg)} chars into chunks")
            chunks += split_html(pg, size_threshold)

    merged_chunks = merge_small_chunks(chunks, size_threshold)
    chunk_html = [build_chunk(title, chunk) for chunk in merged_chunks]
    print(f"Returning {len(chunk_html)} chunks")
    return chunk_html
