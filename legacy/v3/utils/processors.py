
def extract_text(text, prefix, suffix, next_prefix):
    # Replace newlines with spaces for searching
    text_with_no_new_lines = text.replace("\n", " ")

    start = prefix.replace("\n", " ")
    end = suffix.replace("\n", " ")

    # 1) Find the start position
    start_pos = text_with_no_new_lines.find(start)
    if start_pos == -1:
        sys.stderr.write(f"Start not found: {start}\nUsing the whole text as content\n")
        return str(text)

    # Slice from the start position (in the original text to preserve content)
    remaining_text = text[start_pos:]
    remaining_text_no_new_lines = remaining_text.replace("\n", " ")

    # 2) Try to find the next article prefix first
    end_pos = -1
    if next_prefix:
        sys.stderr.write(f"Trying to find next prefix: {next_prefix}\n")
        next_prefix_no_new_lines = next_prefix.replace("\n", " ")
        end_pos = remaining_text_no_new_lines.find(next_prefix_no_new_lines)
        if end_pos == -1:
            sys.stderr.write(f"Next prefix not found\n")

    # 3) If we couldn't find next_prefix or next_prefix wasn't given,
    #    then try the current article's `ends_with`
    if end_pos == -1:
        sys.stderr.write(f"Trying to find end: {end}\n")
        end_pos_temp = remaining_text_no_new_lines.find(end)
        if end_pos_temp == -1:
            sys.stderr.write(f"End not found: {end} (with start: {start})\n")
            sys.stderr.write(f"Using the whole text as content\n")
            end_pos = len(remaining_text)
        else:
            # If found, include the `end` marker in the content
            end_pos = end_pos_temp + len(end)

    content = remaining_text[:end_pos]
    return str(content)