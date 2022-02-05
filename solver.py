from collections import Counter, defaultdict
import itertools

def load_words():
    with open('words_alpha.txt') as word_file:
        valid_words = set([ w.lower() for w in word_file.read().split() if w.isalpha()])

    return valid_words

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


if __name__ == '__main__':
    english_words = load_words()

    wordle_words = { w for w in english_words if len(w) == 5}

    def get_stats(ws):

        # Calculate frequency of characters
        freq_map_words = {}
        
        # positional_counter_map = defaultdict(lambda: [Counter(), Counter(), Counter(), Counter(), Counter()])
        positional_counter = [Counter(), Counter(), Counter(), Counter(), Counter()]
        freq_counter = Counter()
        # Counter for a particulat unique set of chars
        freq_counter_unique_map = defaultdict(lambda : 0)
        positional_counter_unique_map = defaultdict(lambda : [Counter(), Counter(), Counter(), Counter(), Counter()])
        freq_2char_counter = Counter()

        n_ws = len(ws)

        for w in ws:
            unique_chars_counter = Counter(w)
            unique_chars_set = frozenset(w)

            freq_map_words[w] = unique_chars_counter
            for ea_i_counter, c in zip(positional_counter_unique_map[unique_chars_set], w):
                ea_i_counter.update([c])

            freq_counter_unique_map[unique_chars_set]+=1 #.update(unique_chars_set)

            freq_counter.update(unique_chars_set)
            freq_2char_counter.update(itertools.combinations(w, 2))
        
        # Now we do DP to propagate the 1 to 2, 2 to 3 and so on...
        max_unique_len = max([ len(s) for s in freq_counter_unique_map.keys()])
        for l in range(2,max_unique_len+1):
            for uniquechar_l in filter(lambda c: len(c)==l, freq_counter_unique_map.keys()):
                for dominated_uniquechar_l in itertools.combinations(uniquechar_l, len(uniquechar_l)-1):
                    dominated_uniquechar_l = frozenset(dominated_uniquechar_l)
                    if dominated_uniquechar_l in freq_counter_unique_map:
                        freq_counter_unique_map[uniquechar_l] += freq_counter_unique_map[dominated_uniquechar_l]

                        for ea_target, ea_source in zip(positional_counter_unique_map[uniquechar_l], positional_counter_unique_map[dominated_uniquechar_l]):
                            ea_target.update(ea_source)

        # for ea_i_counter in positional_counter:
        #     print(ea_i_counter.most_common(3))
        n_unique = sum(freq_counter.values())

        rank_words = {}
        for w in ws:
            
            unique_chars_set = frozenset(w)
            

            rank_words[w] = freq_counter_unique_map[unique_chars_set]/n_unique
            char_sum_map = {}
            for c in unique_chars_set:
                char_sum_map[c] = sum([ ea_i_counter[c] for ea_i_counter in positional_counter_unique_map[unique_chars_set] ])

            pos_stats = 0
            for i, ea_i_counter, ea_char in zip(range(5), positional_counter_unique_map[unique_chars_set], w):
                pos_stats += ea_i_counter[ea_char]/char_sum_map[ea_char]
                # rank_words[w] += ea_i_counter[ea_char]
            rank_words[w] *= pos_stats

            # for c2 in itertools.combinations(w, 2):
            #     rank_words[w] += freq_2char_counter[c2]
        
        return freq_map_words, list(reversed(sorted(rank_words, key=rank_words.get)))[:10]

    freq_map_words, current_words = get_stats(wordle_words)
    print(current_words)

    correct_chars_list = [set(), set(), set(), set(), set()]
    incorrect_chars_set = set()
    for i in range(6):

        correct_chars_set = Counter()

        current_word = input("Current Word: ")
        response = input("Enter action (1 for correct, 2 for wrong pos, 0 else): ")
        # print(response)

        if response == "11111":
            break

        for r, c, i in zip(list(response), list(current_word), range(5)):
            if r == "1":
                correct_chars_set.update([c])
                correct_chars_list[i] = c
            elif r == "2":
                correct_chars_set.update([c])
                correct_chars_list[i].add(c)
            else:
                incorrect_chars_set.add(c)

        diff_incorrect_set = incorrect_chars_set - set(correct_chars_set.keys())
        wordle_words = { w for w in wordle_words if is_wordpos_correct(list(w), correct_chars_list)}
        wordle_words = { w for w in wordle_words if all([ freq_map_words[w][k] >= v for k,v in correct_chars_set.items() if not k in incorrect_chars_set ]) }
        wordle_words = { w for w in wordle_words if all([ freq_map_words[w][k] == v for k,v in correct_chars_set.items() if k in incorrect_chars_set ]) }
        wordle_words = { w for w in wordle_words if not any([u in diff_incorrect_set for u in set(freq_map_words[w].keys())]) }
        
        freq_map_words, current_words = get_stats(wordle_words)
        print(current_words)

    print(f"Solution is: {current_word}")