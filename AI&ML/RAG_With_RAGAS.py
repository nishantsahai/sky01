from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_text_splitters import CharacterTextSplitter
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv
load_dotenv()

# Load the data
loader = UnstructuredFileLoader("state_of_the_union.txt")
documents = loader.load()

# Chunk the data
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
# Vector store
vectorstore = Chroma(
    #documents=chunks,
    embedding_function=embeddings,
    persist_directory="./chroma_db",
    collection_name="rag_eval_collection"
)

#Add chunks
vectorstore.add_documents(chunks)

retriever = vectorstore.as_retriever()

# Build RAG chain
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

template = """
You are an assistant for question-answering tasks. 
Use the following pieces of retrieved context to answer the question. 
If you don't know the answer, say you don't know.
Use two sentences maximum.

Question: {question} 
Context: {context} 
Answer:
"""

prompt = ChatPromptTemplate.from_template(template)

rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# Evaluation dataset
eval_questions = [
    "What did the president say about Justice Breyer?",
    "What did the president say about Intel's CEO?",
    "What did the president say about gun violence?"
]

ground_truths = [
    "The president said that Justice Breyer has dedicated his life to serve the country and thanked him for his service.",
    "The president said that Pat Gelsinger is ready to increase Intel's investment to $100 billion.",
    "The president asked Congress to pass proven measures to reduce gun violence."
]

answers = []
contexts = []

for query in eval_questions:
    answers.append(rag_chain.invoke(query))

    retrieved_docs = retriever.invoke(query)
    #docs = retrieved["context"]
    contexts.append([doc.page_content for doc in retrieved_docs])

data = {
    "question": eval_questions,
    "answer": answers,
    "contexts": contexts,
    "ground_truth": ground_truths
}

dataset = Dataset.from_dict(data)

# Run Ragas evaluation
result = evaluate(
    dataset=dataset,
    metrics=[faithfulness, answer_relevancy, context_precision, context_recall]
)

print(result.to_pandas())