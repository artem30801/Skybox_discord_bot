import os


def load_words():
    with open(os.path.abspath('english/skybox_dictionary.txt')) as word_file:
        valid_words = list(word_file.read().split())

    with open(os.path.abspath('english/topwiki.txt')) as word_file: #google-10000-english.txt
        valid_words.extend(word_file.read().split())

    return valid_words


if __name__ == '__main__':
    english_words = load_words()
    # demo print
    print('rest' in english_words)
