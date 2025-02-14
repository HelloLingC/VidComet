from config_utils import *
import json
from string import Template

def get_split_prompt(word_limit: int):
    """
    num_parts: number of parts to split the sentence into
    word_limit: maximum number of words in each part
    """
    split_prompt = f"""
### Role
You are a professional Netflix subtitle splitter.

### Task
Split the given subtitle text into appropriate parts, each part less than {word_limit} words.

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
the upgraded claude sonnet is now available for all users developers can build with the computer use beta<br>on the anthropic api amazon bedrock and google cloud’s vertex ai<br>the new claude haiku will be released later this month

""".strip()
    return split_prompt

def get_summary_prompt():
    pass

def get_translation_prompt():
    TARGET_LANGUAGE = get_config_value("translator.target")
    src_language = get_config_value("whisper.detected_language")

    prompt_faithfulness = '''
### Role
You are a professional Netflix subtitle translator, fluent in both ${src_language} and {TARGET_LANGUAGE}. Your expertise lies in accurately understanding the semantics and structure of the original {src_language} text and faithfully translating it into {TARGET_LANGUAGE} while preserving the original meaning.

### Task
We have a segment of original ${src_language} subtitles that need to be directly translated into {TARGET_LANGUAGE}. These subtitles come from a specific context and may contain specific themes and terminology.

### Translation Principles
1. Faithful to the original: Accurately convey the content and meaning of the original text, without arbitrarily changing, adding, or omitting content.
2. Accurate terminology: Use professional terms correctly and maintain consistency in terminology.
3. Understand the context: Fully comprehend and reflect the background and contextual relationships of the text.

### Input Format
A JSON structure where each subtitle is identified by a unique numeric key:
{
  "1": "<<< Original Content >>>",
  "2": "<<< Original Content >>>",
  ...
}

### Output Format

Return a pure JSON following this structure and translate into ${target_language}:
{
  "1": {
    "translation": "<<< 第一轮直译:逐字逐句忠实原文,不遗漏任何信息。直译时力求忠实原文，使用${target_language} >>>",
    "free_translation": "<<< 第二轮意译:在保证原文意思不改变的基础上用通俗流畅的${target_language}意译原文，适度采用一些中文成语、熟语、网络流行语等,使译文更加地道易懂 >>>",
    "revise_suggestions": "<<< 第三轮改进建议:仔细审视以上译文,检测是否参考术语词汇翻译对应表以及要求（如果有）。结合注意事项，指出格式准确性、语句连贯性，阅读习惯和语言文化，给出具体改进建议。 >>>",
    "revised_translation": "<<< 第四轮定稿:择优选取整合,修改润色,最终定稿出一个简洁畅达、符合${target_language}阅读习惯和语言文化的译文 >>>"
  },
  ...
}

Please notice << >> represents placeholders that should not appear in your answer

### EXAMPLE INPUT
{
  "1": "为了实现双碳目标，中国正在努力推动碳达峰和碳中和。",
  "2": "这项技术真是YYDS！"
}

### EXAMPLE OUTPUT
{
  "1": {
    "translation": "In order to achieve the dual carbon goals, China is working hard to promote carbon peaking and carbon neutrality.",
    "free_translation": "To realize the dual carbon goals, China is striving to advance carbon peaking and carbon neutrality.",
    "revise_suggestions": "该句中涉及多个专业术语，如“dual carbon goals”（双碳目标）、“carbon peaking”（碳达峰）和“carbon neutrality”（碳中和），已参照相关术语词汇对应表进行翻译，确保专业性与准确性。在意译阶段，建议使用“To realize”替代冗长的“In order to achieve”，同时将“working hard to promote”调整为更简洁有力的“striving to advance”，以增强表达效果，符合视频字幕的简洁性和流畅性。",
    "revised_translation": "To realize the dual carbon goals, China is striving to advance carbon peaking and carbon neutrality."
  },
  "2": {
    "translation": "This technology is really YYDS!",
    "free_translation": "This technology is absolutely the GOAT!",
    "revise_suggestions": "‘YYDS’作为中文网络流行语，在英语中缺乏直接对应。参考文化背景和表达习惯，将其意译为‘GOAT’（Greatest Of All Time），既保留了原文的赞美和推崇之情，又符合英语表达习惯。在此基础上，使用‘absolutely’替代‘really’使语气更加强烈和自然，适合视频聊天的语境。",
    "revised_translation": "This technology is absolutely the GOAT!"
  }
}
'''
    return Template(prompt_faithfulness.strip()).substitute(src_language=src_language, target_language=TARGET_LANGUAGE)