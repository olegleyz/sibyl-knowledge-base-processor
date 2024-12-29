import chromadb
from kb.kb_topic import KBTopic, Topics

class NumerologyKB:
    KB_NAME = "numerology"
    KB_DESCRIPTION = "Numerology Knowledge Base"
    PATH_TO_KB = "../vector_db"
    
    def __init__(self):
        self.kb_client = self.get_kb_client()
        self.kb = self.get_or_create_kb()

    def get_kb_client(self):
        return chromadb.PersistentClient(path=self.PATH_TO_KB)

    def get_or_create_kb(self):
        existing_collections = {col.name for col in self.kb_client.list_collections()}

        if self.KB_NAME in existing_collections:
            return self.kb_client.get_collection(self.KB_NAME)
        return self.kb_client.create_collection(
            name=self.KB_NAME,
            metadata={"description": self.KB_DESCRIPTION}
        )

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

    def query_kb(self, base_energy_day, base_energy_month, prompt=""):
        query = self.get_query(base_energy_day, base_energy_month)
        
        return self.kb.query(
            query_texts = [prompt],
            where=query,
            include=["documents", "distances"]
        )

    @staticmethod
    def get_query(base_energy_day, base_energy_month):
        param_map = {
            Topics.BASE_ENERGIES_DAY: base_energy_day,
            Topics.BASE_ENERGIES_MONTH: base_energy_month
        }
        query = {"$or": []}
        for topic in Topics.TOPICS:
            sub_query = {
                "$or": [
                    {
                        "$and": [
                            {
                                KBTopic.TOPIC_KEY: topic
                            },
                            {
                                KBTopic.TYPE_KEY: KBTopic.DESCRIPTION_KEY
                            }
                        ]
                    },
                    {
                        "$and": [
                            {
                                KBTopic.TOPIC_KEY: topic
                            },
                            {
                                KBTopic.NUMBER_KEY: param_map[topic]
                            }
                        ]
                    }
                ]
            }
            query["$or"].append(sub_query)
        return query
