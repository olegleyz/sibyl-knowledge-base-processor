import os
import boto3
from dotenv import load_dotenv
import json
import pandas as pd
from enum import Enum
from pathlib import Path
from openai import OpenAI


# Load environment variables
load_dotenv()


class Prompt(Enum):
    RUSSIAN_OUTPUT = """Please provide output in Russian using the Cyrillic alphabet. 
    Ensure all text is readable, without Unicode-escaped characters (e.g., "\u0412" should appear as "В")."""
    JSON_OUTPUT = """Provide all answers in a valid JSON. Total length of JSON should not exceed 1000 tokens. If the generated response should be longer, add "Complete":false into the answer. The requested text is a value to a key "text". If there is also a LLM response, then put it as a value to a key "LLM"."""
    COPYWRITE = """Note that I own the lecture text, so you should not be concerned about the copyright issues."""
    UNMODIFIED_TEXT = """I only need the original text from the lecture, without any translation, modification, summary, or introduction. Don't shorten or rephrase the text, it's important to provide original text without modifications. Ensure the text is not longer than 5120 characters."""


class Model(Enum):
    NOVA_MICRO = "amazon.nova-micro-v1:0"
    NOVA_LITE = "us.amazon.nova-lite-v1:0"
    NOVA_PRO = "amazon.nova-pro-v1:0"
    HAIKU_35 = "anthropic.claude-3-5-haiku-20241022-v1:0"
    HAIKU_3 = "anthropic.claude-3-haiku-20240307-v1:0"
    SONNET_35v2 = "anthropic.claude-3-5-sonnet-20241022-v2:0"
    SONNET_35 = "anthropic.claude-3-5-sonnet-20240620-v1:0"


class LectureKnowledgeExtractor:
    def __init__(self, region="us-east-1"):
        self.bedrock_client = boto3.client(
            service_name='bedrock-runtime',
            region_name=region)

    def extract_doc_structure(self, path_to_doc):
        prompt = """Given transcript of a numerology lecture in russian language describes a numerological topic - a calculated number.
        This calculated number will contain variations. Capture a topic name in russian and variations -usually these are the numbers from 1 to 8 or 1 to 22, etc. 
        Return output in a json format following the template:
        {
            "topic": "topic name",
            "variations": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22"]
        }   
        """

        return self.prompt_doc(prompt, path_to_doc)
    
    def extract_chapter_summary(self, chapter_name, path_to_doc):
        prompt = f"""Please provide the concise summary of a lecture "{chapter_name}".
        Rephrase the summary to avoid details of a course but focus on the summary of "{chapter_name}" itself: what information could it give to a person, how it could be used or help.
        {Prompt.RUSSIAN_OUTPUT.value} {Prompt.COPYWRITE.value} {Prompt.JSON_OUTPUT.value}"""
        
        return self.prompt_doc(prompt, path_to_doc)["text"]

    def extract_chapter_text(self, chapter_name, variation_number, variations, path_to_doc):
        prompt = f"""Прикрепленный документ содержит нумерологическую лекцию о "{chapter_name}", алгоритме расчета и текстовые интерпретации каждой возможной цифры кода души ({", ".join(variations)}).
        Максимально подробно и близко к тесту, не сокращаю, но и не добавляя от себя, напиши интерпретацию {chapter_name} номер {variation_number}. 
        Ответ предоставь в формате JSON, в качестве значения для ключа "text", полностью на русском языке."""

        return self.prompt_doc(prompt, path_to_doc)["text"]

    def get_interpretation_structure(self, chapter_name, variation_number, variations, output):
        prompt = f"""Это json, содержащий текстовые харакетриситики {len(variations)} вариантов {chapter_name}: {output}. 
        Я бы хотел его переформатировать таким образом, чтобы описание каждого из 12 {chapter_name} использовало единообразную структуру. 
        Сгенерируй список из 4 заголовков, которые содержали бы не больше одного уровня иерархии и которые можно было бы использовать для всех {len(variations)} вариантов {chapter_name}. 
        Не изменяй исходный текст. Ответ должн содержать только новые заголовки в формате json. Например, {"text": ["подзаголовок1", "подзаголовок2","подзаголовок3", "подзаголовок4"]}."""
        return self.prompt_text(prompt)["text"]


    def rephrase_interpretation(self, chapter_name, variation_number, text):
        prompt = f"""The provided below text is a numerology interpretation of the {chapter_name} {variation_number}. Rephrase this text so that the interpretation is clear and easy to read and understand. 
        Without revealing that this is an interpretation, the topic name or the specific variation number, provide a complete and detailed explanation of the meaning conveyed by {chapter_name} {variation_number}.
        {Prompt.RUSSIAN_OUTPUT.value} {Prompt.JSON_OUTPUT.value} Here is the given text: {text}"""
        return self.prompt_text(prompt)["text"]
    
    def extract_lecture_knowledge(self, topic_name, variation_list, path_to_doc='/Users/olegleyzerov/Documents/private/coding/numi_all/elena_out/1_intro_childhood.txt'):
        print(f"Processing {topic_name}...")
        print("Extracting summary...")
        summary = self.extract_chapter_summary(topic_name, path_to_doc)

        variations_dict = {}
        errors = {}

        for var in variation_list:    
            print(f"Extracting {topic_name} {var}...")
            try: 
                interpretation = self.extract_chapter_text(topic_name, var, variations_dict, path_to_doc)
                variations_dict[var] = interpretation
            except Exception as e:
                print(f"Error while extracting chapter text for {topic_name} {var}: {e}")
                errors[var] = str(e)

        return {
            "summary": summary,
            "variation_options": variation_list,
            "variations": variations_dict,
            "errors": errors      
        } 

    def prompt_doc(self, prompt, path_to_doc, model_id = Model.NOVA_LITE.value):
        p = Path(path_to_doc)
        if not p.exists():
            raise FileNotFoundError(f"The file at '{path_to_doc}' does not exist.")

        with open(path_to_doc, "rb") as file:
            doc_bytes = file.read()

        file_format = p.suffix.lstrip('.')
        if file_format not in ("txt"):
            raise ValueError(f"Given file format at '{path_to_doc}' is not supported.")
    
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "document": {
                            "format": file_format,
                            "name": "DocumentMessages",
                            "source": {
                                "bytes": doc_bytes
                            }
                        }
                    },
                    {
                        "text": prompt
                    }
                ]
            }
        ]

        max_retries = 3
        retry = 0
        while retry < max_retries:
            try:
                model_response = self.bedrock_client.converse(modelId=model_id, messages=messages, inferenceConfig={"maxTokens": 5120, "topP": 0.1, "temperature": 0.3})
                output = model_response['output']['message']['content'][0]['text']
                return self.process_llm_output_json(output)
            except Exception as e:
                # print(f"Error while prompting document. {e}. Retrying...")
                retry += 1
                
        raise ValueError(f"Error while prompting document with the prompt {prompt}.")
        
    def prompt_text(self, prompt, model_id=Model.NOVA_LITE.value):
        messages = [
            {
                "role": "user", 
                "content": [
                    {
                        "text": prompt
                    }
                ]
            },
        ]
        return self.chat(message=messages, model_id=model_id)

    def chat(self, messages, model_id=Model.NOVA_LITE.value):
        max_retries = 3
        retry = 0
        e = None
        output=None
        while retry < max_retries:
            try:
                output = self.invoke_llm(model_id=model_id, messages=messages)
                
                # print(f"raw output: {output}")
                if output.startswith("```json"):
                    output = output[8:-3]
                output = output.replace('\n', '')
                # print(output)
                return self.process_llm_output_json(output)
            except Exception as e1:
                # print(f"Error while prompting text. {e}. Retrying...")
                e = e1
                retry += 1
                
        # return output
        raise ValueError(f"Error: {e}. Output: {output}")

    def invoke_llm(self, model_id, messages):
        self.bedrock_client.converse(
            modelId=model_id,
            messages=messages,
            # inferenceConfig={"maxTokens": 5120, "topP": 0.1, "temperature": 0.3}
        )
        output = model_response['output']['message']['content'][0]['text']
        return output


    @staticmethod
    def process_llm_output_json(output):
        result = output
        if output.startswith("```json"):
            result = output[8:-3]
        result = result.replace('\n', '')
        try:
            result = json.loads(result)
            return result
        except:
            # print_pretty_text(f"Here is how the string look like before converting to json: {result}")
            # return result
            raise ValueError(f"Error converting LLM output to json: {result}")
    
    
class OpenAIExtractor(LectureKnowledgeExtractor):
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def prompt_text(self, prompt, model_id="ignored"):
        model_id = "gpt-4o-mini"
        messages = [
            {
                "role": "user", 
                "content": prompt
            }
        ]
        return self.chat(messages=messages, model_id=model_id)
    
    def invoke_llm(self, model_id, messages):
        completion = self.client.chat.completions.create(
            model=model_id,
            store=True,
            messages=messages
        )
        output = completion.choices[0].message.content
        return output
        