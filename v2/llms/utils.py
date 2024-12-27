import sys

def extract_article_content(text, begins_with, ends_with, next_start_with = None):
    text_with_no_new_lines = text.replace("\n", " ")
    start = begins_with.replace("\n", " ")
    end = ends_with.replace("\n", " ")
    start_pos = text_with_no_new_lines.find(start)
    remaining_text = text[start_pos:]
    remaining_text_no_new_lines = remaining_text.replace("\n", " ")
    end_pos = remaining_text_no_new_lines.find(end)
    if end_pos == -1:
        if next_start_with:
            sys.stderr.write(f"Trying to find next start: {next_start_with}\n")
            next_start_pos = remaining_text_no_new_lines.find(next_start_with.replace("\n", " "))
            if next_start_pos != -1:
                end_pos = next_start_pos            
            else:
                sys.stderr.write(f"Next start not found: {next_start_with}\n")
                sys.stderr.write(f"Using the whole text as content\n")
                end_pos = len(remaining_text)
        else:
            sys.stderr.write(f"End not found: {end} (with start: {start})\n")
            sys.stderr.write(f"Using the whole text as content\n")
            end_pos = len(remaining_text)
        
    else:
        end_pos += len(end)
    content = remaining_text[0:end_pos]
    return str(content)