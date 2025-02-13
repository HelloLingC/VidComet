from config_utils import *
import json

def get_split_prompt(num_parts: int, word_limit: int):
    """
    num_parts: number of parts to split the sentence into
    word_limit: maximum number of words in each part
    """
    split_prompt = f"""
### Role
You are a professional Netflix subtitle splitter.

### Task
Split the given subtitle text into {num_parts} parts, each less than {word_limit} words.

### Instructions
1. Maintain sentence meaning coherence according to Netflix subtitle standards
2. Keep parts roughly equal in length (minimum 3 words each)
3. Split at natural points like punctuation marks or conjunctions
4. It is necessary to use <br> for segmentation based on the semantics.
5. Directly return the segmented text without additional explanation.

### Examples
Input:
the upgraded claude sonnet is now available for all users developers can build with the computer use beta on the anthropic api amazon bedrock and google cloud’s vertex ai the new claude haiku will be released later this month
Output:
the upgraded claude sonnet is now available for all users<br>developers can build with the computer use beta<br>on the anthropic api amazon bedrock and google cloud’s vertex ai<br>the new claude haiku will be released later this month

""".strip()
    return split_prompt

def get_summary_prompt():
    pass

def get_translation_prompt(lines, shared_prompt):
    TARGET_LANGUAGE = get_config_value("target_language")
    # Split lines by \n
    line_splits = lines.split('\n')
    
    # Create JSON return format example
    json_format = {}
    for i, line in enumerate(line_splits, 1):
        json_format[i] = {
            "origin": line,
            "direct": f"<<direct {TARGET_LANGUAGE} translation>>"
        }
    
    src_language = get_config_value("whisper.detected_language")
    prompt_faithfulness = f'''
### Role Definition
You are a professional Netflix subtitle translator, fluent in both {src_language} and {TARGET_LANGUAGE}, as well as their respective cultures. Your expertise lies in accurately understanding the semantics and structure of the original {src_language} text and faithfully translating it into {TARGET_LANGUAGE} while preserving the original meaning.

### Task Background
We have a segment of original {src_language} subtitles that need to be directly translated into {TARGET_LANGUAGE}. These subtitles come from a specific context and may contain specific themes and terminology.

### Task Description
1. Translate the original {src_language} subtitles into {TARGET_LANGUAGE} line by line
2. Ensure the translation is faithful to the original, accurately conveying the original meaning
3. Consider the context and professional terminology

{shared_prompt}

### Translation Principles
1. Faithful to the original: Accurately convey the content and meaning of the original text, without arbitrarily changing, adding, or omitting content.
2. Accurate terminology: Use professional terms correctly and maintain consistency in terminology.
3. Understand the context: Fully comprehend and reflect the background and contextual relationships of the text.

### Subtitle Data
<subtitles>
{lines}
</subtitles>
### Output Format
Please complete the following JSON data, where << >> represents placeholders that should not appear in your answer, and return your translation results in JSON format:
{json.dumps(json_format, ensure_ascii=False, indent=4)}
'''
    return prompt_faithfulness.strip()