import utils.config_utils as cfg
import gpt_openai
import gpt_prompts
import os
import json_repair
from typing import List

def chunk_text(text: str, max_tokens: int = 3000) -> List[str]:
    """Split text into chunks that won't exceed token limit."""
    sentences = text.split('. ')
    chunks = []
    current_chunk = []
    current_length = 0
    
    for sentence in sentences:
        # Rough estimate: 1 token ≈ 4 characters
        sentence_tokens = len(sentence) // 4
        if current_length + sentence_tokens > max_tokens:
            chunks.append('. '.join(current_chunk) + '.')
            current_chunk = [sentence]
            current_length = sentence_tokens
        else:
            current_chunk.append(sentence)
            current_length += sentence_tokens
    
    if current_chunk:
        chunks.append('. '.join(current_chunk) + '.')
    return chunks

def start_summary():
    with open(cfg.TRANSCRIPTION_SENT_PATH, 'r', encoding='utf-8') as f:
        text = f.read()
        
        # Split into manageable chunks
        chunks = chunk_text(text)
        
        # Get summary for each chunk
        chunk_summaries = []
        for chunk in chunks:
            tgt = cfg.get_config_value('translator.target')
            summary = gpt_openai.ask_gpt(chunk, gpt_prompts.get_summary_prompt(tgt))
            if summary == None:
                print('error when generating summary')
                chunk_summaries.append("Error None")
                return
            summary = json_repair.repair_json(summary)
            chunk_summaries.append(summary)

        # If we have multiple chunks, combine them with a final summary
        if len(chunk_summaries) > 1:
            combined_summary = gpt_openai.ask_gpt(
                "\n".join(chunk_summaries),
                gpt_prompts.get_combine_summaries_prompt()
            )
            final_summary = json_repair.repair_json(combined_summary)
        else:
            final_summary = chunk_summaries[0]

        with open(cfg.SUMMARY_PATH, 'w', encoding='utf-8') as f:
            f.write(final_summary)

if __name__ == '__main__':
    start_summary()