from dotenv import load_dotenv
import os
import json


class KBEntity:
    def __init__(self, doc):
        self.doc = doc
    
    def get_text(self):
        return self.doc[KBTopic.TEXT_KEY]

    def get_metadata(self):
        return self.doc[KBTopic.METADATA_KEY]

    def get_id(self):
        return self.doc[KBTopic.ID_KEY]

class Topics:
    BASE_ENERGIES_DAY = "BaseEnergiesDay"
    BASE_ENERGIES_MONTH = "BaseEnergiesMonth"
    TOPICS = (BASE_ENERGIES_DAY, BASE_ENERGIES_MONTH)

class KBTopic:
    load_dotenv()
    PATH_TO_PROJECT = os.getenv("PATH_TO_PROJECT")
    PATH_TO_KB_DICTS = os.path.join(PATH_TO_PROJECT, "data", "output")
    DESCRIPTION_KEY = "description"
    INTERPRETATION_KEY = "interpretation"
    TEXT_KEY = "text"
    METADATA_KEY = "metadata"
    TOPIC_KEY = "topic"
    SUBSECTION_KEY = "subsection"
    NUMBER_KEY = "number"
    TYPE_KEY = "type"
    ID_KEY = "id"
    LANG_KEY = "lang"


    def __init__(self):
        self.kb_dict = self.get_kb_dict()
        self.doc_count = 0

    def get_kb_dict(self):
        with open(self.PATH_TO_KB_DICT, "r") as f:
            return json.load(f)

    def get_documents(self):
        # Create documents for vector store
        documents = []
        
        # Append a topic description document        
        self.append_doc(documents, {
            KBTopic.TEXT_KEY: self.DESCRIPTION,
            KBTopic.METADATA_KEY: {
                KBTopic.TOPIC_KEY: self.NAME,
                KBTopic.TYPE_KEY: KBTopic.DESCRIPTION_KEY,
                KBTopic.LANG_KEY: self.LANG
            },
            KBTopic.ID_KEY: self.get_id(subsection=KBTopic.DESCRIPTION_KEY)
        })

        # Append individual value interpretations
        for var in self.kb_dict:
            for group in self.kb_dict[var]:
                self.append_doc(documents, {
                    KBTopic.TEXT_KEY: self.kb_dict[var][group],
                    KBTopic.METADATA_KEY: {
                       KBTopic.TOPIC_KEY: self.NAME,
                        KBTopic.SUBSECTION_KEY: group,
                        KBTopic.NUMBER_KEY: int(var),
                        KBTopic.TYPE_KEY: KBTopic.INTERPRETATION_KEY,
                        KBTopic.LANG_KEY: self.LANG
                    },
                    KBTopic.ID_KEY: self.get_id(subsection=group, var=int(var))
                })

        return documents

    def get_id(self, subsection, var=None):
        result = f"{self.LANG}#{self.NAME}#{subsection}"
        if var:
            result += f"#{var}"
        return result

    def append_doc(self, doc_list, doc):
        doc_list.append(KBEntity(doc))
        self.doc_count += 1


class BaseEnergiesDayKBTopicEn(KBTopic):
    PATH_TO_KB_DICT = os.path.join(KBTopic.PATH_TO_KB_DICTS, "base_energy_day_kb_single_en.json")
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
    PATH_TO_KB_DICT = os.path.join(KBTopic.PATH_TO_KB_DICTS, "base_energy_month_kb_en.json")
    LANG = "en"
    DESCRIPTION = """The base energy of a month of birth reflects the broader life tasks and responsibilities a person inherits, 
    often tied to their family lineage and ancestral legacy. 
    This energy, rooted in the month of birth, reveals the significant challenges and missions a person is meant to address in their lifetime. 
    It serves as a guide to understanding the larger patterns of their journey and the lessons they are destined to learn."""
    NAME = Topics.BASE_ENERGIES_MONTH
