from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI

def setup_doc_search():
    embeddings = OpenAIEmbeddings()
    text_splitter = CharacterTextSplitter(chunk_size=1000)
    
    # Example texts for embedding
    texts = ["Example text 1", "Example text 2", "Example text 3"]
    docsearch = FAISS.from_texts(texts, embeddings)

    prompt_template = PromptTemplate(
        input_variables=["input_documents", "question"],
        template="Combine the documents to answer the question: {question}"
    )
    qa_chain = load_qa_chain(OpenAI(temperature=0.7, max_tokens=100), chain_type="stuff", prompt=prompt_template)
    
    return docsearch, qa_chain

def search_documents(docsearch, query):
    docs = docsearch.similarity_search(query)
    return docs[:3]  # 確保選取部分文檔避免超過上下文長度限制
