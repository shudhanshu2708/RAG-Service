from fastapi import FastAPI , UploadFile
from pypdf import PdfReader
import chromadb 
from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(model="nomic-embed-text")
client = chromadb.Client()
collection = client.create_collection(name="documents")

app = FastAPI()

def chunk_text(text , chunk_size=200):

    chunks = []
    for i in range(0 , len(text) , chunk_size):
        chunk = text[i : i + chunk_size]
        chunks.append(chunk)

    return chunks



def extract_text_from_pdf(filepath):
    reader = PdfReader(filepath)
    full_text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        full_text += page_text

    return full_text

if __name__ == "__main__":
    text = extract_text_from_pdf("uploads/Sudhanshu_Singh_Resume.pdf")
    print(text[:200]) 
    print("---")
    print(len(text))  



@app.get("/")
def index():
    return {"message" : "hellow world"}


@app.post("/upload")
def upload_file(file: UploadFile):
    contents = file.file.read() #read the file

    with open(f"uploads/{file.filename}","wb") as f:
        f.write(contents)

    text = extract_text_from_pdf(f"uploads/{file.filename}")  

    chunks = chunk_text(text)
    ids = [f"chunk_{i}" for i, chunk in enumerate(chunks)]
    chunk_embeddings = embeddings.embed_documents(chunks)

    collection.add(
    documents=chunks,
    embeddings=chunk_embeddings,
    ids=ids
)

    print(collection.count())
     

    return {"filename" : file.filename , "chunks": len(chunks)}

@app.get("/count")
def get_count():
    return {"total_chunks": collection.count()}