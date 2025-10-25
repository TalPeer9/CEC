import pandas as pd
from jinja2 import Template
import nbformat as nbf
from bs4 import BeautifulSoup
import markdown


def generate_notebook(input_file):

    df = pd.read_csv(input_file)

    notebook_content = df.to_dict(orient='records')
    print(notebook_content)

    with open('htmls/hw_notebook.html', 'r', encoding='utf-8') as file:
        html_template = file.read()

    # Create the template object from the HTML template
    template = Template(html_template)

    # Prepare the content data for template rendering
    rendered_html = ""
    notebook = nbf.v4.new_notebook()
    for content_data in notebook_content:
        rendered_cell = template.render(content_data)
        notebook.cells.append(nbf.v4.new_markdown_cell(rendered_cell))

    with open('output_notebook.ipynb', 'w', encoding='utf-8') as output_file:
        nbf.write(notebook, output_file)


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
    cleaned_text = soup.get_text(separator=' ').strip().replace('#', '')
    return cleaned_text


def extract_design_attributes(raw_text):
    """
    Extracts design-related attributes (e.g., CSS styles, HTML tags, and their attributes)
    from a Markdown cell's raw content by converting Markdown to HTML.

    Args:
        raw_text (str): Raw markdown content from the cell.

    Returns:
        list[dict]: A list of dictionaries containing design-related attributes for each tag.
    """

    html_content = markdown.markdown(raw_text)
    soup = BeautifulSoup(html_content, 'html.parser')
    design_elements = []
    for element in soup.find_all(True):
        design_attributes = {
            "tag": element.name,
            "attributes": element.attrs,
            "text": element.text.replace('#', '')
        }
        design_elements.append(design_attributes)

    return design_elements


def extract_design_attributes2(raw_text):
    """
    Extracts design-related attributes (e.g., CSS styles, HTML tags, and their attributes)
    from a markdown cell's raw HTML.

    Args:
        raw_text (str): Raw markdown content from the cell.

    Returns:
        list[dict]: A list of dictionaries containing design-related attributes for each tag.
    """
    # Parse the raw text as HTML
    soup = BeautifulSoup(raw_text, 'html.parser')

    # Find all elements with attributes
    design_elements = []
    for element in soup.find_all(True):  # True finds all tags
        design_attributes = {
            "tag": element.name,
            "attributes": element.attrs,
            "text": element.text.replace('#', '')  # Extract inner text
        }
        design_elements.append(design_attributes)

    return design_elements


def generate_html_with_bs(text, text_type):
    """
    Generates an HTML string based on the given text and text_type using BeautifulSoup.

    Args:
        text (str): The content to be wrapped in the HTML design.
        text_type (str): The type of text, which determines the design.

    Returns:
        str: The HTML string with the specified design.
    """
    # Define designs for various text types
    designs = {
        "question_title": {
            'div': {'align': 'center', 'dir': 'rtl'},
            'font': {'color': '#9EB9F6', 'size': '5'},
            'bold_text': True, },
        "question_text": {
            'div': {'align': 'center', 'dir': 'rtl'},
            'font': {'color': '#9EB9F6', 'size': '5'},
            'bold_text': True,
        }
    }

    # Get the design for the given text_type
    design = designs.get(text_type)
    if not design:
        raise ValueError(f"Design for text_type '{text_type}' is not defined.")

    # Create a BeautifulSoup object for building HTML
    soup = BeautifulSoup("", 'html.parser')

    # Create the <div> tag with attributes
    div_tag = soup.new_tag("div", **design.get('div', {}))

    # Create the <font> tag with attributes
    font_tag = soup.new_tag("font", **design.get('font', {}))

    # Wrap the text in bold if specified
    if design.get('bold_text', False):
        b_tag = soup.new_tag("b")
        b_tag.string = text
        font_tag.append(b_tag)
    else:
        font_tag.string = text

    # Nest the tags appropriately
    div_tag.append(font_tag)

    # Return the formatted HTML string
    return div_tag.prettify()


def generate_html(text, text_type, path=None):
    """
    Generates HTML based on the text type and the styles dictionary.

    Args:
        text (str): The content to be wrapped in the HTML design.
        text_type (str): The type of text which determines the design.
        path (str, optional): Path for images, used for "images" text_type.

    Returns:
        str: Prettified HTML string.
    """
    styles = {
        "notebook_header": lambda text: f"""
        <div dir='rtl' align='center'>
            <font color='#7E30E1' size='16'><b>{text}</b></font><br><br>
        </div>
        """,
        "notebook_type": lambda text: f"""<div dir="rtl" align='center'><font color='#7E30E1' size='14'><b>
        {text}
        </b></font>
        """,
        "notebook_parts": lambda text: f"""<div dir='rtl' align='center'><hr style="border: none; border-top: 2px solid; margin: 0;" color= '#7E30E1'><hr style="border: none; border-top: 2px solid; margin: 0;" color= '#7E30E1'><div dir="rtl" align='center'><font color='#7E30E1' size='6'><b>
        {text}
        </b></font><div dir='rtl' align='center'><hr style="border: none; border-top: 2px solid; margin: 0;" color= '#7E30E1'><hr style="border: none; border-top: 2px solid; margin: 0;" color= '#7E30E1'>
                """,
        "section_title": lambda text: f"""
        <div dir='rtl' align='right'>
            <font color="#7E30E1" size='5'><b>{text}</b></font>
        </div>
        """,
        "section_text": lambda text: f"""
        <div dir='rtl' align='right'>
            <font size='4'>{text}</font>
        </div>
        """,
        "question_title": lambda text: f"""
        <div dir='rtl' align='right'>
            <font color='#7E30E1' size='4'><b>{text}</b></font>
        </div>
        """,
        "question_text": lambda text: f"""
        <div dir='rtl' align='right'>
            <font size='4'>{text}</font>
        </div>
        """,
        "images": lambda path: f"![Image]({path})",
        "stop_section": lambda text: f"""
        <div dir='rtl' align='center'><font color='#DC3535' size='8'><b>
        {text}
        </b></font><br>
        <img src='stop_sign.png' alt='Stop Section'>
        </div>
        """
    }

    if text_type not in styles:
        raise ValueError(f"Invalid text_type '{text_type}'. Valid options are: {list(styles.keys())}")

    if text_type == "images" and not path:
        raise ValueError("Path must be provided for 'images' text_type.")

    raw_html = styles[text_type](text if text_type != "images" else path)

    soup = BeautifulSoup(raw_html, 'html.parser')
    prettified_html = soup.prettify()
    return prettified_html

raw_input = """place holder"""
design_info = extract_design_attributes2(raw_input)

print(design_info[0]['text'])
raw_input = design_info[0]['text']
output = clean_markdown_cell(raw_input)
print(output)
print(generate_html_with_bs(output,text_type='question_text'))
# soup = BeautifulSoup(design_info, 'html.parser')
# print(soup.prettify())
