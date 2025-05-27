import os


PAGE_CONFIG = {
    "page_title": "Agentic RAG Application",
    "page_icon": "🤖",
    "layout": "wide"
}


AWS_CONFIG = {
    "region": os.getenv("AWS_REGION", "eu-central-1"),
    "s3_bucket": os.getenv("S3_BUCKET", "your-bucket-name"),
    "knowledge_base_id": os.getenv("KNOWLEDGE_BASE_ID", "YOUR_KNOWLEDGE_BASE_ID")
}


UPLOAD_CONFIG = {
    "allowed_types": [
        'pdf', 'txt', 'docx', 'doc', 'md', 'html', 'csv', 'xls', 'xlsx'
    ],
    "multiple_files": True
}