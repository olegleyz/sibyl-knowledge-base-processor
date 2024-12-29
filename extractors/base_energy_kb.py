import ast
from dotenv import load_dotenv
import json
import os

from prompts import base_energy_kb_prompts as base_energy_prompts 
from .extractor import OpenAIExtractor, LectureKnowledgeExtractor
from utils.utils import print_json_pretty

class BaseEnergyKB:
    load_dotenv()
    PATH_TO_PROJECT = os.getenv("PATH_TO_PROJECT")
    PATH_TO_TRANSCRIPT = os.path.join(PATH_TO_PROJECT, "data", "input", "base_energy_transcript.json")
    PATH_TO_MONTH_TR = os.path.join(PATH_TO_PROJECT, "data", "input", "base_energies_month_rus.json")
    PATH_TO_KB = os.path.join(PATH_TO_PROJECT, "data", "output", "base_energy_kb.json")
    PATH_TO_MONTH_KB = os.path.join(PATH_TO_PROJECT, "data", "output", "base_energy_month_kb.json")

    PATH_TO_BE_DAY_KB_EN = os.path.join("data", "output", "base_energy_day_kb_en.json")
    PATH_TO_BE_DAY_KB_SINGLE_EN = os.path.join("data", "output", "base_energy_day_kb_single_en.json")
    PATH_TO_BE_MONTH_KB_EN = os.path.join("data", "output", "base_energy_month_kb_en.json")

    def __init__(self, use_openai=False):
        if use_openai:
            self.extr = OpenAIExtractor()
        else:
            self.extr = LectureKnowledgeExtractor(region="us-east-1")
        self.tr = self.load_transcript()
        self.base_energy_day_kb = self.load_be_day_kb()
        self.base_energy_month_kb = self.load_be_month_kb()

    def load_be_month_kb(self, lang="ru"):
        path_to_kb = self.PATH_TO_MONTH_KB
        if lang == "en":
            path_to_kb = self.PATH_TO_BE_MONTH_KB_EN
        with open(path_to_kb, "r") as f:
            tr = json.load(f)
        return tr
    
    def load_be_day_kb(self, lang="ru"):
        path_to_kb = self.PATH_TO_KB
        if lang == "en":
            path_to_kb = self.PATH_TO_BE_DAY_KB_EN

        with open(path_to_kb, "r") as f:
            tr = json.load(f)
        tr_json = {}
        for el in tr:
            el_t = ast.literal_eval(el)
            if type(el_t) == int:
                el_t = (el_t,)
            tr_json[el_t] = tr[el]
        return tr_json

    def load_be_day_single_kb(self, lang="en"):
        path_to_kb = None
        if lang == "en":
            path_to_kb = self.PATH_TO_BE_DAY_KB_SINGLE_EN
        else: 
            return None
        with open(path_to_kb, "r") as f:
            tr = json.load(f)
        return tr
    
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
    
    def get_kb(self, demo=False, verbose=False):
        kb = {}
        for el in self.tr:
            print(f"Day(s): {el}")
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
                print_json_pretty(kb[str(el)])
            if demo:
                break
        return kb 

    def get_month_kb(self, demo=False, verbose=False):
        kb = {}
        with open(self.PATH_TO_MONTH_TR, "r") as f:
            month_tr = json.load(f)
        for el in month_tr:
            print(f"Month: {el}")
            prompt = base_energy_prompts.get_be_month_prompt1(month_tr[el])
            result = self.extr.prompt_text(prompt)
            kb[el] = {
                "summary": result["text"]["summary"],
                "recommendation": result["text"]["recommendation"]
            }
            if verbose:
                print_json_pretty(kb[el])
            if demo:
                break
        return kb

    def get_reading(self, first_name, day_of_birth, month_of_birth, age, sex, lang, verbose=False):
        base_energy_day_kb = self.load_be_day_kb(lang=lang)
        base_energy_month_kb = self.load_be_month_kb(lang=lang)

        be_interpr = self.get_be_interpretation(
            day_of_birth=day_of_birth,
            month_of_birth=month_of_birth, 
            base_energy_day_kb=base_energy_day_kb, 
            base_energy_month_kb=base_energy_month_kb) 

        prompt = base_energy_prompts.get_base_energy_day_reading(be_interpr["summary"], be_interpr["positive"], be_interpr["negative"], be_interpr["recommendation"], first_name, sex, age, lang=lang)
        result = self.extr.prompt_text(prompt)
        if verbose:
            print_json_pretty(result, width=150)
    
        return result

    def translate_be_day(self, demo=False, verbose=False):
        kb_en = {}
        for el in self.base_energy_day_kb:
            if el not in kb_en:
                kb_en[el] = {}
            for ch in self.base_energy_day_kb[el]:
                text_ru = self.base_energy_day_kb[el][ch]
                prompt = base_energy_prompts.translate_rus_to_en(text_ru)
                text_en = self.extr.prompt_text(prompt)["text"]
                kb_en[el][ch] = text_en
            if demo:
                break 

        result = {}
        for key in kb_en:
            result[str(key)] = kb_en[key]
        
        if verbose:
            print_json_pretty(result)

        if not demo:
            self.save_kb(result, self.PATH_TO_BE_DAY_KB_EN)

    def translate_be_month(self, verbose=False):
        kb_en = {}
        for el in self.base_energy_month_kb:
            print(el)
            if el not in kb_en:
                kb_en[el] = {}
            for ch in self.base_energy_month_kb[el]:
                text_ru = self.base_energy_month_kb[el][ch]
                prompt = base_energy_prompts.translate_rus_to_en(text_ru)
                text_en = self.extr.prompt_text(prompt)["text"]
                kb_en[el][ch] = text_en
            if verbose:
                print_json_pretty(kb_en[el])

        self.save_kb(kb_en, self.PATH_TO_BE_MONTH_KB_EN)

    def get_combined_be_day(self, lang="en", verbose=False):
        result = {}
        base_energy_day_kb = self.load_be_day_kb(lang=lang)
        for el in base_energy_day_kb:
            temp = base_energy_day_kb[el]
            for n in el:
                if n not in result:
                    result[n] = {}
                    for el in temp:
                        result[n][el] = []
                for el in temp:
                    result[n][el].append(temp[el])    
        if verbose:
            print_json_pretty(result)
        for el in result:
            for ch in result[el]:
                result[el][ch] = " ".join(result[el][ch])
        self.save_kb(result, self.PATH_TO_BE_DAY_KB_SINGLE_EN)
    
    @staticmethod
    def save_kb(kb, path_to_file):
        with open(path_to_file, "w", encoding="utf-8") as json_file:
            json.dump(kb, json_file, ensure_ascii=False, indent=4)
    
    @staticmethod
    def get_be_interpretation(day_of_birth, month_of_birth, base_energy_day_kb, base_energy_month_kb):
        interpretations = {}
        
        for el in base_energy_day_kb:
            if day_of_birth in el:
                interpr = base_energy_day_kb[el]
                for key in interpr:
                    if key not in interpretations:
                        interpretations[key] = []
                    interpretations[key].append(interpr[key])
        be_m = base_energy_month_kb[str(month_of_birth)]
        for key in be_m:
            if key not in interpretations:
                interpretations[key] = []
            interpretations[key].append(be_m[key])
        
        for key in interpretations:
            interpretations[key] = ". ".join(interpretations[key])
            
        return interpretations
