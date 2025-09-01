from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv
from AI.FinnhubAPI import generate_asset_summary

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
    stock_summary = generate_asset_summary()

    retriever = vs.as_retriever(search_kwargs={"k": 3})
    llm = ChatOpenAI(model_name="gpt-4o", temperature=0)
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff", retriever=retriever)

    context = f"""
    Você é um assistente financeiro pessoal, ligado a um sistema de finanças pessoais. Dê respostas objetivas e concisas.

    Dados do usuário extraídos do sistema de finanças pessoais:
    {user_data}

    Resumo dos principais ativos do mercado atualmente:
    {stock_summary}  
    """

    question = '''
    Você é um assistente financeiro. Analise os dados do usuário e os documentos financeiros fornecidos, e gere respostas objetivas, concisas e acionáveis.

    Regras:
    1. Responda em **até cinco sentenças**, sempre se referindo ao usuário como "você".
    2. Analise padrões de gastos e investimentos, destacando categorias fora da curva e sugerindo ajustes quando necessário.
    3. Gere **três recomendações concretas** por resposta, incluindo pelo menos uma dica prática de finanças ou investimento. Seja criativo, indo além de fundos de investimento.Pórem se o usuário tiver uma boa saúde financeira, elogie e apenas sugira cortar gastos se tive um gasto muito exagerado.
    4. Inclua sugestões de **investimentos populares no Brasil**, tanto de renda fixa quanto variável, adequadas ao perfil do usuário.
    5. Utilize referências confiáveis sempre que possível (B3, CVM, Banco Central, IBGE, XP Investimentos, BTG Pactual), sem mencionar Receita Federal.
    6. Priorize clareza e utilidade para **decisões financeiras pessoais atuais**; use dados dos dois meses anteriores apenas para comparação ou identificação de padrões.
    7. Combine insights dos PDFs com os dados do usuário para gerar recomendações mais precisas e contextualizadas.
    8. Formate as recomendações numeradas para facilitar leitura.
    9. Nunca mencione que você é uma IA ou modelo de linguagem.
    10. Sempre que possível, sugira ações concretas que o usuário pode tomar para melhorar sua saúde financeira.
    11. Sempre que mencionar ativos financeiros, converta siglas em nomes amigáveis para o usuário
    12. Sempre mostre o resumo do ativo escolhido para indicação, tente dar duas opções de investimento vindas do resumo, sempre analisando todas opções e oferencendo as duas melhores, mostrando dados que comprovem aquela escolha.
    13. Nunca use markdown para dar a resposta. Quero a resposta em texto natural, como se estivesse conversando com um humano.
    14. Caso alguma criptomoeda seja recomendada, sugira ela.
    '''

    response = qa_chain.run(f"{context}\nPergunta: {question}")
    return response
