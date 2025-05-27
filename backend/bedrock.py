import os
import boto3
from typing import List, Dict, Any, Optional
from backend.logger import RichLogger
from dotenv import load_dotenv
load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
REGION_NAME = os.getenv("AWS_REGION", "eu-central-1")
KNOWLEDGE_BASE_ID = os.getenv("KNOWLEDGE_BASE_ID", "")


class BedrockChunkRetriever:
    def __init__(self):
        self.logger = RichLogger("BedrockChunkRetriever")
        self.session = boto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=REGION_NAME
        )
        self.kb_client = self.session.client("bedrock-agent-runtime")
        self.knowledge_base_id = KNOWLEDGE_BASE_ID
        self.logger.success("Successfully initialized BedrockChunkRetriever and connected to Bedrock agent runtime.")

    def retrieve(
        self,
        query: str,
        number_of_results: int = 5,
        metadata_filter: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        self.logger.info(f"Retrieving chunks for query: '{query}' with top {number_of_results} results.")
        retrieval_config = {
            "vectorSearchConfiguration": {
                "numberOfResults": number_of_results
            }
        }
        if metadata_filter:
            self.logger.debug(f"Applying metadata filter: {metadata_filter}")
            retrieval_config["vectorSearchConfiguration"]["filter"] = metadata_filter

        response = self.kb_client.retrieve(
            retrievalQuery={"text": query},
            knowledgeBaseId=self.knowledge_base_id,
            retrievalConfiguration=retrieval_config
        )
        results = []
        for item in response.get("retrievalResults", []):
            chunk_content = item.get("content", "")
            if isinstance(chunk_content, dict) and "text" in chunk_content:
                chunk_text = chunk_content["text"]
            else:
                chunk_text = chunk_content
            results.append({
                "chunk": chunk_text,
                "score": item.get("score", None)
            })
        self.logger.success(f"Retrieved {len(results)} chunks from Bedrock.")
        return results