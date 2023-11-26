

## Software used:

- PDFMiner https://pypi.org/project/pdfminer/


## Documented discrepancies

### Some artcile titles are hidden

Some artcile titles get not noticed and are in the body of the previous articles

Example:
```
</span><span>Bancos. Têm agencias na Madeira as seguintes instituições de 
```

### Some articles have subchapters

Example: Levadas have many other subtitles, and they are also marked as <b> and they are indistuinguishable from the main headers.

### Some articles have bold text

Example: Origem da Ilha da Madeira., 

```
Pelo «argumento», que a seguir transcrevemos, se pode ajuizar do merecimento da obr<b>a:</b>
```

### Titles have parts in parenthesis, not in the <b> section

They are in italic. But the parenthesis themselves are not italic neither bold.



# HTML Cleaning Script Documentation

## Overview
This Python script is designed to clean and reformat HTML content, specifically targeting elements like divs, spans, and style attributes. It uses BeautifulSoup for HTML parsing and manipulation.

## Functions

### `is_empty(element)`
- **Purpose**: Checks if an HTML element is empty or contains only whitespace.
- **Parameters**: `element` - The HTML element to check.
- **Returns**: `True` if the element is empty or contains only whitespace; `False` otherwise.

### `remove_headers(soup)`
- **Purpose**: Removes specific header elements and page numbers from the HTML.
- **Parameters**: `soup` - A BeautifulSoup object representing the HTML content.
- **Returns**: The modified BeautifulSoup object.

### `replace_br_with_newline(soup)`
- **Purpose**: Replaces `<br>` tags with newline characters.
- **Parameters**: `soup` - A BeautifulSoup object.
- **Returns**: Modified BeautifulSoup object.

### `compact(soup)`
- **Purpose**: Compacts the HTML by removing unnecessary divs and adjusting styles for bold and italic text.
- **Parameters**: `soup` - A BeautifulSoup object.
- **Returns**: Modified BeautifulSoup object.

### `adjust_i_tags(soup)`
- **Purpose**: Adjusts `<i>` tags, specifically handling cases with parentheses.
- **Parameters**: `soup` - A BeautifulSoup object.
- **Returns**: Modified BeautifulSoup object.

### `remove_newlines_around_tags(html_content, tag_name, put_newline_before, put_newline_after)`
- **Purpose**: Removes or adds newlines around specified tags.
- **Parameters**: 
  - `html_content`: The HTML content as a string.
  - `tag_name`: The name of the tag to process.
  - `put_newline_before`: Boolean to determine if a newline should be added before the tag.
  - `put_newline_after`: Boolean to determine if a newline should be added after the tag.
- **Returns**: The modified HTML content as a string.

### `remove_space(html_content)`
- **Purpose**: Removes extra spaces from the HTML content.
- **Parameters**: `html_content` - The HTML content as a string.
- **Returns**: The modified HTML content as a string.

### `remove_all_styles(soup)`
- **Purpose**: Removes all style attributes from tags in the HTML.
- **Parameters**: `soup` - A BeautifulSoup object.
- **Returns**: Modified BeautifulSoup object.

### `clean_html(input_file, output_file)`
- **Purpose**: Orchestrates the cleaning process by calling the above functions and writes the cleaned HTML to a file.
- **Parameters**: 
  - `input_file`: Path to the input HTML file.
  - `output_file`: Path for the cleaned HTML output.
- **Operations**: Reads the HTML file, cleans it using the defined functions, and writes the cleaned HTML to the output file.

## Main Execution
- Checks command-line arguments for the input file.
- Sets the output file name based on the input file name.
- Calls `clean_html` with the input and output file paths.

## Usage
Run the script with the input HTML file as an argument:
```
python script.py <input_file.html>
```


## Transformations and Justifications
1. **Empty Element Removal**: Removes elements that don't contribute to the content.
2. **Header and Page Number Removal**: Cleans up the HTML by removing headers and pagination that are irrelevant to the main content.
3. **Style Adjustments**: Streamlines the appearance by handling bold and italic styles and removing extraneous styles.
4. **Whitespace Management**: Improves readability and consistency by managing spaces and newlines.
5. **Tag Specific Adjustments**: Ensures correct formatting of content, especially for italicized text involving parentheses.
