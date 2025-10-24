import openai
from openai import OpenAI
import config

client = OpenAI(api_key=config.OPENAI_API_KEY)


def rephrase_text_hebrew(input_text):
    """
    Rephrases the given Hebrew text into a clearer version using OpenAI's GPT API.

    Args:
        input_text (str): The original Hebrew text to rephrase.

    Returns:
        str: Rephrased Hebrew text.
    """

    system_instruction = (
        "You are a Hebrew language assistant. Your task is to rephrase the given text "
        "into clearer Hebrew while keeping the original meaning. The text is for 15-year-old "
        "kids learning AI. Format the text to be more understandable by adding line breaks, "
        "commas, and other punctuation where needed to improve clarity. Simplify the language "
        "if necessary to suit their understanding level."
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": input_text}
        ],
        temperature=0.8
    )

    return response


input_text = """

 באמצעות איזה גרפים כדאי להציג משתנים אלה?
  באמצעות ספריית סיברון הציגו גרף מתאים למשתנה גיל ולחץ דם, כתבו מסקנות חדשות שהסקתם מהייצוג הגרפי#

**למדריך - חלק ייבחרו בBOXPLOT וחלק בהיסטוגרמה התרגיל בכוונה לא נותן פיתרון אחד נכון כי זה יוביל לדיון בכיתה שתבצעו"""
#rephrased_text = rephrase_text_hebrew(input_text)
# print("Original Text:", input_text)
#print(rephrased_text)
