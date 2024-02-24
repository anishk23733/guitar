import itertools
import random

def generate_permutations(seq_range=5):
    seq = [str(i) for i in range(seq_range)]
    return ["".join(s) for s in itertools.permutations(seq)]

def select_permutation(seq_range=5):
    return random.choice(generate_permutations(seq_range))