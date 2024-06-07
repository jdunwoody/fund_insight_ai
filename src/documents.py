import re
import shelve
from hashlib import sha256

from langchain.schema import Document
from langchain_community.document_loaders.pdf import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from tqdm import tqdm


def load_docs(file_paths):
    docs = []

    for file_path in tqdm(file_paths, desc="loading docs"):
        doc = load_doc(file_path=file_path)

        docs += [doc.page_content]

    return docs
    # docs_texts = [d.page_content.strip() for d in docs]

    # d_sorted = sorted(docs, key=lambda x: x.metadata["source"])
    # d_reversed = list(reversed(d_sorted))
    # concatenated_content = "\n\n\n --- \n\n\n".join(
    #     [doc.page_content for doc in d_reversed]
    # )

    # text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    #     chunk_size=200, chunk_overlap=0
    # )
    # texts_split = text_splitter.split_text(concatenated_content)

    # return docs_texts, texts_split


def load_doc(file_path):
    pages = load_pages(file_path=file_path)

    return "\n".join([page for page in pages])


def clean(text):
    result = re.sub("^[\d\W]*", "", text)

    return result.strip()


def load_pages(file_path):
    with shelve.open(".cache_preprocessed_docs") as cache:
        # cache.clear()

        file_path_str = str(file_path)

        if file_path_str in cache:
            pages = cache[file_path_str]
        else:
            loader = PyMuPDFLoader(
                file_path=file_path,
                extract_images=False,
                # extractor=lambda x: Soup(x, "html.parser").text,
            )
            raw_pages = loader.load()

            pages = [clean(page.page_content) for page in raw_pages]
            cache[file_path_str] = pages

    return pages
