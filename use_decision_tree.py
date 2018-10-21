import csv
import math
import time
import matplotlib.pyplot as plt


class Decision_Tree:
    'The data structure of decision tree is very nb'

    Tree = {}
    out_label = 0

    def __init__(self, thr):
        self.Threshold = thr

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

    def build_tree(self, train_data, features, decision_tree):
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

        if len(features) == 0:
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

            self.build_tree(processed_train_data, processed_features,
                            decision_tree[feature][cnt])

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


def read_train_data(filename):
    csvFile = open(filename, "r")
    reader = csv.reader(csvFile)

    output = [[1 for j in range(1, 12)] for i in range(1, 892)]
    num = 0
    for item in reader:
        if reader.line_num == 1:
            continue
        for cnt in range(11):
            output[num][cnt] = item[cnt + 1]
        num = num + 1

    train_data = [[1 for j in range(1, 12)] for i in range(1, 761)]
    test_data = [[1 for j in range(1, 12)] for i in range(1, 132)]

    for i in range(891):
        if i < 760:
            for t in range(11):
                train_data[i][t] = output[i][t]
        else:
            for r in range(11):
                test_data[i - 760][r] = output[i - 760][r]

    csvFile.close()
    return train_data, test_data


def process_data(data):

    train_data = []
    features = {}
    features_name = ["pclass", "sex", "age", "sibsp",
                     "parch", "fare", "embarked", "label"]
    features.fromkeys(features_name, 0)

    features['pclass'] = 3
    features['sex'] = 2
    features['age'] = 6
    features['sibsp'] = 3
    features['parch'] = 3
    features['fare'] = 7
    features['embarked'] = 3
    features['label'] = 2

    for cnt in range(len(data)):
        one_data = {}

        # 0
        data[cnt][0] = int(data[cnt][0])
        one_data.update({"label": data[cnt][0]})

        # 1
        if data[cnt][1] == '':
            data[cnt][1] = 2
        elif data[cnt][1] == 1:
            data[cnt][1] = 0
        elif data[cnt][1] == 2:
            data[cnt][1] = 1
        else:
            data[cnt][1] = 2
        # pclass.append(data[cnt][1])
        one_data.update({"pclass": data[cnt][1]})

        # 3
        if data[cnt][3] == '':
            if data[cnt][0] == 0:
                data[cnt][3] = "female"
            else:
                data[cnt][3] = "male"
        if data[cnt][3] == 'male':
            data[cnt][3] = 0
        else:
            data[cnt][3] = 1
        # sex.append(data[cnt][3])
        one_data.update({"sex": data[cnt][3]})

        # 4
        if data[cnt][4] == '':
            data[cnt][4] = 18
        data[cnt][4] = float(data[cnt][4])
        if data[cnt][4] <= 3:
            data[cnt][4] = 0
        elif data[cnt][4] <= 10 and data[cnt][4] > 3:
            data[cnt][4] = 1
        elif data[cnt][4] <= 18 and data[cnt][4] > 10:
            data[cnt][4] = 2
        elif data[cnt][4] <= 35 and data[cnt][4] > 18:
            data[cnt][4] = 3
        elif data[cnt][4] <= 65 and data[cnt][4] > 35:
            data[cnt][4] = 4
        elif data[cnt][4] > 65:
            data[cnt][4] = 5
        # age.append(data[cnt][4])
        one_data.update({"age": data[cnt][4]})

        # 5
        if data[cnt][5] == '':
            data[cnt][5] = 0
        data[cnt][5] = int(data[cnt][5])
        if data[cnt][5] >= 3:
            data[cnt][5] = 2
        # sibsp.append(data[cnt][5])
        one_data.update({"sibsp": data[cnt][5]})

        # 6
        if data[cnt][6] == '':
            data[cnt][6] = 0
        data[cnt][6] = int(data[cnt][6])
        if data[cnt][6] >= 3:
            data[cnt][6] = 2
        # parch.append(data[cnt][6])
        one_data.update({"parch": data[cnt][6]})

        # 8
        if data[cnt][8] == '':
            data[cnt][8] = 5.0
        data[cnt][8] = float(data[cnt][8])

        if data[cnt][8] <= 7.8:
            data[cnt][8] = 0
        elif data[cnt][8] > 7.8 and data[cnt][8] <= 8.6:
            data[cnt][8] = 1
        elif data[cnt][8] > 8.6 and data[cnt][8] <= 12:
            data[cnt][8] = 2
        elif data[cnt][8] > 12 and data[cnt][8] <= 20:
            data[cnt][8] = 3
        elif data[cnt][8] > 20 and data[cnt][8] <= 36:
            data[cnt][8] = 4
        elif data[cnt][8] > 36 and data[cnt][8] <= 58:
            data[cnt][8] = 5
        else:
            data[cnt][8] = 6
        # fare.append(data[cnt][8])
        one_data.update({"fare": data[cnt][8]})

        # 10
        if data[cnt][10] == '':
            data[cnt][10] = 'S'
        if data[cnt][10] == 'S':
            data[cnt][10] = 0
        elif data[cnt][10] == 'Q':
            data[cnt][10] = 1
        else:
            data[cnt][10] = 2
        # embarked.append(data[cnt][10])
        one_data.update({"embarked": data[cnt][10]})

        # print(one_data)
        train_data.append(one_data)

    arr_x = []
    for j in range(len(data)):
        arr_x.append(j)
    arr_y = []
    for h in range(len(data)):
        arr_y.append(data[h][8])
    plt.figure('Analysis')
    ax = plt.gca()
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.scatter(arr_x, arr_y, c='r', s=1, alpha=1)
    # plt.show()
    # plt.waitforbuttonpress()

    # print(len(train_data))

    return train_data, features


def process_test_data(test_data):
    test_data_for_process, unused_features = process_data(test_data)
    out_test_data = []
    labels = []
    for item in range(len(test_data_for_process)):
        labels.append(test_data_for_process[item]["label"])
        test_data_for_process[item].pop("label")
        out_test_data.append(test_data_for_process[item])

    return out_test_data, labels


if __name__ == "__main__":

    fn = "dataset/train.csv"
    train_test, test_test = read_train_data(fn)
    train_data, features = process_data(train_test)
    # print(train_data)
    test_tree = Decision_Tree(0.01)
    test_tree.build_tree(train_data, features, test_tree.Tree)
    out_test_data, labels = process_test_data(test_test)

    num = 0
    for cnt in range(len(out_test_data)):
        input_list = out_test_data[cnt]
        output_value = test_tree.predict(input_list)
        if output_value == labels[cnt]:
            num = num + 1

    accuracy = (num / len(out_test_data)) * 100.0
    print("The accuracy is %.3f" % accuracy, "%.")
