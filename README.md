# Sibyl Knowledge Base Processor

**PROPRIETARY AND CONFIDENTIAL**

This repository contains proprietary and confidential information. All rights reserved. 
No part of this codebase may be reproduced, distributed, or transmitted in any form or by any means without the prior written permission of the owner.

 2025 All Rights Reserved

---

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
- Vector-based knowledge retrieval using Chroma DB
- Semantic search for numerology interpretations
- Filtering capabilities for personalized readings

## Project Structure
```
.
├── data/
│   ├── input/          # Raw transcripts and text documents
│   └── output/         # Processed knowledge bases
├── extractors/         # Core processing modules
├── kb/                # Knowledge base management and vector storage
├── prompts/           # LLM prompt templates
└── utils/             # Utility functions
```

## AWS Lambda Layer

The project includes an AWS SAM template to deploy a Lambda layer containing ChromaDB dependency and NumerologyKB classes. This layer can be used in other AWS Lambda functions that need to query the knowledge base.

### Layer Contents

The layer includes:
- ChromaDB library and its dependencies
- KB querier classes:
  - `kb.kb_topic`: Base classes for KB topics
  - `kb.numi_kb`: Base NumerologyKB class
  - `kb.numi_kb_querier`: Querier implementation

### Deployment Instructions

1. Install AWS SAM CLI if you haven't already:
```bash
brew install aws-sam-cli
```

2. Build the layer:
```bash
make build
```

3. Deploy the layer (first time):
```bash
make deploy-guided
```
This will prompt you for:
- Stack name
- AWS Region
- Environment parameter (defaults to "dev")

4. For subsequent deployments:
```bash
AWS_PROFILE=admin make deploy
```
This will use the `admin` AWS profile for deployment.

### Using the Layer

After deployment, the layer will be available with the name `sibyl-layers-kb-${Environment}`. The layer's ARN is exported as `SibylKbLayerArn` and can be referenced in other CloudFormation templates using:

```yaml
!ImportValue SibylKbLayerArn
```

## Dependencies
- boto3 >= 1.28.0
- python-dotenv >= 1.0.0
- openai >= 0.27.4
- pandas >= 2.0.0
- jupyter >= 1.0.0
- chromadb >= 0.4.0

## Usage
The project provides functionality for:
- Processing base energy readings
- Creating knowledge bases from transcripts
- Translating content between Russian and English
- Generating personalized interpretations
- Vector-based storage and retrieval of numerology knowledge
- Semantic search across the knowledge base
- Filtering interpretations based on personal characteristics

Example usage can be found in the respective extractor and knowledge base modules.
