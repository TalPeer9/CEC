from bs4 import BeautifulSoup
import json
import pandas as pd
import re


def classify_content(content: str) -> str:
    """
    Classifies the content into text types based on predefined identifiers.

    Args:
        content (str): The content to classify.

    Returns:
        str: The classified text type.
    """

    clean_content = content.strip()

    notebook_parts_pattern = r"חלק\s+\d+\s*-\s*.+"
    question_title_identifiers = ["שאלה", "תרגיל"]
    notebook_parts_identifiers = ["חלק"]
    question_section_title_identifiers = ["סעיף"]
    stop_section_identifiers = ["סיום", "עצור"]
    image_pattern = r"!\[\w+\.png\]\(.*?\)"
    end_notebook = ["כל הכבוד! סיימתם"]
    to_drop = ["כתבו תשובה כאן", "כתוב תשובה"]
    if any(clean_content.startswith(identifier) for identifier in to_drop):
        return "drop"
    if any(clean_content.startswith(identifier) for identifier in question_title_identifiers):
        return "question_title"
    elif any(clean_content.startswith(identifier) for identifier in question_section_title_identifiers):
        return "section_title"
    elif re.match(notebook_parts_pattern, clean_content):
        return "notebook_parts"
    elif re.match(image_pattern, clean_content):
        return "image_load"
    elif any(clean_content.startswith(identifier) for identifier in notebook_parts_identifiers):
        return "notebook_parts"
    elif any(identifier in clean_content for identifier in to_drop):
        return "drop"
    else:
        return "question_text"


def clean_markdown_cell(raw_text):
    """
    Processes raw text from a Colab markdown cell and removes all design-related HTML/CSS,
    keeping only the plain text content.

    Args:
        raw_text (str): Raw markdown content from the cell.

    Returns:
        str: Cleaned text with only the presented content.
    """

    soup = BeautifulSoup(raw_text, 'html.parser')

    cleaned_text = soup.get_text(separator=' ').strip().replace('#', '').replace("כתוב תשובה כאן", "").replace("כתוב תשובה", "")
    return cleaned_text


def start_extraction(notebook_path, file_title="clean_"):
    notebook_type, class_week = file_title.rsplit('_', 1)
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook_data = json.load(f)

    rows_clean_text = []
    notebook_title = f'שבוע {class_week}'
    if notebook_type == 'class_assigment':
        notebook_type = 'תרגול כיתה'
    elif notebook_type == 'home_assigment':
        notebook_type = 'תרגול בית'
    notebook_header = f"{notebook_title} - {notebook_type}"
    rows_clean_text.append({
        'cell_id': 1,
        'cell_type': 'markdown',
        'cell_script': '',
        'markdown_type': 'notebook_header',
        'content': notebook_header
    })
    rows_clean_text.append({
        'cell_id': 2,
        'cell_type': 'markdown',
        'cell_script': '',
        'markdown_type': 'reminder_mark',
        'content': ''
    })
    for cell_id, cell in enumerate(notebook_data.get('cells', []), start=3):
        cell_type = cell.get('cell_type', '')
        if cell_type == 'code':
            cell_script = ''.join(cell.get('source', []))
            rows_clean_text.append({
                'cell_id': cell_id,
                'cell_type': 'code',
                'cell_script': cell_script.strip(),
                'markdown_type': '',
                'content': ''
            })
        elif cell_type == 'markdown':
            raw_content = ''.join(cell.get('source', []))
            clean_content = clean_markdown_cell(raw_content)
            rows_clean_text.append({
                'cell_id': cell_id,
                'cell_type': 'markdown',
                'cell_script': '',
                'markdown_type': classify_content(clean_content),
                'content': clean_content.strip()
            })

    df_clean_text = pd.DataFrame(rows_clean_text,
                                 columns=['cell_id', 'cell_type', 'cell_script', 'markdown_type', 'content'])

    output_clean_text_csv_path = f"extracted_cells/{file_title}_cells.csv"
    df_clean_text.to_csv(output_clean_text_csv_path, index=False, encoding='utf-8-sig')
