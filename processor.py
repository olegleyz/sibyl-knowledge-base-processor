import glob
import json
import os

from extractor import LectureKnowledgeExtractor

class TranscriptProcessor:
    def __init__(self):
        self.transcripts_dir = os.getenv("TRANSCRIPTS_PATH")
        if not self.transcripts_dir:
            raise ValueError("TRANSCRIPTS_PATH environment variable is not set.")
        self.extractor = LectureKnowledgeExtractor()
        self.lectures = self.get_lectures_structure()

    def get_lectures_structure(self):
        lectures = {}
        input_files = glob.glob(os.path.join(self.transcripts_dir, "*.txt"))
        for path_to_doc in input_files:
            lecture = self.extractor.extract_doc_structure(path_to_doc)
            if "topic" in lecture and "variations" in lecture:
                lectures[lecture["topic"]] = {"path_to_doc": path_to_doc, "variations": lecture["variations"]}
            else:
                raise ValueError(f"Failure during extracting a structure of lecture {path_to_doc}. Unexpected structure.")
        return lectures

    @staticmethod
    def save_to_json(data_dict, filename):    
        # Ensure output directory exists
        output_dir = 'data/output'
        os.makedirs(output_dir, exist_ok=True)
        
        # Create full file path
        file_path = os.path.join(output_dir, filename)
        
        # Save dictionary to JSON file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data_dict, f, indent=4, ensure_ascii=False)
        print(f"Dictionary saved to {file_path}")

    def process_lectures(self):
        for lecture in self.lectures:
            lecture_knowledge = self.extractor.extract_lecture_knowledge(lecture, self.lectures[lecture]["variations"], self.lectures[lecture]["path_to_doc"])
            self.save_to_json({lecture: lecture_knowledge}, f"{lecture}.json")

if __name__ == "__main__":
    processor = TranscriptProcessor()
    processor.process_lectures()
