import json
import time
import jieba


def add_userdict(file_name_of_userdict):
    jieba.load_userdict(file_name_of_userdict)


def remove_duplicates(data_list):
    out_list = []

    for word in data_list:
        if word not in out_list:
            out_list.append(word)

    # print(len(out_list))
    return out_list


def load_stop_words(file_name):
    file_of_stopwords = open(file_name, "r", encoding='utf-8')
    data = file_of_stopwords.readlines()
    data_new = []
    for line in data:
        line = line.strip('\n')
        data_new.append(line)

    str_file_1 = 'C:/Users/28012/Desktop/Machine Learning/' + \
        'Natural Language Processing/HCP实验室/分诊器/word2vec/data_init/stop_words_processed.txt'
    str_file_2 = "C:/Users/28012/Desktop/Machine Learning/" + \
        "Natural Language Processing/HCP实验室/分诊器/word2vec/data_init/stop_words_processed.txt"

    # print(len(data_new))
    data_out = remove_duplicates(data_new)
    file_of_stopwords.close()
    # print(len(data_out))
    file_sw = open(str_file_1, 'w', encoding='utf-8')
    for ele in data_out:
        file_sw.write(ele)
        file_sw.write('\n')
    file_sw.close()

    file_of_stopwords_new = open(str_file_2, "r", encoding='utf-8')
    data_sw_new = file_of_stopwords_new.readlines()
    data_sw_out = []
    for line in data_sw_new:
        line = line.strip('\n')
        data_sw_out.append(line)

    # print(type(data_sw_out))
    # print(len(data_sw_out))
    # print(data_sw_out[0])
    return data_sw_out


def cut_words(str_words, stopwords):
    words = list(jieba.cut(str_words))
    words_out = []
    for word in words:
        if word not in stopwords:
            words_out.append(word)

    return words_out


if __name__ == "__main__":
    add_userdict("./data_init/dictionary.txt")
    load_stop_words("./data_init/stopword.txt")
