from dotenv import load_dotenv
from kb.numi_kb import NumerologyKB, Topics
from kb.kb_topic import KBTopic
import os

class NumerologyKBCreator(NumerologyKB):
    def delete_topic_from_kb(self, topic: KBTopic):
        query = {
            "$and": [
                {KBTopic.TOPIC_KEY: topic.NAME},
                {KBTopic.LANG_KEY: topic.LANG}
            ]
        }
        self.kb.delete(where=query)
    
    def upsert_topic_to_kb(self, topic: KBTopic):
        # First clean previous entries of a topic
        self.delete_topic_from_kb(topic)

        documents = topic.get_documents()
        
        # Add documents to collection
        texts = []
        metadatas = []
        ids = []

        for i, kb_entity in enumerate(documents):
            texts.append(kb_entity.get_text())
            metadatas.append(kb_entity.get_metadata())
            ids.append(kb_entity.get_id())
        
        self.kb.add(
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )


class BaseEnergiesDayKBTopicEn(KBTopic):
    load_dotenv()
    PATH_TO_PROJECT = os.getenv("PATH_TO_PROJECT")
    PATH_TO_KB_DICTS = os.path.join(PATH_TO_PROJECT, "data", "output")
    PATH_TO_KB_DICT = os.path.join(PATH_TO_KB_DICTS, "base_energy_day_kb_single_en.json")
    LANG = "en"
    DESCRIPTION = """The base energy of a day of birth represents the foundational essence of an individual’s character, imprinted at the moment of birth. 
    This energy, derived from the day of birth, shapes key personality traits and life directions. 
    It reveals how a person can best harness their strengths and address their weaknesses, 
    while also highlighting potential challenges and obstacles that may arise on their journey of personal growth.  
    Understanding this base energy fosters deeper self-awareness and insight into others, enhancing relationships, 
    guiding intentional decision-making, and supporting goal achievement. 
    This knowledge serves as a powerful tool for personal development, career progression, relationship harmony, 
    and overall well-being, offering meaningful guidance for optimizing life’s path."""
    NAME = Topics.BASE_ENERGIES_DAY
    

class BaseEnergiesMonthKBTopicEn(KBTopic):
    load_dotenv()
    PATH_TO_PROJECT = os.getenv("PATH_TO_PROJECT")
    PATH_TO_KB_DICTS = os.path.join(PATH_TO_PROJECT, "data", "output")
    PATH_TO_KB_DICT = os.path.join(PATH_TO_KB_DICTS, "base_energy_month_kb_en.json")
    LANG = "en"
    DESCRIPTION = """The base energy of a month of birth reflects the broader life tasks and responsibilities a person inherits, 
    often tied to their family lineage and ancestral legacy. 
    This energy, rooted in the month of birth, reveals the significant challenges and missions a person is meant to address in their lifetime. 
    It serves as a guide to understanding the larger patterns of their journey and the lessons they are destined to learn."""
    NAME = Topics.BASE_ENERGIES_MONTH