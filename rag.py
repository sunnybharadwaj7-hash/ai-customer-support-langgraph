from langchain_community.document_loaders import TextLoader

from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_community.vectorstores import FAISS

from langchain_ollama import OllamaEmbeddings


DOCUMENTS = [
    "documents/company_policy.txt",
    "documents/pricing_guide.txt",
    "documents/technical_manual.txt",
    "documents/faq.txt"
]


def load_documents():

    docs = []

    for file in DOCUMENTS:
        loader = TextLoader(file)
        docs.extend(loader.load())

    return docs


def create_vector_store():

    docs = load_documents()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(docs)

    embeddings = OllamaEmbeddings(
        model="nomic-embed-text"
    )

    vector_db = FAISS.from_documents(
        chunks,
        embeddings
    )

    return vector_db


vector_db = create_vector_store()


def retrieve_context(query):

    docs = vector_db.similarity_search(
        query,
        k=3
    )

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    return context