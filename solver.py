from collections import Counter
import itertools

def load_words():
    with open('words_alpha.txt') as word_file:
        valid_words = set(word_file.read().split())

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

    print(is_wordpos_correct("aries", [set(), {'r'}, set(), set(), set()]))

    def get_stats(ws):

        # Calculate frequency of characters
        freq_map_words = {}
        positional_counter = [Counter(), Counter(), Counter(), Counter(), Counter()]
        freq_counter = Counter()
        freq_2char_counter = Counter()

        for w in ws:
            unique_chars = Counter(w)
            freq_map_words[w] = unique_chars
            for ea_i_counter, c in zip(positional_counter, w):
                ea_i_counter.update([c])

            freq_counter.update(unique_chars)
            freq_2char_counter.update(itertools.combinations(w, 2))

        # for ea_i_counter in positional_counter:
        #     print(ea_i_counter.most_common(3))

        rank_words = {}
        for w in ws:
            rank_words[w] = 0

            for ea_i_counter, ea_char in zip(positional_counter, w):
                rank_words[w] += ea_i_counter[ea_char]

            # for c in freq_map_words[w]:
            #     rank_words[w] += freq_counter[c]

            # for c2 in itertools.combinations(w, 2):
            #     rank_words[w] += freq_2char_counter[c2]

        return freq_map_words, list(reversed(sorted(rank_words, key=rank_words.get)))[:10]

    freq_map_words, current_words = get_stats(wordle_words)
    print(current_words)

    correct_chars_list = [set(), set(), set(), set(), set()]
    incorrect_chars_set = set()
    for i in range(6):

        correct_chars_set = Counter()

        current_word = input("Current Word:")
        response = input("Enter action (1 for correct, 2 for wrong pos, 0 else): ")
        print(response)

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