# Sibyl Knowledge Base Processor

A specialized text processing system that transforms Russian numerology lecture transcriptions into structured knowledge bases for the [Sibyl chatbot](https://meet-sibyl.com). The system leverages both AWS Bedrock (with Amazon Nova foundational models) and OpenAI GPT-4 to process and structure numerological concepts, making them suitable for Retrieval-Augmented Generation (RAG) in the chatbot.

## Setup

1. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install the package in development mode:
```bash
pip install -e .
```

3. Configure environment:
Create a `.env` file with the following variables:
```
AWS_PROFILE=your_aws_profile
AWS_DEFAULT_REGION=us-east-1
OPENAI_API_KEY=your_openai_key
PATH_TO_PROJECT=/path/to/this/project
TRANSCRIPTS_PATH=/path/to/transcripts
```

## Features
- Process text documents using AWS Bedrock or OpenAI models
- Create and manage base energy knowledge bases
- Support for both Russian and English translations
- Extract structured information including:
  - Summaries
  - Positive/negative aspects
  - Recommendations
  - Monthly and daily interpretations
- JSON-based storage for processed knowledge

## Project Structure
```
.
├── data/
│   ├── input/          # Raw transcripts and text documents
│   └── output/         # Processed knowledge bases
├── extractors/         # Core processing modules
├── prompts/           # LLM prompt templates
└── utils/             # Utility functions
```

## Dependencies
- boto3 >= 1.28.0
- python-dotenv >= 1.0.0
- openai >= 0.27.4
- pandas >= 2.0.0
- jupyter >= 1.0.0

## Usage
The project provides functionality for:
- Processing base energy readings
- Creating knowledge bases from transcripts
- Translating content between Russian and English
- Generating personalized interpretations

Example usage can be found in the respective extractor modules.
