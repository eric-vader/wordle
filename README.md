# Wordle Bot for CS3243

This is an example implementation of the wordle bot; the heuristic used in the current implementation is using information entropy:

$$h_2(s_i)=\sum_{j\in[1,3^5]}\Bigg[\frac{|C_{i}^{(j)}|}{|C_{i-1}|}\log_2{\frac{|C_{i}^{(j)}|}{|C_{i-1}|}}\Bigg]$$

The heuristic is used for $1$-lookahead, it would be possible to consider multi-step lookahead.

Please see the [midterm slides](https://www.eric-han.com/teaching/AY2122S2/CS3243/Midterm_Tutorial_Slides.pdf) for the full setup and discussion.
Note that the heuristic here is `max` instead of `min`; but conversion is trivial.

The three word banks in the repo are as described:

1. `words_alpha.txt`: dictionary words from [https://github.com/dwyl/english-words/](https://github.com/dwyl/english-words/) - note this contains other non-5 letter words.
1. `words_wordle.txt`: dictionary words from the original wordle.
1. `words_wordle_ans.txt`: answer key from the original wordle, for self play purposes.

## How to use the bot

In the root directory of this repository,

1. Install required dependencies `pip install -r requirements.txt`
1. Run the bot `python wordle.py`.
    1. In the first run, it will pre-compute some data and it will take some time; it will generate a pickle file of 818MB.
    1. In subsequent runs, it will be faster relying on that pre-compute.

The bot is currently used with the `words_wordle.txt` as the dictionary $D$.

## Licence

All code released under MIT License.