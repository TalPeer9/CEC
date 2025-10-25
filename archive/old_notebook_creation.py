import pandas as pd
import nbformat as nbf
import os
import inspect
import importlib.util

colors = {"basic_purple": "#7E30E1", "challenge": ""}


def extract_function_body(module_path, function_name):
    spec = importlib.util.spec_from_file_location("module", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    func = getattr(module, function_name)
    source_lines = inspect.getsourcelines(func)[0]
    return ''.join(line for line in source_lines[1:] if line.strip())


def generate_notebook(input_file, functions_path, output_notebook):
    """
    Generates an(.ipynb) file based on input CSV/Excel file.
    :param input_file: Path to the CSV/Excel file with notebook structure.
    :param functions_path: Path to the Python script containing functions.
    :param output_notebook: Path to save the generated .ipynb file.
    """

    if input_file.endswith(".csv"):
        df = pd.read_csv(input_file)
    elif input_file.endswith(".xlsx"):
        df = pd.read_excel(input_file)
    else:
        raise ValueError("Unsupported file format. Use CSV or Excel.")
    required_columns = ['cell_id', 'cell_type', 'cell_script', 'markdown_type', 'content']
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"Input file must contain the following columns: {required_columns}")

    notebook = nbf.v4.new_notebook()
    for _, row in df.iterrows():
        cell_type = row['cell_type']
        cell_script = row.get('cell_script', '')
        markdown_type = row.get('markdown_type', '')
        content = row.get('content', '')

        if cell_type == 'code':
            notebook.cells.append(nbf.v4.new_code_cell(cell_script.strip()))
            # if cell_script.startswith("from "):
            #     try:
            #         module, function_name = cell_script.replace("from ", "").replace(" import ", ".").split('.')
            #     except ValueError:
            #         raise ValueError(
            #             f"Invalid format for cell_script: {cell_script}. Expected 'from <module> import <function>'.")
            #     if not module.endswith("functions"):
            #         raise ValueError(f"Module must be 'functions'. Found: {module}")
            #
            #     function_body = extract_function_body(functions_path, function_name)
            #     notebook.cells.append(nbf.v4.new_code_cell(function_body))
            # else:
            #     notebook.cells.append(nbf.v4.new_code_cell(cell_script))

        elif cell_type == 'markdown':
            markdown_content = ""
            if markdown_type == "notebook_header":
                notebook_header = content
                # markdown_content = f"""<div dir='rtl' align='center'><hr style="border: none; border-top: 2px solid; margin: 0;" color= '#7E30E1'><hr style="border: none; border-top: 2px solid; margin: 0;" color= '#7E30E1'><font color='#7E30E1' size='12'><b>{notebook_header}</b></font><hr style="border: none; border-top: 2px solid; margin: 0;" color= '#7E30E1'><hr style="border: none; border-top: 2px solid; margin: 0;" color= '#7E30E1'></div>"""
                # markdown_content = f"<div dir='rtl' align='Center'><hr color=\"#7E30E1\"><b><font color='#7E30E1' size='16'> {notebook_header} <hr color=\"#7E30E1\"></font><br>"
                markdown_content = f"<div dir='rtl' align='center'><br><br><font color='#7E30E1' size='16'><b> {notebook_header} </b></font><br><br>"
            elif markdown_type == "notebook_parts":
                part_number = content
                markdown_content = f"""<div dir='rtl' align='center'><hr style="border: none; border-top: 2px solid; margin: 0;" color= '#7E30E1'"><hr style="border: none; border-top: 2px solid; margin: 0;" color= '#7E30E1'"><font color="#7E30E1" size='12'><b> {part_number} </b></font><div dir='rtl' align='center'><div dir='rtl' align='center'><hr style="border: none; border-top: 2px solid; margin: 0;" color= '#7E30E1'"><hr style="border: none; border-top: 2px solid; margin: 0;" color= '#7E30E1'"><font color="#7E30E1" size='12'><b>"""
            elif markdown_type == "section_title":
                section_number = content
                markdown_content = f"<div dir='rtl' align='right'><font color=\"#7E30E1\" size='5'><b> {section_number} </b></font></div>"
            elif markdown_type == "section_text":
                markdown_content = f"<div dir='rtl' align='right'><font size='4'> {content} <br></div>"
            elif markdown_type == "question_title":
                question_title = content
                markdown_content = f"<div dir=rtl align=right><font color='#7E30E1' size='4'><b> {question_title} </b></font></div>"
            elif markdown_type == "question_text":
                question_text = content
                markdown_content = f"<div dir='rtl'><font size='4'> {question_text} </b></font></div>"
            elif markdown_type == "images":
                image_path = content
                markdown_content = f"![Image]({image_path})"
            elif markdown_type == "stop_section":
                stop_section = content
                image_path = 'img/stop_sign.png'
                stop_image = f"<div dir='rtl' align='center'> ![Image]({image_path})"
                notebook.cells.append(nbf.v4.new_markdown_cell(stop_image))
                markdown_content = f"<div dir='rtl' align='center'><font color='#DC3535' size='8'><b><br> {stop_section} </b>"
            else:
                raise ValueError(f"Unsupported markdown type: {markdown_type}")
            markdown_content = markdown_content.strip()
            notebook.cells.append(nbf.v4.new_markdown_cell(markdown_content))

        else:
            raise ValueError(f"Unsupported cell type: {cell_type}")

    with open(output_notebook, 'w') as f:
        nbf.write(notebook, f)

    print(f"Notebook generated and saved to {output_notebook}")


if __name__ == "__main__":
    input_file = "home_assigment_13.csv"
    functions_path = "../functions.py"
    output_notebook = "home_assigment_13.ipynb"
    generate_notebook(input_file=input_file, output_notebook=output_notebook, functions_path=functions_path)

cell_type = row['cell_type']
cell_script = row.get('cell_script', '')
markdown_type = row.get('markdown_type', '')
content = row.get('content', '')

if cell_type == 'code':
    if cell_script.startswith("from "):
        try:
            module, function_name = cell_script.replace("from ", "").replace(" import ", ".").split('.')
        except ValueError:
            raise ValueError(
                f"Invalid format for cell_script: {cell_script}. Expected 'from <module> import <function>'.")
        if not module.endswith("functions"):
            raise ValueError(f"Module must be 'functions'. Found: {module}")

        function_body = extract_function_body(functions_path, function_name)
        notebook.cells.append(nbf.v4.new_code_cell(function_body))
    else:
        notebook.cells.append(nbf.v4.new_code_cell(cell_script))


