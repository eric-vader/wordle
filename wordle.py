from collections import Counter, defaultdict
import copy
from itertools import product

def is_wordpos_correct(ws, cs):
    for w, c in zip(ws, cs):
        if c == set():
            continue
        if type(c) == str:
            if c == w:
                continue
            else:
                return False
        if w in c:
            return False
    return True

class WordSpace(object):
    def __init__(self, file_name):
        with open(file_name) as word_file:
            self.words = set([ w.lower() for w in word_file.read().split() if w.isalpha()])
        
        self.freq_map_words = {}
        for ea_w in self.words:
            unique_chars_counter = Counter(ea_w)
            self.freq_map_words[ea_w] = unique_chars_counter
    def copy(self):
        return copy.deepcopy(self)

class Constraint(object):
    def __init__(self, response, action_word):
        self.correct_chars_list = [set(), set(), set(), set(), set()]
        self.incorrect_chars_set = set()

        self.correct_chars_set = Counter()

        for ea_r, ea_c, i in zip(response, action_word, range(5)):
            if ea_r == "1":
                self.correct_chars_set.update([ea_c])
                self.correct_chars_list[i] = ea_c
            elif ea_r == "2":
                self.correct_chars_set.update([ea_c])
                self.correct_chars_list[i].add(ea_c)
            else:
                self.incorrect_chars_set.add(ea_c)        
    def apply_to(self, old_ws):
        ws = old_ws.copy()

        diff_incorrect_set = self.incorrect_chars_set - set(self.correct_chars_set.keys())
        ws.words = { w for w in ws.words if is_wordpos_correct(w, self.correct_chars_list)}
        ws.words = { w for w in ws.words if all([ ws.freq_map_words[w][k] >= v for k,v in self.correct_chars_set.items() if not k in self.incorrect_chars_set ]) }
        ws.words = { w for w in ws.words if all([ ws.freq_map_words[w][k] == v for k,v in self.correct_chars_set.items() if k in self.incorrect_chars_set ]) }
        ws.words = { w for w in ws.words if not any([u in diff_incorrect_set for u in set(ws.freq_map_words[w].keys())]) }

        return ws

    def count_filtered(self, ws):

        diff_incorrect_set = self.incorrect_chars_set - set(self.correct_chars_set.keys())

        count = 0
        for w in ws.words:
            if (is_wordpos_correct(w, self.correct_chars_list) 
                    and all([ ws.freq_map_words[w][k] >= v for k,v in self.correct_chars_set.items() if not k in self.incorrect_chars_set ])
                    and all([ ws.freq_map_words[w][k] == v for k,v in self.correct_chars_set.items() if k in self.incorrect_chars_set ])
                    and (not any([u in diff_incorrect_set for u in set(ws.freq_map_words[w].keys())]))):
                count += 1

        return count

class WordleEnv(object):
    def __init__(self, target_word):
        self.target_word = target_word
    def guess(self, guess_word):
        response = [0,0,0,0,0]
        target_unique = set(self.target_word)
        
        for g_c, t_c, i in zip(guess_word, self.target_word, range(len(response))):
            if g_c == t_c:
                response[i] = 1
                target_unique.discard(t_c)

        for g_c, i in zip(guess_word, range(len(response))):
            if g_c in target_unique:
                response[i] = 2
                target_unique.discard(g_c)

        return ''.join(map(str, response))


dict_ws = WordSpace("words_wordle.txt")
ans_ws = WordSpace("words_wordle_ans.txt")
c = Constraint("11111", "brawl")
print(c.apply_to(dict_ws).words)

# print(list(product(*[[1,2,3],[1,2,3],[1,2,3]])))
responses_perm = [ ''.join(perm) for perm in product(*(["123"]*5)) ]
from tqdm import tqdm
from collections import defaultdict

count_dict = {}
for ea_guess_word in tqdm(dict_ws.words):
    count_dict[ea_guess_word] = {}
    for ea_dict_word in ans_ws.words:
        env = WordleEnv(ea_dict_word)
        ea_constraint = Constraint(env.guess(ea_guess_word), ea_guess_word)
        count_dict[ea_guess_word][ea_dict_word] = ea_constraint.count_filtered(dict_ws)

import pickle
pickle.dump(count_dict, open('count_dict.pickle', 'wb'))



# for ea_guess_word in dict_ws.words:
#     total_filtered = 0
#     for ea_response in responses_perm:
#         total_filtered += Constraint(ea_response, ea_guess_word).count_filtered(dict_ws)
#     print(len(dict_ws.words), total_filtered)
    

# env = WordleEnv("shake")
# print(env.guess("sweet"))
