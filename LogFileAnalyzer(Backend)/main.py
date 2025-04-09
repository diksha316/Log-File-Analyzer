from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import logging
import requests
from huggingface_hub import configure_http_backend

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def backend_factory() -> requests.Session:
    session = requests.Session()
    session.verify = False  
    return session

configure_http_backend(backend_factory=backend_factory)

app = FastAPI()

# Enabling CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

API_KEY = "AIzaSyBN9Cdk_x5IQ_LPi41lR4fq2K0P2qNbdbQ"  
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

MAX_FILE_SIZE = 5 * 1024 * 1024
vectorstore = None

def read_log_file(file: UploadFile) -> str:
    try:
        contents = file.file.read()
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File size exceeds 5MB limit.")
        return contents.decode("utf-8")
    except Exception as e:
        logger.error(f"Error reading file: {e}")
        raise HTTPException(status_code=400, detail=f"Error reading file: {e}")

@app.post("/upload/")
async def upload_log_file(file: UploadFile = File(...)):
    global vectorstore
    try:
        if not file.filename.endswith((".txt", ".log")):
            raise HTTPException(status_code=400, detail="Only .txt or .log files are supported.")
        
        log_content = read_log_file(file)
        logger.info("File uploaded successfully.")

        # 1. Creating chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200) 
        documents = text_splitter.create_documents([log_content])

        # 2. Creating Vector Embeddings
        embeddings = HuggingFaceEmbeddings()
        vectorstore = FAISS.from_documents(documents, embeddings)
        logger.info("Log file indexed successfully.")

        # 3. Relevant chunks
        retriever = vectorstore.as_retriever()
        relevant_chunks = retriever.get_relevant_documents("Analyze the log file")
        context = "\n".join([chunk.page_content for chunk in relevant_chunks])

        prompt = (
            f"Context:\n{context}\n\n"
            f"The log file contains multiple status codes and details. "
            f"Count the total number of errors that the file contains."
            f"Please analyze the content and provide a detailed broad description, "
            f"Including a summary of all the status codes present and their meanings. "
            f"Organize the summary in a tabular format if applicable."
        )
        logger.info(f"Generated prompt: {prompt}")

        response = model.generate_content(prompt)

        if not response or not hasattr(response, "text"):
            raise HTTPException(status_code=500, detail="No valid response received from the Gemini model.")

        generated_response = response.text
        return {"message": "Log file processed successfully.", "analysis": generated_response}

    except Exception as e:
        logger.error(f"Error processing log file: {e}")
        return JSONResponse(content={"detail": str(e)}, status_code=500)
