from collections import Counter, defaultdict
import copy

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

ws = WordSpace("words_wordle.txt")
c = Constraint("11111", "brawl")
c.apply_to(ws)