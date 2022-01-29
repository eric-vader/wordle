import collections 

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
        freq_counter = collections.Counter()

        for w in ws:
            unique_chars = set(w)
            freq_map_words[w] = unique_chars
            freq_counter.update(unique_chars)

        rank_words = {}
        for w in ws:
            rank_words[w] = 0

            for c in freq_map_words[w]:
                rank_words[w] += freq_counter[c]

        return freq_map_words, list(reversed(sorted(rank_words, key=rank_words.get)))[:10]

    freq_map_words, current_words = get_stats(wordle_words)
    print(current_words)

    correct_chars_set = set()
    correct_chars_list = [set(), set(), set(), set(), set()]
    incorrect_chars_set = set()
    for i in range(6):

        current_word = input("Current Word:")
        response = input("Enter action (1 for correct, 2 for wrong pos, 0 else): ")
        print(response)

        if response == "11111":
            break

        for r, c, i in zip(list(response), list(current_word), range(5)):
            if r == "1":
                correct_chars_set.add(c)
                correct_chars_list[i] = c
            elif r == "2":
                correct_chars_set.add(c)
                correct_chars_list[i].add(c)
            else:
                incorrect_chars_set.add(c)

        print(correct_chars_set)
        print(correct_chars_list)
        print(incorrect_chars_set)

        wordle_words = { w for w in wordle_words if correct_chars_set.issubset(freq_map_words[w]) }
        wordle_words = { w for w in wordle_words if not any([u in incorrect_chars_set for u in freq_map_words[w]]) }
        wordle_words = { w for w in wordle_words if is_wordpos_correct(list(w), correct_chars_list)}

        freq_map_words, current_words = get_stats(wordle_words)
        print(current_words)

    print(f"Solution is: {current_word}")