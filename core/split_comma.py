import itertools
import split_main

""""""
def _is_vaild_sentence(sent):
    has_subject = any(token.dep_ == 'nsubj' for token in sent)
    has_verb = any(token.pos_ == 'VERB' or token.pos_ == 'AUX' for token in sent)
    return has_subject and has_verb

def should_split_by_comma(start, doc, token):
    left_sent = doc[max(start, token.i - 9):token.i]
    right_sent = doc[token.i + 1:min(len(doc), token.i + 10)]

    should_split = _is_vaild_sentence(right_sent) or _is_vaild_sentence(left_sent)

    left_words = [t for t in left_sent if not t.is_punct]
    right_words = list(itertools.takewhile(lambda t: not t.is_punct, left_sent))
 
    if len(left_words) <= 3 or len(right_words) <= 2:
        should_split = False
    return should_split


def split_sent_by_comma(text: str, nlp):
    """
    text是一个合法的句子，如: The book, which was on the table, and the pen, which was in the drawer, were both needed for the assignment.
    遍历句子的token，如果发现逗号的token，就判断是否应该在此逗号处切分句子
    """
    doc = nlp(text)
    start = 0
    for i, token in enumerate(doc):
        if token.text == ',' or token.text == '，':
            if should_split_by_comma(start, doc, token):
                start = token.i + 1
                print('split at: ', doc[start:])

if __name__ == '__main__':
    split_sent_by_comma('The book, which was on the table, and the pen, which was in the drawer, were both needed for the assignment.', split_main.prepare_spacy_model('en'))