"""
Model-based word similarity measurement.

Use model.sim(a,b) instead of static word vectors and cosine similarity.
"""
import sys
import os
import pandas as pd
import numpy as np

from ranking import *

def model_all_wordsim(model):
  """Return DataFrame of word similarity results.

  model must the following methods:
    model.sim(a, b) for string words a, b => Return scalar similarity between a and b.
    model.__contains__(a) for string word a
  """
  word_sim_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                              'data',
                              'word-sim')

  rows = []
  for filename in os.listdir(word_sim_dir):
    manual_dict, auto_dict = ({}, {})
    not_found, total_size = (0, 0)
    for line in open(os.path.join(word_sim_dir, filename),'r'):
      line = line.strip().lower()
      word1, word2, val = line.split()
      word1 = unicode(word1, encoding='ascii')
      word2 = unicode(word2, encoding='ascii')
      if word1 in model and word2 in model:
        manual_dict[(word1, word2)] = float(val)
        auto_dict[(word1, word2)] = model.sim(word1, word2)
      else:
        not_found += 1
      total_size += 1
    row = [filename, total_size, not_found,
           spearmans_rho(assign_ranks(manual_dict), assign_ranks(auto_dict))]
    rows.append(row)

  return pd.DataFrame(rows, columns=['Dataset', 'Num Pairs', 'Not found', 'Rho'])


# Mock model for test case
class RandomModel(object):
  """Return a random value from [-1, 1] for all similarities. Expected correlation is 0."""
  def __contains__(self, w):
    return True

  def sim(self, w, v):
    return np.random.uniform(-1, 1)

# Test case
if __name__ == '__main__':
  random_model = RandomModel()
  results = model_all_wordsim(random_model)
  print results