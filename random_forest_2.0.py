import math
import time
import random


class Decision_Tree:
    'The data structure of decision tree is very nb'

    Tree = {}
    out_label = 0

    def __init__(self, thr):
        self.Threshold = thr
        Decision_Tree.Tree.clear()

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

    def build_tree_update(self, train_data, features):
        T = {}
        self.build_tree(train_data, features, T)
        Decision_Tree.Tree = T

    def build_tree(self, train_data, features, decision_tree):
        # 训练集要包含如下元素：特征名称和特征值，为一个列表嵌套字典
        # 特征集为一个字典，字典的键为特征名称和“label”，键值为该特征或标签的取值
        # 因为这个程序为一个递归程序，所以decision_tree这个传过来的参数
        # 可能仅仅是树的一个分支，经过ipython的test
        # python中的传值皆为对象，相当于一个引用

        if len(train_data) == 0:
            # print("There0")
            decision_tree.update({"no_feature": 0})
            # return decision_tree
            return

        ifequal = True
        flag = train_data[0]["label"]
        for item in range(len(train_data)):
            if flag != train_data[item]["label"]:
                ifequal = False
                break

        if ifequal:
            decision_tree.update({"no_feature": flag})
            # print("There1")
            # return decision_tree
            return

        if len(features) == 1:
            this_1_label = self.majority_decide(train_data, features)
            decision_tree.update({"no_feature": this_1_label})
            # print("There2")
            # return decision_tree
            return

        feature, igr = self.count_igr(train_data, features)
        # print(feature)

        if igr < self.Threshold:
            this_2_label = self.majority_decide(train_data, features)
            decision_tree.update({"no_feature": this_2_label})
            # print("There3")
            # return decision_tree
            return

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

            self.build_tree(processed_train_data, processed_features,
                            decision_tree[feature][cnt])

    def print_tree(self):
        print(Decision_Tree.Tree)

    def use_tree_predict(self, test_data, decision_tree):
        temp_list = []
        # print(decision_tree)
        for key in decision_tree:
            # print(key)
            temp_list.append(key)
        if len(temp_list) != 1:
            # print(len(temp_list))
            # print(temp_list)
            print("ERROR")
            # a = 0
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


class Random_Forest(Decision_Tree):
    'Forest is here'

    Forest = []

    def __init__(self, d_1, d_2, n_1, n_2):
        self.dimension_1 = d_1
        self.dimension_2 = d_2
        self.num_1 = n_1
        self.num_2 = n_2
        # super(Random_Forest, self).__init__(Threshold)

        # Random_Forest.Forest = [Decision_Tree() for n in range(self.num_1 * self.num_2)]

    def random_choice_train_data(self, train_data):
        num_1 = len(train_data)
        random_list_1 = [n for n in range(num_1)]
        slice_list_1 = random.sample(random_list_1, self.dimension_1)
        # print(slice_list_1)

        return slice_list_1

    def random_choice_features(self, features):

        num_2 = len(features) - 1
        random_list_2 = [n for n in range(num_2)]
        slice_list_2 = random.sample(random_list_2, self.dimension_2)
        # print(slice_list_2)

        return slice_list_2

    def plant_tree(self, train_data, features, Threshold):
        list_for_features_name = []
        for key in features:
            if key != "label":
                list_for_features_name.append(key)

        Random_Forest.Forest = [Decision_Tree(
            Threshold) for n in range(self.num_1 * self.num_2)]

        # for u in range(self.num_1 * self.num_2):
        #     Random_Forest.Forest[u].print_tree()
        t1 = time.clock()

        # Random_Forest.Forest[i * self.num_2 + j] = Decision_Tree(Threshold)
        for i in range(self.num_1):
            list_for_train_data = self.random_choice_train_data(train_data)
            train_data_temp = []

            for cnt in range(len(list_for_train_data)):
                train_data_temp.append(train_data[list_for_train_data[cnt]])
                # print(train_data[list_for_train_data[cnt]])

            for j in range(self.num_2):
                list_for_features = self.random_choice_features(features)
                features_temp = {}

                for cnt in range(len(list_for_features)):
                    feature_temp = list_for_features_name[list_for_features[cnt]]
                    num_temp = features[feature_temp]
                    features_temp.update({feature_temp: num_temp})

                num = features["label"]
                features_temp.update({"label": num})
                # print(features_temp)

                train_temp = []
                for sd in range(len(train_data_temp)):
                    d_temp_1 = {}
                    # print(train_data_temp[sd])
                    # d_temp_1 = train_data_temp[sd].copy()
                    for key in train_data_temp[sd]:
                        if key in features_temp:
                            # print(key)
                            d_temp_1.update({key: train_data_temp[sd][key]})
                    # train_data_temp[sd] = d_temp_1
                    # print(train_data_temp[sd])
                    # print(d_temp_1)
                    train_temp.append(d_temp_1)

                # print(i * self.num_2 + j)
                # Random_Forest.Forest[i * self.num_2 + j] = Decision_Tree(Threshold)
                # print(train_temp)
                # print(features_temp)

                # print(i * self.num_2 + j)
                # Random_Forest.Forest[i * self.num_2 + j].print_tree()
                Random_Forest.Forest[i * self.num_2 +
                                     j].build_tree_update(train_temp, features_temp)

                # Random_Forest.Forest[i * self.num_2 + j].print_tree()

        t2 = time.clock()
        time_used = t2 - t1
        print("Planting %d trees uses %.2fs." %
              ((self.num_1 * self.num_2), time_used))

    def predict_forest(self, test_data):
        result_labels = []

        for item in range(len(Random_Forest.Forest)):
            # Random_Forest.Forest[item].print_tree()
            result = Random_Forest.Forest[item].predict(test_data)
            result_labels.append(result)

        count_list = []
        count_list = [0 for n in range(666)]
        for cnt in range(len(result_labels)):
            count_list[result_labels[cnt]] = count_list[result_labels[cnt]] + 1

        max_num = 0
        max_label = 0
        for i in range(len(count_list)):
            if max_num <= count_list[i]:
                max_num = count_list[i]
                max_label = i

        return max_label
