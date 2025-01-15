from enum import Enum


class Prompts(Enum):
    BOT = 'Hi, I am your AI assistant. How can I help you today?'
    SEARCH = 'Based on your knowledge answer factually asked question in given language.'
    RAG_SEARCH = ' '.join([
        'Based on your knowledge and doc text, answer factually asked question in given language.',
        'Add information about source when answering from documents.',
        'Given context: {context}'
    ])
    RAG_KEYWORDS = ' '.join([
        'Generate meaningful keywords that are unique for this chunk of text in given language.',
        'Answer only in json.loads() format with "keywords" key.',
        'Keyword is just one word, no urls or special characters.',
        'Given text: {text}',
    ])
    RAG_QUERY = ' '.join([
        'Based on question, create keywords and accurate question to help search for relevant information in documents.',
        'Answer in given language.',
        'Given question: {question}',
    ])
    RAG_SUMMARIZE = ' '.join([
        'Summarize given text without changing meaning and personal form.',
        'Answer in given language.',
        'If u cant return original text.',
    ])
