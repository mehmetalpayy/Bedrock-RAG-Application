from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .requests import ChatRequest, RetrievalRequest
from .responses import ChatResponse, RetrievalResponse
from .bedrock import BedrockChunkRetriever
from .logger import RichLogger

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
    try:
        user_input = request.user_input
        response_message = f"LLM'den yanıt: {user_input} mesajınızı aldım, işliyorum."
        
        return ChatResponse(
            answer=response_message,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post("/retrieve_chunks", response_model=RetrievalResponse)
async def retrieve(request: RetrievalRequest):
    try:
        retriever = BedrockChunkRetriever()

        metadata_filter = {
            "equals": {
                "key": "x-amz-bedrock-kb-source-uri",
                "value": [f"s3://bedrock-agentic-rag/{file_id}" for file_id in request.file_ids]
            }
        }
        
        results = await retriever.retrieve(request.user_input, number_of_results=4, metadata_filter=metadata_filter)
        
        return RetrievalResponse(chunks=results)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))