from english.read_english_dictionary import load_words
import re
import itertools


words = load_words()


def convert_spacetalk(word):
    output = re.sub('[aeiou]', '-', word)
    output = improve_spacetalk(output)
    output = re.sub('[b-df-hyj-np-tv-xz]', '/', output)
    return output


def improve_spacetalk(word):
    output = re.sub('--', '—', word)
    return output


def clarify_spacetalk(word):
    output = re.sub('—', '--', word)
    return output


def mask_match(word):
    word = clarify_spacetalk(word)
    size = len(word)
    word = improve_spacetalk(word)
    if re.match('[^\/\-—]', word):
        out_words = [word]
    else:
        len_words = filter(lambda x: len(x) == size, words)
        out_words = filter(lambda x: convert_spacetalk(x) == word, len_words)
    return out_words


def sentence_match(*wordlist, wordnum=5):
    all_variants = [list(mask_match(str(x)))[:wordnum] for x in wordlist]
    # print(all_variants)
    return itertools.product(*all_variants)


if __name__ == "__main__":
    word = input("Spacetlak mask to find: ")
    print(*sentence_match(*word.split(), wordnum=20), sep='\n')
    #result = list(mask_match(word))
    #print("Total words found: {} \n	100 first words are: {}".format(len(result), result[:100]))
