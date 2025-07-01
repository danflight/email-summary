"""
src/summary.py

Provides functions to summarize email snippets or bodies using either
Hugging Face transformers (BART), extractive TextRank (sumy), or OpenAI ChatGPT.
"""

from typing import List
import os

def summarize_emails_snippets(snippets: List[str], method: str = 'transformers', openai_api_key: str = None) -> str:
    """
    Summarizes a list of email snippets or bodies into a short text.

    Args:
        snippets (List[str]): List of email snippets or bodies to summarize.
        method (str): Summarization method. 'transformers' uses BART (default),
            'textrank' uses extractive TextRank (sumy), 'chatgpt' uses OpenAI ChatGPT.
        openai_api_key (str): OpenAI API key for ChatGPT summarization (optional).

    Returns:
        str: The summarized text.

    Raises:
        ValueError: If an unknown summarization method is provided.
    """
    summary = ""
    if method == 'transformers':
        from transformers import pipeline
        summarizer = pipeline('summarization', model='facebook/bart-large-cnn')
        joined = " ".join(snippets)
        # BART has a max token limit, so chunk if needed
        max_chunk = 1024
        chunks = [joined[i:i+max_chunk] for i in range(0, len(joined), max_chunk)]
        summarized = [summarizer(chunk, max_length=130, min_length=30, do_sample=False)[0]['summary_text'] for chunk in chunks]
        summary = " ".join(summarized)
    elif method == 'textrank':
        from sumy.parsers.plaintext import PlaintextParser
        from sumy.nlp.tokenizers import Tokenizer
        from sumy.summarizers.text_rank import TextRankSummarizer
        joined = " ".join(snippets)
        parser = PlaintextParser.from_string(joined, Tokenizer("english"))
        summarizer = TextRankSummarizer()
        summary_sentences = summarizer(parser.document, 5)
        summary = " ".join(str(sentence) for sentence in summary_sentences)
    elif method == 'chatgpt':
        import openai
        openai.api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
        prompt = (
            "Summarize the following emails into a short, clear summary:\n\n" +
            "\n\n".join(snippets)
        )
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.5,
        )
        summary = response.choices[0].message['content'].strip()
    else:
        raise ValueError("Unknown summarization method")
    return summary
