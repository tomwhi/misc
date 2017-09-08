from nltk.tokenize import sent_tokenize, word_tokenize
import codecs, re, sys

text = codecs.open(sys.argv[1], 'r', "utf-8").readline().split("|")[-1]
var = open(sys.argv[2]).readline().strip().split(",")

sents = sent_tokenize(text)

d = {'C': 'CYS', 'D': 'ASP', 'S': 'SER', 'Q': 'GLN', 'K': 'LYS', 'I': 'ILE', 'P': 'PRO', 'T': 'THR', 'F': 'PHE', 'N': 'ASN', 'G': 'GLY', 'H': 'HIS', 'L': 'LEU', 'R': 'ARG', 'W': 'TRP', 'A': 'ALA', 'V': 'VAL', 'E': 'GLU', 'Y': 'TYR', 'M': 'MET'}


def substitution_matches(word, aa_sub):
    int_span = re.search("[0-9]+", word).span()
    word_start = word[:int_span[0]]
    word_end = word[int_span[1]:]
    pos = int(word[int_span[0]:int_span[1]])
    if not word_start in aa_sub[0]:
        return False
    if not word_end in aa_sub[2]:
        return False
    if abs(pos - aa_sub[1]) > 20:
        return False
    return True


def aa_sub_tok(input_str):
    lett1 = input_str[0]
    lett2 = input_str[-1]
    aa_starts = [lett1, d[lett1], d[lett1].title(), d[lett1].lower()]
    aa_ends = [lett2, d[lett2], d[lett2].title(), d[lett2].lower()]
    pos = int(input_str[1:-1])
    return (aa_starts, pos, aa_ends)


def sent_match(sentence, query_aa_sub):
    aa_sub_tup = aa_sub_tok(query_aa_sub)
    for word in word_tokenize(sentence):
        try:
            if substitution_matches(word, aa_sub_tup):
                return True
        except Exception:
            pass
    alternative_aa_expressions = get_alternatives(aa_sub_tup)
    for alternative in alternative_aa_expressions:
        if alternative in sentence:
            return True
    return False


def get_alternatives(aa_sub):
    return([aa_sub[0][0] + str(aa_sub[1]) + aa_sub[2][0],
            aa_sub[0][1] + str(aa_sub[1]) + aa_sub[2][1],
            aa_sub[0][2] + str(aa_sub[1]) + aa_sub[2][2],
            aa_sub[0][3] + str(aa_sub[1]) + aa_sub[2][3]])


print("\n".join([sent for sent in sents if sent_match(sent, var[2])]), file=codecs.open(sys.argv[3], 'w', "utf-8"))
