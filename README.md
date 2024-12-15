# AWS Bedrock Text Document Processor

This project uses AWS Bedrock to process lecture trascriptions using Amazon Nova LLM models. 

## Setup

1. Install the required dependencies:
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

2. Configure AWS credentials:
- Make sure you have AWS credentials configured with access to Bedrock service
- Create a `.env` file with your AWS credentials (if not using AWS CLI configuration):
```
AWS_PROFILE=your_profile
TRANSCRIPTS_PATH=/path/to/your/lectures
```

3. Process the transcriptions:
```bash
source .venv/bin/activate && python3 -m main
```

## Features
- Load and process text documents
- Interact with AWS Bedrock LLM models
- Perform text analysis and knowledge extraction
- Stores strucutred lectures in a JSON format
