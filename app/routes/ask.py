from fastapi import APIRouter
from pydantic import BaseModel
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from app.core.vectorstore import vectorstore

router = APIRouter(prefix="/ask", tags=["Ask"])


class AskRequest(BaseModel):
    question: str


llm = OllamaLLM(model="llama3.2:3b")
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

prompt = ChatPromptTemplate.from_template("""
Answer the question using ONLY the context below.
If the answer is not present in the context, say "I don't know."

Context:
{context}

Question: {question}
Answer:
""")


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)


@router.post("")
def ask_question(request: AskRequest):
    answer = rag_chain.invoke(request.question)
    docs = retriever.invoke(request.question)   # sources dikhane ke liye alag se retrieve
    return {
        "answer": answer,
        "sources": [doc.metadata for doc in docs]
    }