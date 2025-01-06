import chromadb


class Topics:
    BASE_ENERGIES_DAY = "BaseEnergiesDay"
    BASE_ENERGIES_MONTH = "BaseEnergiesMonth"
    TOPICS = (BASE_ENERGIES_DAY, BASE_ENERGIES_MONTH)


class NumerologyKB:
    KB_NAME = "numerology"
    KB_DESCRIPTION = "Numerology Knowledge Base"
    PATH_TO_KB = "../vector_db"
    
    def __init__(self):
        self.kb_client = None
        self.create_kb_client()
        self.kb = self.get_or_create_kb()

    def create_kb_client(self):
        if not self.kb_client:
            self.kb_client = chromadb.PersistentClient(path=self.PATH_TO_KB)

    def get_or_create_kb(self):
        existing_collections = self.kb_client.list_collections()

        if self.KB_NAME in existing_collections:
            return self.kb_client.get_collection(self.KB_NAME)
        return self.kb_client.create_collection(
            name=self.KB_NAME,
            metadata={"description": self.KB_DESCRIPTION}
        )
