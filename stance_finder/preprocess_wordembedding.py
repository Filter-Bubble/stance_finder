import re
import sys
import glob
import os
from unidecode import unidecode

lettersanddotsonly = re.compile(r'[^a-zA-Z\.]')


def preprocess(s):
    # This is new: first ascify
    s = unidecode(s)
    s = s.lower().replace('!', '.').replace('?', '.')  # replace ! and ? by . for splitting sentences
    s = lettersanddotsonly.sub(' ', s)

    return s


def get_sentences(filename):
    with open(filename) as fin:
        text = fin.read()
    sentences = preprocess(text).split('.')
    sentences_as_list = [' '.join(s.split()) for s in sentences]
    return sentences_as_list


if __name__ == "__main__":
    input_dir = sys.argv[1]
    output_file = sys.argv[2]

    with open(output_file, 'w') as fout:
        for filename in glob.glob(os.path.join(input_dir, '*')):
            sentences = get_sentences(filename)
            for s in sentences:
                if len(s) > 0:
                    fout.write(s)
                    fout.write('\n')
