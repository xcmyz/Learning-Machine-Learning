import json
import time
import jieba
import gensim

from desion_tree import Decision_Tree
import word2vec.load_ as load
from log_ import use_logging


def init():
    with open("./data/feature/name_dict.json", "r", encoding="utf-8")as file_name:
        name_dict = json.load(file_name)

    with open("./data/feature/features.json", "r", encoding="utf-8")as file_features:
        features = json.load(file_features)

    return name_dict, features


def create_test_data(list_symptom, features):
    template_test = {}
    for feature in features.keys():
        if feature != "label":
            template_test.update({feature: 0})

    for ele in list_symptom:
        template_test[ele] = 1

    # print(template_test)
    # print(len(template_test))

    return template_test


def test(list_symptom, tree_test):
    # init
    name_dict, features = init()
    test_data = create_test_data(list_symptom, features)

    # tree_test = Decision_Tree(ifload=True, file_name=file_tree)
    label = tree_test.predict(test_data)
    out_result = ""

    for key in name_dict.keys():
        if name_dict[key] == label:
            out_result = key

    # print(out_result)
    return out_result


if __name__ == "__main__":
    # list_symptom = []
    # name_dict, features = init()
    # create_test_data(list_symptom,features)

    list_symptom = "呕吐"
    file_tree = "./tree/decision_tree.json"
    tree_test = Decision_Tree(ifload=True, file_name=file_tree)
    # tree_test.print_tree()
    test(list_symptom, tree_test)
