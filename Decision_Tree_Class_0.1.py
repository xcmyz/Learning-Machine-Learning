import math


class Decision_Tree:

    Tree = {}

    def __init__(self, thr, dataset, feature_set):
        self.threshold = thr
        self.train_data = dataset
        self.features = feature_set

        build_tree(self.train_data, self.features, Decision_Tree.Tree)

    def get_max_key(in_list):
        flag = 0
        out_key = 0
        for i in range(len(in_list)):
            if in_list[i] >= flag:
                flag = in_list[i]
                out_key = i

        return out_key

    def majority_decide(dataset, features):
        pos_value = features["label"]
        count_list = [0 for i in range(pos_value)]

        for item in range(len(dataset)):
            temp_num = dataset[item]["label"]
            count_list[temp_num] = count_list[temp_num] + 1

        out_label = get_max_key(count_list)
        return out_label

    def count_igr(train_data, features):
        features_name = []
        for key in features:
            features_name.append(key)

        features_dict = {}
        H_features = {}
        H_one_features = {}
        features_dict.fromkeys(features_name, 0.0)
        H_features.fromkeys(features_name, 0.0)
        H_one_features.fromkeys(features_name, 0.0)

        H_dataset = 0.0

    def build_tree(train_data, features, decision_tree):
        # 训练集要包含如下元素：特征名称和特征值，为一个列表嵌套字典
        # 特征集为一个字典，字典的键为特征名称和“label”，键值为该特征或标签的取值
        # 因为这个程序为一个递归程序，所以decision_tree这个传过来的参数
        # 可能仅仅是树的一个分支，经过ipython的test
        # python中的传值皆为对象，相当于一个引用

        ifequal = True
        flag = train_data[0]["label"]
        for item in range(len(train_data)):
            if flag != train_data[item]["label"]:
                ifequal = False
                break
        if ifequal:
            decision_tree.update({"no_feature": flag})
            return decision_tree

        if len(features) == 0:
            this_1_label = majority_decide(train_data, features)
            decision_tree.update({"no_feature": this_1_label})
            return decision_tree

        feature, igr = count_igr(train_data, features)

        if igr < self.threshold:
            this_2_label = majority_decide(train_data, features)
            decision_tree.update({"no_feature": this_2_label})
            return decision_tree

        creat_list_num = features[feature]
        creat_list = [0 for j in range(creat_list_num)]
        decision_tree.update({feature: creat_list})
        for cnt in range(creat_list_num):
            creat_list[cnt] = {}
            processed_train_data = []
            for it in range(len(train_data)):
                if train_data[it][feature] != cnt:
                    processed_train_data.append(train_data[it])
                else:
                    continue

            processed_features = {}
            processed_features.copy(features)
            processed_features.pop(feature)

            decision_tree[feature]
            build_tree(processed_train_data, processed_features,
                       decision_tree[feature][cnt])
