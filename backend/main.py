from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .requests import ChatRequest, RetrievalRequest
from .responses import ChatResponse, RetrievalResponse
from .bedrock import BedrockChunkRetriever
from langchain_google_genai import ChatGoogleGenerativeAI
from .logger import RichLogger
from dotenv import load_dotenv
load_dotenv()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = RichLogger()


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    response: Response = await call_next(request)
    logger.info(f"Response status: {response.status_code} for {request.method} {request.url}")
    return response


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    logger.info(f"Received /chat request with body: {request}")
    try:
        user_input = request.user_input
        logger.info(f"User input: {user_input}")
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0
        )
        logger.info("ChatGoogleGenerativeAI model initialized.")
        response = llm.invoke(input=user_input)
        logger.info(f"Model response: {response}")
        return ChatResponse(
            answer=response.content
        )
    except Exception as e:
        logger.error(f"Error in /chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post("/retrieve_chunks", response_model=RetrievalResponse)
async def retrieve(request: RetrievalRequest):
    logger.info(f"Received /retrieve_chunks request with body: {request}")
    try:
        retriever = BedrockChunkRetriever()
        logger.info("BedrockChunkRetriever instance created.")

        answer = await retriever.retrieve(
            query=request.query
        )
        logger.info(f"BedrockChunkRetriever returned answer: {answer}")
        
        return ChatResponse(answer=answer)

    except Exception as e:
        logger.error(f"Error in /retrieve_chunks endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))