from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = API_KEY


# def load_documents():
#     loader = PyPDFLoader("AI/PDFs/Financeiro.pdf")
#     docs = loader.load()
#     splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
#     chunks = splitter.split_documents(docs)

#     return chunks


def get_vectorstore():
    persist_dir = "AI/vectorstore"
    embeddings = OpenAIEmbeddings()
    # if os.path.exists(persist_dir):
    vs = Chroma(persist_directory=persist_dir,
                embedding_function=embeddings)
    # else:
    #     vs = Chroma.from_documents(
    #         documents=doc_texts,
    #         embedding=embeddings,
    #         persist_directory=persist_dir
    #     )
    vs.persist()
    return vs


def generate_rag_response(user_data):
    # texts = load_documents()
    vs = get_vectorstore()

    retriever = vs.as_retriever(search_kwargs={"k": 3})
    llm = ChatOpenAI(model_name="gpt-4o", temperature=0)
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff", retriever=retriever)

    context = f"""
    Você é um assistente financeiro ligado a um sistema de finanças pessoais. Dê respostas objetivas e concisas.
    Dados do usuário extraídos do sistema de finanças pessoais:
    {user_data}
    """

    question = '''
        Você é um assistente financeiro. Analise os dados do usuário e os documentos financeiros fornecidos, e gere respostas objetivas, concisas e acionáveis.

        Regras:
        1. Responda em **até cinco sentenças**, sempre se referindo ao usuário como "você".
        2. Inclua **fontes ou referências** sempre que possível, utilizando o documento PDF como base, mas nunca revele a seção do documento; cite a instituição ou estudo relevante.
        3. Forneça **pelo menos uma dica prática de finanças ou investimento** por resposta; seja criativo e vá além de fundos de investimento.
        4. Destaque categorias com gastos fora da curva ou exagerados, sugerindo ajustes se necessário.
        5. Priorize clareza e utilidade para **decisões financeiras pessoais atuais**; use dados dos dois meses anteriores apenas para comparação ou identificação de padrões.
        6. Nunca mencione que você é uma IA ou modelo de linguagem.
        7. Sempre que possível, sugira ações concretas que o usuário pode tomar para melhorar sua saúde financeira.
        8. Inclua sugestões de **investimentos populares no Brasil**, tanto de renda fixa quanto variável, adequando ao perfil do usuário e oferecendo opções.
        9. Evite citar a Receita Federal; prefira outras fontes confiáveis.
        10. Se possível, combine insights dos PDFs com os dados do usuário para gerar recomendações mais precisas e contextualizadas.
    '''

    response = qa_chain.run(f"{context}\nPergunta: {question}")
    return response
