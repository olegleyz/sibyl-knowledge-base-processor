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


class KBTopic:
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
