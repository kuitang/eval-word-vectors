import os

from collections import namedtuple
from itertools import izip

# If an analogy is a:b::a*:b*, the question is (a, b, a*) and the answer is b*.
Question = namedtuple('Question', ['category', 'question', 'answer'])

analogy_open_vocab_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                      'data',
                                      'analogy-open-vocab')

# Currently only handle the words; will do phrases later.
def read_google():
    fname = os.path.join(analogy_open_vocab_dir, 'google', 'questions-words.txt')
    with open(fname, 'r') as of:
        curr_category = None
        for line in of:
            line = line.strip().lower()
            # Are we at a category header?
            toks = [unicode(x, encoding='ascii') for x in line.split()]
            if line[0] == ':':
                curr_category = toks[1]
            else:
                assert curr_category is not None
                yield Question(curr_category,
                               tuple(toks[:3]),
                               toks[3])

def read_msr():
    q_fname = os.path.join(analogy_open_vocab_dir, 'msr', 'word_relationship.questions')
    a_fname = os.path.join(analogy_open_vocab_dir, 'msr', 'word_relationship.answers')

    with open(q_fname, 'r') as qf, open(a_fname, 'r') as af:
        for q_line, a_line in izip(qf, af):
            category, answer = a_line.split()
            yield Question(category,
                           tuple(q_line.split()),
                           answer)

analogy_readers = {'google': read_google, 'msr': read_msr}
