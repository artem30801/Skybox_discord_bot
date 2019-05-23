import os


def load_words():
    with open(os.path.abspath('english/google-10000-english.txt')) as word_file:
        valid_words = set(word_file.read().split())

    with open(os.path.abspath('english/skybox_dictionary.txt')) as word_file:
        valid_words.update(word_file.read().split())

    return valid_words


if __name__ == '__main__':
    english_words = load_words()
    # demo print
    print('rest' in english_words)
