import os
import boto3
from backend.logger import RichLogger
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_aws import ChatBedrock
from langchain_aws.retrievers import AmazonKnowledgeBasesRetriever
from dotenv import load_dotenv
load_dotenv()


class BedrockChunkRetriever:
    def __init__(self):
        self.logger = RichLogger("BedrockChunkRetriever")
        self.logger.info("Initializing BedrockChunkRetriever...")
        self.session = boto3.Session(
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
        )
        self.logger.info("Boto3 session created.")
        
        self.kb_client = self.session.client("bedrock-agent-runtime")
        self.logger.info("bedrock-agent-runtime client initialized.")
        self.runtime_client = self.session.client("bedrock-runtime")
        self.logger.info("bedrock-runtime client initialized.")
        
    async def retrieve(
        self,
        query: str
    ) -> str:
        self.logger.info(f"Entered retrieve() with query: '{query}'")
        
        try:
            model_kwargs_claude = {
                "temperature": 0,
                "max_tokens": 500
            }
            self.logger.debug(f"Model kwargs: {model_kwargs_claude}")
            llm = ChatBedrock(
                model_id="eu.meta.llama3-2-3b-instruct-v1:0",
                model_kwargs=model_kwargs_claude,
                client=self.runtime_client
            )
            self.logger.info("ChatBedrock LLM initialized.")

            retriever = AmazonKnowledgeBasesRetriever(
                client=self.kb_client,
                knowledge_base_id=os.getenv('KNOWLEDGE_BASE_ID')
            )
            self.logger.info("AmazonKnowledgeBasesRetriever initialized.")

            qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                retriever=retriever,
                return_source_documents=False
            )
            self.logger.info("RetrievalQA chain created. Invoking chain...")

            response = qa_chain(query)
            self.logger.info(f"Chain response received: {response}")

            result = response['result']
            self.logger.info(f"Returning result: {result}")

            return result
            
        except Exception as e:
            self.logger.error(f"Error in query processing: {str(e)}",)
            raise