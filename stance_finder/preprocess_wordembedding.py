import re
import sys
import glob
import os

lettersanddotsonly = re.compile(r'[^a-zA-Z\.]')


def preprocess(s):
    # Should we first ascify?
    s = s.lower().replace('!', '.').replace('?', '.')  # replace ! and ? by . for splitting sentences
    s = lettersanddotsonly.sub(' ', s)
    # Should we replace multiple consecutive whitespace by 1 space?
    return s


def get_sentences(filename):
    with open(filename) as fin:
        text = fin.read()
    sentences = preprocess(text).split('.')
    sentence_as_list = [' '.join(s.split()) for s in sentences]
    return sentences


if __name__ == "__main__":
    input_dir = sys.argv[1]
    output_file = sys.argv[2]

    with open(output_file, 'w') as fout:
        for filename in glob.glob(os.path.join(input_dir, '*')):
            sentences = get_sentences(filename)
            for s in sentences:
                fout.write(s)
                fout.write('\n')
