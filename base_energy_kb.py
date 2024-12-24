import ast
import json
import os

from prompts import base_energy_kb_prompts as base_energy_prompts 
from extractor import OpenAIExtractor, LectureKnowledgeExtractor
from utils import print_json_pretty

class BaseEnergyKB:
    PATH_TO_TRANSCRIPT = os.path.join("data", "input", "base_energy_transcript.json")
    PATH_TO_MONTH_TR = os.path.join("data", "input", "base_energies_month_rus.json")
    PATH_TO_KB = os.path.join("data", "output", "base_energy_kb.json")
    PATH_TO_MONTH_KB = os.path.join("data", "output", "base_energy_month_kb.json")

    def __init__(self, use_openai=False):
        if use_openai:
            self.extr = OpenAIExtractor()
        else:
            self.extr = LectureKnowledgeExtractor(region="us-east-1")
        self.tr = self.load_transcript()
        

    def load_transcript(self):
        with open(self.PATH_TO_TRANSCRIPT, "r") as f:
            tr = json.load(f)
        tr_json = {}
        for el in tr:
            tr_json[ast.literal_eval(el)] = tr[el]
        return tr_json
        
    
    def get_neg_multi_step(self, transcription, verbose=False):
        prompt1 = base_energy_prompts.get_neg_prompt_step1(transcription)
        result = self.extr.prompt_text(prompt1)
        if verbose:
            print_json_pretty(result, width=150)

        prompt2 = base_energy_prompts.get_neg_prompt_step2(result["text"])
        result = self.extr.prompt_text(prompt2)
        if verbose:
            print_json_pretty(result, width=150)

        prompt3 = base_energy_prompts.proofread_rus(result["text"])
        result = self.extr.prompt_text(prompt3)
        if verbose:
            print_json_pretty(result, width=150)

        return result
    
    def get_pos_multi_step(self, transcription, verbose=False):
        prompt1 = base_energy_prompts.get_pos_prompt_step1(transcription)
        result = self.extr.prompt_text(prompt1)
        if verbose:
            print_json_pretty(result, width=150)

        prompt2 = base_energy_prompts.get_pos_prompt_step2(result["text"])
        result = self.extr.prompt_text(prompt2)
        if verbose:
            print_json_pretty(result, width=150)

        prompt3 = base_energy_prompts.proofread_rus(result["text"])
        result = self.extr.prompt_text(prompt3)
        if verbose:
            print_json_pretty(result, width=150)

        return result
    
    def get_summary(self, transcription, verbose=False):
        prompt = base_energy_prompts.get_summary_prompt(transcription)
        result = self.extr.prompt_text(prompt)
        if verbose:
            print_json_pretty(result, width=150)
            
        proofread_prompt = base_energy_prompts.proofread_rus(result["text"])
        result = self.extr.prompt_text(proofread_prompt)
        if verbose:
            print_json_pretty(result, width=150)

        return result

    def get_recommendation(self, transcription, verbose=False):
        prompt = base_energy_prompts.get_recommendation(transcription)
        result = self.extr.prompt_text(prompt)
        if verbose: 
            print_json_pretty(result, width=150)
        
        proofread_prompt = base_energy_prompts.proofread_rus(result["text"])
        result = self.extr.prompt_text(proofread_prompt)
        if verbose:
            print_json_pretty(result, width=150)
        
        return result

    
    def get_kb(self, verbose=False):
        kb = {}
        for el in self.tr:
            print(el)
            summary = self.get_summary(self.tr[el])["text"]
            pos = self.get_pos_multi_step(transcription=self.tr[el])["text"]
            neg = self.get_neg_multi_step(transcription=self.tr[el])["text"]
            recommendation = self.get_recommendation(transcription=self.tr[el])["text"]
            kb[str(el)] = {
                "summary": summary,
                "positive": pos,
                "negative": neg,
                "recommendation": recommendation
            }
            if verbose:
                print_json_pretty(kb[el])
        return kb 

    def get_month_kb(self, verbose=False):
        kb = {}
        with open(self.PATH_TO_MONTH_TR, "r") as f:
            month_tr = json.load(f)
        for el in month_tr:
            print(el)
            proofread_prompt = base_energy_prompts.proofread_rus(month_tr[el])
            result = self.extr.prompt_text(proofread_prompt)
            if verbose:
                print_json_pretty(result, width=150)
            kb[el] = result["text"]
            if verbose:
                print_json_pretty(kb[el])
        return kb

    def save_kb(self, kb, path_to_file):
        with open(path_to_file, "w", encoding="utf-8") as json_file:
            json.dump(kb, json_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    bekb = BaseEnergyKB(use_openai=True)
    bekb_kb = bekb.get_month_kb()
    bekb.save_kb(kb=bekb_kb, path_to_file=bekb.PATH_TO_MONTH_KB)
