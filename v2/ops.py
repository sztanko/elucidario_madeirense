import re
import json
import sys
import time
import yaml

multispace_regex = re.compile(r"([^\s\n])( {2,})([^\s\n])")
new_page_regex = re.compile(r"\n\n\d{1,4}\n\n")
page_num_regex = re.compile(r"\n\d+\n\n\n\n")
new_letter_regex = re.compile(r"\n\n[A-Z]\n\n")
headers = [
    re.compile(r".*ELUCID.*MADEIR.*VOLUME.*"),
    #r" ELUCIDÁRIO MADEIRENSE - VOLUME II",
    #r" ELUCIDÁRIO MADEIRENSE – VOLUME II",
    #r" ELUCIDÁRIO MADEIRENSE - VOLUME I",
    #r" ELUCIDÁRIO MADEIRENSE - VOLUME I",
    #r"                                                                                                                               Vol. III",
    #r"                                                                                                                                                   ≡ Elucidário Madeirense (O-Z)",
]


def replace_spaces(t):
    return multispace_regex.sub(r"\1 \3", t)


def remove_new_pages(t):
    return new_page_regex.sub("\n", t)


def remove_page_numbers(t):
    return page_num_regex.sub("\n", t)


def remove_new_letters(t):
    return new_letter_regex.sub("\n", t)


def remove_headers(t):
    for header_regex in headers:
        t = header_regex.sub("\n", t)
        # t = t.replace(header, "")
    return t


def find_in_text_igonoring_new_lines(text, pattern):
    # find the index of the pattern in the text, ignoring new lines in both
    # the text and the pattern

    # take the first word of the pattern
    first_word = pattern.split()[0]


def split_into_chunks(text, approx_chunk_size):
    """
    Splits the text into chunks of approximately the specified size,
    ensuring splits occur at double newlines and each new chunk overlaps
    by 10% of the previous chunk.

    Parameters:
    text (str): The input text to split.
    approx_chunk_size (int): The approximate size of each chunk.

    Returns:
    list: A list of chunks.
    """
    if len(text) <= approx_chunk_size:
        return [text]

    chunks = []
    start = 0
    overlap_size = int(approx_chunk_size * 0.1)

    while start < len(text):
        end = start + approx_chunk_size
        if end >= len(text):
            chunks.append(text[start:])
            break

        # Find the nearest double newline before the end
        double_newline_pos = text.rfind("\n\n", start, end)
        if double_newline_pos == -1:
            # If no double newline found, find any newline
            double_newline_pos = text.rfind("\n", start, end)

        if double_newline_pos == -1:
            # If still no newline, force split at approx_chunk_size
            double_newline_pos = end

        chunk = text[start:double_newline_pos]
        chunks.append(chunk)

        # Update the start to ensure overlap
        start = double_newline_pos - overlap_size

    return chunks


def get_next_chunk(text, start, approx_chunk_size):
    end = start + approx_chunk_size
    if end >= len(text):
        return text[start:]
    double_newline_pos = text.rfind("\n\n", start, end)
    if double_newline_pos == -1:
        double_newline_pos = text.rfind("\n", start, end)
    if double_newline_pos == -1:
        double_newline_pos = end
    return text[start:double_newline_pos]


def remove_ocr_errors(article_str):
    fixes = {
        "Madakna": "Magdalena",
        "n1s": "nºs",
        "Ant6nio": "António",
        "ilh6u": "ilhéu",
        "Ju1ho": "Julho",
        "del1e": "dele",
        "ing1ês": "inglês",
        "Gonça1ves": "Gonçalves",
        "MadaZe7ia": "Madalena",
        "dó1ar": "dólar",
        "Hist6rico": "Histórico",
        "Hist6ria": "História",
        "col6nia": "colónia",
        "tamb6m": "também",
        "Cust6dio": "Custódio",
        "Vlt6ria": "Vitória",
        "Al1guns": "Alguns",
        "a1çapremas": "alçapremas",
        "Si1va": "Silva",
    }
    for fix in fixes:
        if fix in article_str:
            article_str = article_str.replace(fix, fixes[fix])
    return article_str


def preprocess_text(text):
    text = remove_headers(text)
    text = replace_spaces(text)
    text = replace_spaces(text)
    text = remove_new_pages(text)
    text = remove_page_numbers(text)
    text = remove_new_letters(text)
    text = remove_ocr_errors(text)
    return text


def get_article_chunks(text, approx_chunk_size):
    text = preprocess_text(text)
    chunks = split_into_chunks(text, approx_chunk_size)
    sys.stderr.write(f"Number of chunks: {len(chunks)}\n")
    return chunks


def dump_yaml(data):

    # Custom presenter for all strings to use the literal style "|"
    def literal_presenter(dumper, data):
        if "\n" in data:
            return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
        return dumper.represent_scalar("tag:yaml.org,2002:str", data)

    # Create a custom Dumper class
    class LiteralDumper(yaml.Dumper):
        pass

    # Register the presenter with the custom Dumper
    LiteralDumper.add_representer(str, literal_presenter)

    # Ensure Unicode characters are not escaped
    LiteralDumper.ignore_aliases = lambda *args: True

    # Dump YAML with the custom Dumper
    return yaml.dump(data, Dumper=LiteralDumper, default_flow_style=False, allow_unicode=True, sort_keys=False)


def get_structure(text):
    from prompts import split_articles
    from llms import gemini

    out = gemini.run_llm(split_articles, text)
    try:
        content = json.loads(out.text)
        for i in range(len(content)):
            c = content[i]
            next_prefix = content[i + 1]["begins_with"] if i + 1 < len(content) else ""
            c["content"] = extract_article_content(text, c, next_prefix)
            c["length"] = len(c["content"]) # add length of content
        return content
    except json.JSONDecodeError as e:
        # print(out.text)
        sys.stderr.write("Error decoding JSON\n")
        # print trace to stderr
        sys.stderr.write(f"Error: {e}\n")
        return None


def extract_article_content(text, structure, next_prefix):
    text_with_no_new_lines = text.replace("\n", " ")
    start = structure["begins_with"]
    end = structure["ends_with"]
    start_pos = text_with_no_new_lines.find(start)
    remaining_text = text[start_pos:]
    remaining_text_no_new_lines = remaining_text.replace("\n", " ")
    end_pos = remaining_text_no_new_lines.find(end)
    if end_pos == -1:
        if next_prefix:
            end_pos = remaining_text_no_new_lines.find(next_prefix)
        else:
            end_pos = len(remaining_text)
    else:
        end_pos += len(end)
    content = remaining_text[0:end_pos]
    return str(content)


def test_structure(original_text, structure):
    text_with_no_new_lines = original_text.replace("\n", " ")
    errors = []
    start = structure["begins_with"]
    end = structure["ends_with"]
    start_pos = text_with_no_new_lines.find(start)
    if start_pos == -1:
        errors.append(f"Start not found: {start}")
    remaining_text = text_with_no_new_lines[start_pos:]
    end_pos = remaining_text.find(end)
    if end_pos == -1:
        errors.append(f"End not found: {end}")
    if errors:
        return errors
    end_pos += len(end)
    content = remaining_text[0:end_pos]
    name = structure["name"]
    if name not in content:
        errors.append(f"Name not found: {name}")
    size = structure["length"]
    if len(content) == 0:
        errors.append(f"Size is 0")
        return errors
    length_error = round(100 * abs(len(content) - size) / len(content), 0)
    if length_error > 200:
        errors.append(f"Size mismatch: {len(content)} != {size}, error: {length_error}")
    return errors


def test_structure_all(original_text, structure):
    errors = {}
    for s in structure:
        name = s["name"]
        res = test_structure(original_text, s)
        if res:
            errors[name] = res
    return errors


def structure_all(text, original_chunk_size):
    approx_chunk_size = original_chunk_size
    previous_last_article_name = ""
    chunk_no = 1
    retry_count = 0
    while True:
        sys.stderr.write(f"Processing chunk {chunk_no}\n")
        chunk = get_next_chunk(text, 0, approx_chunk_size)
        sys.stderr.write(f"Chunk size: {len(chunk)}\n")
        if not chunk:
            break
        t0 = time.time()
        structure = get_structure(chunk)
        t1 = time.time()
        sys.stderr.write(f"Time taken to process this chunk: {round(t1 - t0, 2)} seconds\n")
        if not structure:
            sys.stderr.write(f"Error processing chunk {chunk_no}...\n")
            approx_chunk_size = int(approx_chunk_size * 0.9)
            continue
        sys.stderr.write(f"Number of articles in this chunk: {len(structure)}\n")
        last_article = structure[-1]
        try:
            last_article_name = last_article["name"]
            sys.stderr.write(f"Last article: {last_article_name}\n")
            if last_article_name == previous_last_article_name:
                if len(chunk)>= len(text)*0.9:
                    sys.stderr.write(f"Last article reached: {last_article_name}\n")
                    break                
                if len(structure) == 1:
                    sys.stderr.write("It looks like the article is quite large, let's increase the chunk size\n")
                    approx_chunk_size += 20000
                    continue
                
            text_stripped = text.replace("\n", " ")
            last_article_start = text_stripped.find(last_article["begins_with"])
            sys.stderr.write(f"Last article start: {last_article_start} out of {len(text_stripped)}\n")
            if last_article_start == -1:
                sys.stderr.write(f"Last article start not found, using a fallback...\n")
                last_article_start = len(chunk) - max(300, 30 + len(structure["content"]))
            text = text[last_article_start:]
            structure[0]["is_first_in_batch"] = True
            structure[-1]["is_last_in_batch"] = True
            yield structure
            retry_count = 0
            approx_chunk_size = original_chunk_size
            # structures.append(structure)
            previous_last_article_name = last_article_name
            chunk_no += 1
        except Exception as e:
            print(structure)
            sys.stderr.write(f"Error: {e}\n")
            sys.stderr.write(f"Last article: {last_article}\n")
            retry_count += 1
            sys.stderr.write(f"Retry count: {retry_count}\n")
            if retry_count > 5:
                sys.stderr.write(f"Too many retries, exiting...\n")
                break
            approx_chunk_size = int(approx_chunk_size * 0.7)
            sys.stderr.write(f"Retrying with a smaller chunk size of {approx_chunk_size}...\n")


def run():
    import sys
    import argparse
    import yaml

    parser = argparse.ArgumentParser(description="Process text")
    parser.add_argument(
        "action", help="Action to perform", choices=["preprocess", "chunks", "structure", "test", "structure-all"]
    )
    parser.add_argument("--chunk-size", help="Approximate size of each chunk", type=int, default=5000)
    args = parser.parse_args()

    if args.action == "preprocess":
        text = sys.stdin.read()
        print(preprocess_text(text))
    elif args.action == "chunks":
        text = sys.stdin.read()
        chunks = get_article_chunks(text, args.chunk_size)
        sys.stderr.write(f"Number of chunks: {len(chunks)}\n")
        print(dump_yaml(chunks))
    elif args.action == "structure":
        chunk_no = 15
        text = sys.stdin.read()
        text = preprocess_text(text)
        if "VOLUME" in text:
            raise Exception("Text contains VOLUME")
        chunks = get_article_chunks(text, args.chunk_size)
        structure = get_structure(chunks[chunk_no])
        sys.stderr.write(f"Number of articles: {len(structure)}\n")
        print(dump_yaml(structure))
        with open("chunks.yaml", "w") as f:
            f.write(dump_yaml(chunks))
        with open("chunk.txt", "w") as f:
            f.write(chunks[chunk_no])
        errors = test_structure_all(chunks[chunk_no], structure)
        if errors:
            # priunt error one by one to stderr
            for e in errors:
                sys.stderr.write(f"Error in article {e}: {errors[e]}\n")
        else:
            sys.stderr.write("All tests passed\n")
    elif args.action == "structure-all":
        text = sys.stdin.read()
        text = preprocess_text(text)
        if "VOLUME" in text:
            raise Exception("Text contains VOLUME")
        structures = []
        for structure in structure_all(text, args.chunk_size):
            structures += structure
            with open("structure.yaml", "w") as f:
                f.write(dump_yaml(structures))
    elif args.action == "test":
        sys.stderr.write("Testing...\n")
        sys.stderr.write("Reading chunks...\n")
        with open("chunks.yaml") as f:
            chunks = yaml.safe_load(f)
        sys.stderr.write("Reading structure...\n")
        with open("structure.yaml") as f:
            structure = yaml.safe_load(f)
        sys.stderr.write("Testing structure...\n")
        errors = test_structure_all(chunks[0], structure)
        sys.stderr.write("Writing errors...\n")
        with open("chunk.txt", "w") as f:
            f.write(chunks[0])
        with open("errors.yaml", "w") as f:
            f.write(dump_yaml(errors))


def test_replace_spaces():
    t = """Aulas  secundarias.  Antes  da  criação  do  liceu  do  Funchal  funcionavam  nesta  cidade  as  aulas
seguintes: de matemática, de filosofia, de retórica, de francês e inglês, de gramática latina e de latinidade. O
professor de matemática tinha em 1821 de ordenado anual 500:000 reis; o de filosofia 460:000 reis; o de
retórica 440:000 reis; o de gramática latina 400:000 réis; e o de latinidade 400:000 reis. O substituto da
primeira  destas  cadeiras  tinha  250:000  reis  de  ordenado;  o  da  segunda,  230:000  reis;  e  os  da  terceira  e"""
    t = replace_spaces(t)
    t = replace_spaces(t)
    print(t)


if __name__ == "__main__":
    run()
    # test_replace_spaces()