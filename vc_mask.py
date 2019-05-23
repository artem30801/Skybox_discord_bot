from english_words.read_english_dictionary import load_words
import re


words = load_words()


def convert_spacetalk(word):
    output = re.sub('[aeiou]', '-', word)
    output = re.sub('--', '—', output)
    output = re.sub('[b-df-hyj-np-tv-xz]', '/', output)
    return output


def mask_match(word):
    word = convert_spacetalk(word)
    size = len(word)
    len_words = filter(lambda x: len(x) == size, words)
    out_words = filter(lambda x: convert_spacetalk(x) == word, len_words)
    return out_words


if __name__ == "__main__":
    word = input("Spacetlak mask to find: ")
    result = list(mask_match(word))
    print("Total words found: {} \n	100 first words are: {}".format(len(result), result[:100]))
