import math
import time
import json

from log_ import use_logging


class Decision_Tree:
    'The data structure of decision tree is very nb'

    Tree = {}
    out_label = 0

    def __init__(self, thr, ifload=False, file_name=None):
        self.Threshold = thr

        if ifload == True:
            with open(file_name, 'r', encoding='utf-8')as model_file:
                self.Tree = json.load(model_file)

    def get_max_key(self, in_list):
        flag = 0
        out_key = 0
        for i in range(len(in_list)):
            if in_list[i] >= flag:
                flag = in_list[i]
                out_key = i

        return out_key

    def majority_decide(self, dataset, features):
        pos_value = features["label"]
        count_list = [0 for i in range(pos_value)]

        for item in range(len(dataset)):
            temp_num = dataset[item]["label"]
            count_list[temp_num] = count_list[temp_num] + 1

        out_label = self.get_max_key(count_list)
        return out_label

    def count_igr(self, train_data, features):
        features_name = []
        for key in features:
            if key != "label":
                features_name.append(key)

        features_dict = {}
        H_features = {}
        H_features_condition = {}
        G_features = {}
        IGR_features = {}

        features_dict = features_dict.fromkeys(features_name, 0.0)
        H_features = H_features.fromkeys(features_name, 0.0)
        H_features_condition = H_features_condition.fromkeys(
            features_name, 0.0)
        G_features = G_features.fromkeys(features_name, 0.0)
        IGR_features = IGR_features.fromkeys(features_name, 0.0)

        # 数据集的信息熵
        H_dataset = 0.0
        count_list = [0 for n in range(features["label"])]
        for i in range(len(train_data)):
            num = train_data[i]["label"]
            # print("&&&&&&&&&&&&&&&&&")
            # print(num)
            count_list[num] = count_list[num] + 1
        for j in range(features["label"]):
            mul_1 = count_list[j] / len(train_data)
            if mul_1 == 0.0:
                mul_2 = 0.0
            else:
                mul_2 = math.log2(mul_1)
            H_dataset = H_dataset + mul_1 * mul_2
        H_dataset = 0.0 - H_dataset

        # 特征值A的熵
        for key in features:
            if key != "label":
                count_list_feature = [0 for n in range(features[key])]
                for i in range(len(train_data)):
                    num = train_data[i][key]
                    count_list_feature[num] = count_list_feature[num] + 1
                for j in range(features[key]):
                    mul_1 = count_list_feature[j] / len(train_data)
                    if mul_1 == 0.0:
                        mul_2 = 0
                    else:
                        mul_2 = math.log2(mul_1)
                    H_features[key] = H_features[key] + mul_1 * mul_2
                H_features[key] = 0 - H_features[key]
            else:
                continue

        # 条件熵
        for key in features:
            if key != "label":
                for a in range(features[key]):
                    H_dataset_temp = 0.0
                    count_list_temp = [0 for n in range(features["label"])]
                    cnt_i = 0
                    for i in range(len(train_data)):
                        if train_data[i][key] == a:
                            cnt_i = cnt_i + 1
                            num = train_data[i]["label"]
                            count_list_temp[num] = count_list_temp[num] + 1
                    for j in range(features["label"]):
                        if count_list_temp[j] == 0:
                            mul_1 = 0
                        else:
                            mul_1 = count_list_temp[j] / cnt_i
                        if mul_1 == 0.0:
                            mul_2 = 0
                        else:
                            mul_2 = math.log2(mul_1)
                        H_dataset_temp = H_dataset_temp + mul_1 * mul_2
                    H_dataset_temp = 0 - H_dataset_temp
                    H_features_condition[key] = H_features_condition[key] + \
                        (cnt_i / len(train_data)) * H_dataset_temp
            else:
                continue

        for key_name_1 in G_features:
            G_features[key_name_1] = H_dataset - \
                H_features_condition[key_name_1]

        # 没有用信息增益比
        for key_name_2 in IGR_features:
            # IGR_features[key_name_2] = G_features[key_name_2] / \
            #     (H_features[key_name_2] + 0.1)
            IGR_features[key_name_2] = G_features[key_name_2]

        out_feature = ""
        out_IGR = -3126661212
        for key_name_3 in IGR_features:
            if out_IGR <= IGR_features[key_name_3]:
                out_IGR = IGR_features[key_name_3]
                out_feature = key_name_3

        return out_feature, out_IGR

    def build(self, train_data, features, decision_tree):
        # 训练集要包含如下元素：特征名称和特征值，为一个列表嵌套字典
        # 特征集为一个字典，字典的键为特征名称和“label”，键值为该特征或标签的取值
        # 因为这个程序为一个递归程序，所以decision_tree这个传过来的参数
        # 可能仅仅是树的一个分支，经过ipython的test
        # python中的传值皆为对象，相当于一个引用

        if len(train_data) == 0:
            decision_tree.update({"no_feature": 0})
            return decision_tree

        ifequal = True
        flag = train_data[0]["label"]
        for item in range(len(train_data)):
            if flag != train_data[item]["label"]:
                ifequal = False
                break

        if ifequal:
            decision_tree.update({"no_feature": flag})
            # print("There1")
            return decision_tree

        if len(features) == 1:
            this_1_label = self.majority_decide(train_data, features)
            decision_tree.update({"no_feature": this_1_label})
            # print("There2")
            return decision_tree

        feature, igr = self.count_igr(train_data, features)
        # print(feature)

        if igr < self.Threshold:
            this_2_label = self.majority_decide(train_data, features)
            decision_tree.update({"no_feature": this_2_label})
            # print("There3")
            return decision_tree

        # if feature == '':
        #     print("ERROR")
        creat_list_num = features[feature]
        creat_list = [0 for j in range(creat_list_num)]
        decision_tree.update({feature: creat_list})
        for cnt in range(creat_list_num):
            decision_tree[feature][cnt] = {}
            processed_train_data = []
            for it in range(len(train_data)):
                if train_data[it][feature] == cnt:
                    processed_train_data.append(train_data[it])
                else:
                    continue

            processed_features = {}
            processed_features = features.copy()
            processed_features.pop(feature)

            self.build(processed_train_data, processed_features,
                       decision_tree[feature][cnt])

    @use_logging
    def build_tree(self, train_data, features):
        print("Start training...")
        time_start = time.clock()
        self.build(train_data, features, Decision_Tree.Tree)
        time_end = time.clock()
        print("Training end.")
        print("Building tree use %.2f s." % (time_end - time_start))

    def print_tree(self):
        print(Decision_Tree.Tree)

    def use_tree_predict(self, test_data, decision_tree):
        temp_list = []
        for key in decision_tree:
            temp_list.append(key)
        if len(temp_list) != 1:
            print("ERROR")
        else:
            if temp_list[0] == "no_feature":
                temp_num = decision_tree["no_feature"]
                out_label = temp_num
                Decision_Tree.out_label = out_label
            else:
                index = test_data[temp_list[0]]
                self.use_tree_predict(
                    test_data, decision_tree[temp_list[0]][index])

    def predict(self, test_data):
        self.use_tree_predict(test_data, Decision_Tree.Tree)
        return Decision_Tree.out_label

    def save_model(self, file_name):
        with open(file_name, "w", encoding='utf-8')as file_model:
            json.dump(self.Tree, file_model, ensure_ascii=False)


if __name__ == "__main__":

    train_data = [{"age": 0, "work": 0, "house": 0, "money": 0, "label": 0},
                  {"age": 0, "work": 0, "house": 0, "money": 1, "label": 0},
                  {"age": 0, "work": 1, "house": 0, "money": 1, "label": 1},
                  {"age": 0, "work": 1, "house": 1, "money": 0, "label": 1},
                  {"age": 0, "work": 0, "house": 0, "money": 0, "label": 0},
                  {"age": 1, "work": 0, "house": 0, "money": 0, "label": 0},
                  {"age": 1, "work": 0, "house": 0, "money": 1, "label": 0},
                  {"age": 1, "work": 1, "house": 1, "money": 1, "label": 1},
                  {"age": 1, "work": 0, "house": 1, "money": 2, "label": 1},
                  {"age": 1, "work": 0, "house": 1, "money": 2, "label": 1},
                  {"age": 2, "work": 0, "house": 1, "money": 2, "label": 1},
                  {"age": 2, "work": 0, "house": 1, "money": 1, "label": 1},
                  {"age": 2, "work": 1, "house": 0, "money": 1, "label": 1},
                  {"age": 2, "work": 1, "house": 0, "money": 2, "label": 1},
                  {"age": 2, "work": 0, "house": 0, "money": 0, "label": 0}
                  ]

    features = {"age": 3, "work": 2, "house": 2, "money": 3, "label": 2}

    test_tree = Decision_Tree(0.0)
    test_tree.build_tree(train_data, features)
    test_data = {"age": 2, "work": 1, "house": 0, "money": 2}
    pre = test_tree.predict(test_data)
    print(pre)
