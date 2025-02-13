import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
import os,sys
from core.split_main import prepare_spacy_model
from config_utils import *
from rich import print
import pandas as pd

def analyze_connectors(doc, token):
    """
    Analyze whether a token is a connector that should trigger a sentence split.
    
    Processing logic and order:
     1. Check if the token is one of the target connectors based on the language.
     2. For 'that' (English), check if it's part of a contraction (e.g., that's, that'll).
     3. For all connectors, check if they function as a specific dependency of a verb or noun.
     4. Default to splitting for certain connectors if no other conditions are met.
     5. For coordinating conjunctions, check if they connect two independent clauses.
    """
    lang = doc.lang_
    if lang == "en":
        connectors = ["that", "which", "where", "when", "because", "but", "and", "or"]
        mark_dep = "mark"
        det_pron_deps = ["det", "pron"]
        verb_pos = "VERB"
        noun_pos = ["NOUN", "PROPN"]
    elif lang == "zh":
        connectors = ["因为", "所以", "但是", "而且", "虽然", "如果", "即使", "尽管"]
        mark_dep = "mark"
        det_pron_deps = ["det", "pron"]
        verb_pos = "VERB"
        noun_pos = ["NOUN", "PROPN"]
    elif lang == "ja":
        connectors = ["けれども", "しかし", "だから", "それで", "ので", "のに", "ため"]
        mark_dep = "mark"
        det_pron_deps = ["case"]
        verb_pos = "VERB"
        noun_pos = ["NOUN", "PROPN"]
    elif lang == "fr":
        connectors = ["que", "qui", "où", "quand", "parce que", "mais", "et", "ou"]
        mark_dep = "mark"
        det_pron_deps = ["det", "pron"]
        verb_pos = "VERB"
        noun_pos = ["NOUN", "PROPN"]
    elif lang == "ru":
        connectors = ["что", "который", "где", "когда", "потому что", "но", "и", "или"] 
        mark_dep = "mark"
        det_pron_deps = ["det"]
        verb_pos = "VERB"
        noun_pos = ["NOUN", "PROPN"]
    elif lang == "es":
        connectors = ["que", "cual", "donde", "cuando", "porque", "pero", "y", "o"]
        mark_dep = "mark"
        det_pron_deps = ["det", "pron"]
        verb_pos = "VERB"
        noun_pos = ["NOUN", "PROPN"]
    elif lang == "de":
        connectors = ["dass", "welche", "wo", "wann", "weil", "aber", "und", "oder"]
        mark_dep = "mark"
        det_pron_deps = ["det", "pron"]
        verb_pos = "VERB"
        noun_pos = ["NOUN", "PROPN"]
    elif lang == "it":
        connectors = ["che", "quale", "dove", "quando", "perché", "ma", "e", "o"]
        mark_dep = "mark"
        det_pron_deps = ["det", "pron"]
        verb_pos = "VERB"
        noun_pos = ["NOUN", "PROPN"]
    else:
        return False, False
    
    if token.text.lower() not in connectors:
        return False, False
    
    if lang == "en" and token.text.lower() == "that":
        if token.dep_ == mark_dep and token.head.pos_ == verb_pos:
            return True, False
        else:
            return False, False
    elif token.dep_ in det_pron_deps and token.head.pos_ in noun_pos:
        return False, False
    else:
        return True, False

def split_by_connectors(text, context_words=5, nlp=None):
    doc = nlp(text)
    sentences = [doc.text]  # init
    
    while True:
        # Handle each task with a single cut
        # avoiding the fragmentation of a sentence into multiple parts at the same time.
        split_occurred = False
        new_sentences = []
        
        for sent in sentences:
            doc = nlp(sent)
            start = 0
            
            for i, token in enumerate(doc):
                split_before, _ = analyze_connectors(doc, token)
                
                if i + 1 < len(doc) and doc[i + 1].text in ["'s", "'re", "'ve", "'ll", "'d"]:
                    continue
                
                left_words = doc[max(0, token.i - context_words):token.i]
                right_words = doc[token.i+1:min(len(doc), token.i + context_words + 1)]
                
                left_words = [word.text for word in left_words if not word.is_punct]
                right_words = [word.text for word in right_words if not word.is_punct]
                
                if len(left_words) >= context_words and len(right_words) >= context_words and split_before:
                    print(f"[yellow]✂️  Split before '{token.text}': {' '.join(left_words)}| {token.text} {' '.join(right_words)}[/yellow]")
                    new_sentences.append(doc[start:token.i].text.strip())
                    start = token.i
                    split_occurred = True
                    break
            
            if start < len(doc):
                new_sentences.append(doc[start:].text.strip())
        
        if not split_occurred:
            break
        
        sentences = new_sentences
    
    return sentences

def split_sentences_main(nlp):
    # Read input sentences
    df = pd.read_csv(TRANSCRIPTION_SENT_PATH)
    
    all_split_sentences = []
    # Process each input sentence
    for sentence in df['text']:
        split_sentences = split_by_connectors(sentence.strip(), nlp = nlp)
        all_split_sentences.extend(split_sentences)
    
    # output to sentence_splitbyconnector.txt
    with open(os.getcwd() + "\\t.txt", "w+", encoding="utf-8") as output_file:
        for sentence in all_split_sentences:
            output_file.write(sentence + "\n")
        # do not add a newline at the end of the file
        output_file.seek(output_file.tell() - 1, os.SEEK_SET)
        output_file.truncate()
    
    print("[green]💾 Sentences split by connectors saved to →  `sentence_splitbyconnector.txt`[/green]")

if __name__ == "__main__":
    nlp = prepare_spacy_model('en')
    split_sentences_main(nlp)
