from kb.kb_topic import KBTopic
from kb.numi_kb import NumerologyKB, Topics


class NumerologyKBQuerier(NumerologyKB):
    def query_kb(self, base_energy_day, base_energy_month, prompt=""):
        query = self._get_query(base_energy_day, base_energy_month)
        return self.kb.query(
            query_texts=[prompt],
            where=query,
            include=["documents", "distances"]
        )

    @staticmethod
    def _get_query(base_energy_day, base_energy_month):
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
                            {KBTopic.TOPIC_KEY: topic},
                            {KBTopic.TYPE_KEY: KBTopic.DESCRIPTION_KEY}
                        ]
                    },
                    {
                        "$and": [
                            {KBTopic.TOPIC_KEY: topic},
                            {KBTopic.NUMBER_KEY: param_map[topic]}
                        ]
                    }
                ]
            }
            query["$or"].append(sub_query)
        return query