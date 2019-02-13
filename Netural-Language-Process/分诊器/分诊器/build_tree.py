import json
import time
import jieba
import gensim

from desion_tree import Decision_Tree
import word2vec.load_ as load
from log_ import use_logging


@use_logging
def check_data(train_data, features):
    print("The length of train data is %d." % len(train_data))
    print("The type of train data is %s." % type(train_data))
    print("The value of 'label' is %d." % features["label"])
    # print(features)
    # print(len(features))
    value = features["label"]

    name_list = []
    name_dict = {}
    cnt = 0
    for ele in train_data:
        # print(ele["label"])
        if ele["label"] not in name_list:
            name_list.append(ele["label"])
            name_dict.update({ele["label"]: cnt})
            cnt = cnt
            cnt = cnt + 1

    if len(name_list) == value:
        print("RIGHT: the length of features")
        # print(len(name_dict))
        # print(name_dict)
    else:
        print("ERROR!!!")

    return name_dict


@use_logging
def init_data():
    time_start = time.clock()
    with open("./data/saver_1.json", "r", encoding="utf-8")as file_train_data:
        train_data = json.load(file_train_data)
        # print(len(train_data))
        # print(type(train_data))
        # print(train_data[12])

    with open("./data/feature/features.json", "r", encoding="utf-8")as file_features:
        features = json.load(file_features)
        # print(len(features))
        # print(type(features))

    time_end = time.clock()
    print("Time used is %.2f s." % (time_end - time_start))

    return train_data, features


@use_logging
def reprocess_train_data(pre_train_data, labels_dict):
    # cnt = 0
    time_start = time.clock()
    for ele in pre_train_data:
        ele["label"] = labels_dict[ele["label"]]
        # cnt = cnt + 1

    time_end = time.clock()
    # print(cnt)
    # print(pre_train_data[12]["label"])
    print("Reprocessing train data use %.2f s." % (time_end - time_start))
    return pre_train_data


@use_logging
def init():
    pre_train_data, features = init_data()
    labels_dict = check_data(pre_train_data, features)
    train_data = reprocess_train_data(pre_train_data, labels_dict)

    load.add_userdict("./word2vec/data_init/dictionary.txt")
    stopwords = load.load_stop_words("./word2vec/data_init/stopword.txt")
    model = gensim.models.Word2Vec.load('./word2vec/model/model')

    return train_data, features, model, stopwords


@use_logging
def split_consultation(sequence):
    train_data, features, model, stopwords = init()

    build_decision_tree(train_data, features)

    # Cut words
    words_out = load.cut_words(sequence, stopwords)
    print("#####################")
    print(words_out)
    print("#####################")
    print()
    # for word in words_out:
    #     for ele in model.most_similar(word):
    #         print(ele)
    #     print()


@use_logging
def build_decision_tree(train_data, features):
    tree = Decision_Tree(0.012)
    tree.build_tree(train_data, features)

    file_model = "./tree/decision_tree.json"
    tree.save_model(file_model)


if __name__ == "__main__":

    test_seq = "我有点胃痛加恶心"
    split_consultation(test_seq)
