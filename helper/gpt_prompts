

def get_split_prompt(sentence: str, num_parts: int, word_limit: int):
    split_prompt = f"""
### Role
You are a professional Netflix subtitle splitter.

### Task
Split the given subtitle text into {num_parts} parts, each less than {word_limit} words.

### Instructions
1. Maintain sentence meaning coherence according to Netflix subtitle standards
2. Keep parts roughly equal in length (minimum 3 words each)
3. Split at natural points like punctuation marks or conjunctions
4. If provided text is repeated words, simply split at the middle of the repeated words.

### Output Format in JSON
{{
    "analysis": "Brief analysis of the text structure",
    "split": "Complete sentence with [br] tags at split positions"
}}

### Given Text
<split_this_sentence>
{sentence}
</split_this_sentence>

### Your Answer, Provide ONLY a valid JSON object:
""".strip()
    return split_prompt

def get_summary_prompt():
    pass