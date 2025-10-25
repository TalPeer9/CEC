import nbformat as nbf
import inspect
import importlib.util

import notebook_processor
from notebook_processor import *


def extract_function_body(module_path, function_name):
    """
    Extracts the body of a function from a given Python module.
    """
    spec = importlib.util.spec_from_file_location("module", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    func = getattr(module, function_name)
    source_lines = inspect.getsourcelines(func)[0]
    return ''.join(line for line in source_lines[1:] if line.strip())


def generate_markdown_cell(text, text_type, path=None):
    styles = {
        "notebook_header": lambda text: f"""<div dir='rtl' align='center'><font color='#7E30E1' size='16'><b>{text}</b></font><br><br></div>""",
        "notebook_type": lambda text: f"""<div dir="rtl" align='center'><font color='#7E30E1' size='14'><b>{text}</b></font>""",
        "reminder_mark": f"""<div dir="rtl" align="center"><font color="Grey"><ul style="direction: rtl; text-align: right; list-style-position: inside;">
                <li>צרו עותק של המחברת</li>
                <li>שנו את שם העותק לשמכם הפרטי, ועבדו עם עותק זה</li>
                </ul><br>בהצלחה!</font></div>""",
        "notebook_parts": lambda text: f"""<div dir='rtl' align='center'><hr style="border: none; border-top: 2px solid; margin: 0;" color= '#7E30E1'><hr style="border: none; border-top: 2px solid; margin: 0;" color= '#7E30E1'><div dir="rtl" align='center'><font color='#7E30E1' size='6'><b>{text}</b></font><div dir='rtl' align='center'><hr style="border: none; border-top: 2px solid; margin: 0;" color= '#7E30E1'><hr style="border: none; border-top: 2px solid; margin: 0;" color= '#7E30E1'>""",
        "section_title": lambda text: f"""<div dir='rtl' align='right'><font color="#7E30E1" size='5'><b>{text}</b></font></div>""",
        "section_text": lambda text: f"""<div dir='rtl' align='right'><font size='4'>{text}</font></div>""",
        "question_title": lambda text: f"""<div dir='rtl' align='right'><font color='#7E30E1' size='4'><b>{text}</b></font></div>""",
        "image_load": lambda text: f"""<center>\n\n{text}""",
        "question_text": lambda text: f"""<div dir='rtl' align='right'><font size='4'>{text}</font></div>""",
        "images": lambda path: f"![Image]({path})",
        "stop_section": lambda text: f"""<div dir='rtl' align='center'><font color='#DC3535' size='8'><b>{text}</b></font><br><img src='stop_sign.png' alt='Stop Section'></div>""",
        "notebook_footer": lambda text: f"""<div dir='rtl' align='center'><font color='#7E30E1' size='14'><b>{text}</b></font><br><br></div>""",
    }

    if text_type == "images" and not path:
        raise ValueError("Path must be provided for 'images' text_type.")
    elif text_type == "reminder_mark":
        raw_html = styles[text_type]
    elif text_type not in styles:
        raise ValueError(f"Invalid text_type '{text_type}'. Valid options are: {list(styles.keys())}")
    else:
        raw_html = styles[text_type](text if text_type != "images" else path)

    soup = BeautifulSoup(raw_html, 'html.parser')
    prettified_html = soup.prettify()
    return nbf.v4.new_markdown_cell(prettified_html)


def extract_function_body(module_path, function_name):
    spec = importlib.util.spec_from_file_location("module", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    func = getattr(module, function_name)
    source_lines = inspect.getsourcelines(func)[0]
    return ''.join(line for line in source_lines[1:] if line.strip())



def generate_notebook(input_file, output_notebook, rephrase_with_llm=False):
    """
    Generates a .ipynb file based on input CSV/Excel file.
    """
    if input_file.endswith(".csv"):
        df = pd.read_csv(input_file)
    elif input_file.endswith(".xlsx"):
        df = pd.read_excel(input_file)
    else:
        raise ValueError("Unsupported file format. Use CSV or Excel.")

    required_columns = ['cell_id', 'cell_type', 'cell_script', 'markdown_type', 'text']

    notebook = nbf.v4.new_notebook()
    # notebook.cells.append(generate_markdown_cell(text="", text_type='reminder_mark'))

    for _, row in df.iterrows():
        cell_type = row['cell_type']
        content = row.get('content', '')

        if cell_type == 'images':
            continue
        if cell_type == 'code':
            cell_script = row.get('cell_script', '')
            notebook.cells.append(nbf.v4.new_code_cell(cell_script.strip()))

        elif cell_type == 'markdown':
            markdown_type = row.get('markdown_type', '')
            if markdown_type == "images":
                continue
            if markdown_type == 'drop':
                continue
            elif markdown_type == "image_load":
                notebook.cells.append(generate_markdown_cell(content, markdown_type))
            notebook.cells.append(generate_markdown_cell(content, markdown_type))
        else:
            raise ValueError(f"Unsupported cell type: {cell_type}")

    output_notebook = f"new_notebooks/{output_notebook}"
    with open(output_notebook, 'w') as f:
        nbf.write(notebook, f)

    print(f"Notebook generated and saved to {output_notebook}")


if __name__ == "__main__":
    hw = False
    notebook_type = "home_assigment" if hw else "class_assignment"
    number = 22
    file_title = f"{notebook_type}_{number}"
    old_notebook = f"old_notebooks/{file_title}.ipynb"
    file_to_extract = notebook_processor.start_extraction(notebook_path=old_notebook, file_title=file_title)
    input_file = f"extracted_cells/{file_title}_cells.csv"
    output_notebook = f"{file_title}_rephrased.ipynb"
    #generate_notebook(input_file=input_file, output_notebook=output_notebook)
