from langchain.document_loaders import PyPDFLoader, WebBaseLoader, NotionDirectoryLoader
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import OpenAIWhisperParser
from langchain.document_loaders.blob_loaders.youtube_audio import YoutubeAudioLoader

class DocumentLoading:
    def __init__(self, pdf: str = None, youtube: str = None, web: str = None, notion: str = None) -> None:
        self.__pdf = pdf
        self.__youtube = youtube
        self.__web = web
        self.__notion = notion

    # Methods for setting the path for the document
    def set_pdf(self, pdf: str):
        self.__pdf = pdf

    def set_youtube(self, youtube: str):
        self.__youtube = youtube

    def set_web(self, web: str):
        self.__web = web

    def set_notion(self, notion: str):
        self.__notion = notion

    # Load the document with a specified path
    def load_pdf(self):
        if not self.__pdf:
            raise ValueError("PDF path not provided")
        loader = PyPDFLoader(self.__pdf)
        pages = loader.load()
        return pages

    def load_youtube(self):
        if not self.__youtube:
            raise ValueError("YouTube URL not provided")
        loader = GenericLoader(
            YoutubeAudioLoader([self.__youtube], "docs/youtube/"),
            OpenAIWhisperParser()
        )
        docs = loader.load()
        return docs

    def load_url(self):
        if not self.__web:
            raise ValueError("Web URL not provided")
        loader = WebBaseLoader(self.__web)
        docs = loader.load()
        return docs

    def load_notion(self):
        if not self.__notion:
            raise ValueError("Notion directory not provided")
        loader = NotionDirectoryLoader(self.__notion)
        docs = loader.load()
        return docs

def main():
    # Initialize the document loading class
    doc_loader = DocumentLoading()

    documents = []

    # Set and load PDF document
    doc_loader.set_pdf("/Users/juma/Documents/SFBU_MSCS/major-projects/customer-support-chatbot/lang-chain/assets/sfbu-catalog.pdf")
    pdf_pages = doc_loader.load_pdf()
    documents.append(pdf_pages)

    doc_loader.set_youtube("https://www.youtube.com/watch?v=kuZNIvdwnMc")
    youtube_docs = doc_loader.load_youtube()
    documents.append(youtube_docs)

    doc_loader.set_web("")
    web_docs = doc_loader.load_url()
    documents.append(web_docs)
    
    doc_loader.set_notion("")
    notion_docs = doc_loader.load_notion()
    documents.append(notion_docs)

    print(documents[0])


if __name__ == '__main__':
    main()


