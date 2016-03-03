"""
Model-based open vocabulary analogy completion.

Use model.predict_analogy(a,b,a*) => Returns candidate b*.
"""

from read_analogy_open_vocab import analogy_readers
from collections import Counter

import pandas as pd

def model_all_analogy_open_vocab(model):
    """Return DataFrame of analogy completion

    model must the following methods:
      model.predict_analogy(a, b, a*) for string words a, b, a* => Returns prediction candidate word b*.
      model.__contains__(a) for string word a
    """

    rows = []
    # TODO: Parallelize...
    for dataset, reader in analogy_readers.iteritems():
        counts = Counter()
        not_found = Counter()
        correct_counts = Counter()

        for row in reader():
            counts[row.category] += 1

            if all(w in model for w in row.question):
                prediction = model.predict_analogy(*row.question)
                if prediction.lower() == row.answer.lower():
                    correct_counts[row.category] += 1
            else:
                not_found[row.category] += 1

        # Collate statistics
        for category, n_total in counts.iteritems():
            accuracy = float(correct_counts[category]) / n_total
            row = [dataset, n_total, not_found[category], category, accuracy]
            rows.append(row)

    return pd.DataFrame(rows, columns=['dataset', 'total_size', 'not_found', 'category', 'accuracy'])

# Mock model for test case
class ConstantModel(object):
    """Return a constant prediction."""
    def __init__(self, word):
        """Set the word that we will return."""
        self.word = word

    def __contains__(self, w):
        return True

    def predict_analogy(self, a, b, a_star):
        return self.word

# Test case
if __name__ == '__main__':
    model = ConstantModel('sings')
    results = model_all_analogy_open_vocab(model)
    print results

