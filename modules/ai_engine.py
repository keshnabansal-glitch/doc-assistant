import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def summarize_document(text):
    """
    Takes the extracted document text and returns a plain-language
    summary highlighting important/risky clauses.
    """
    prompt = f"""You are helping a non-expert understand a document.
Summarize the following document in plain, simple language.
Highlight any important or risky clauses (deadlines, payments, penalties,
obligations) clearly, without legal jargon.

Document:
{text}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
    )

    return response.choices[0].message.content

def answer_question(text, question):
    """
    Takes the document text and a user's question, and returns
    an answer grounded in the document content.
    """
    prompt = f"""You are answering questions about a specific document.
Only use information found in the document below to answer.
If the answer isn't in the document, say so clearly instead of guessing.

Document:
{text}

Question: {question}

Answer:"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content