import time
import csv
import math
import matplotlib.pyplot as plt


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

    train_data = [[1 for j in range(1, 12)] for i in range(1, 701)]
    test_data = [[1 for j in range(1, 12)] for i in range(1, 192)]

    for i in range(891):
        if i < 700:
            for t in range(11):
                train_data[i][t] = output[i][t]
        else:
            for r in range(11):
                test_data[i - 700][r] = output[i - 700][r]

    csvFile.close()
    return train_data, test_data


def process_data(data):
    label = []

    pclass = []
    sex = []
    age = []
    sibsp = []
    parch = []
    fare = []
    embarked = []

    for cnt in range(len(data)):
        # 0
        data[cnt][0] = int(data[cnt][0])
        label.append(data[cnt][0])

        # 1
        if data[cnt][1] == '':
            data[cnt][1] = 3
        data[cnt][1] = int(data[cnt][1])
        pclass.append(data[cnt][1])

        # 3
        if data[cnt][3] == '':
            if data[cnt][0] == 1:
                data[cnt][3] = "female"
            else:
                data[cnt][3] = "male"
        if data[cnt][3] == 'male':
            data[cnt][3] = 1
        else:
            data[cnt][3] = 2
        sex.append(data[cnt][3])

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
        age.append(data[cnt][4])

        # 5
        if data[cnt][5] == '':
            data[cnt][5] = 0
        data[cnt][5] = int(data[cnt][5])
        if data[cnt][5] >= 3:
            data[cnt][5] = 3
        sibsp.append(data[cnt][5])

        # 6
        if data[cnt][6] == '':
            data[cnt][6] = 0
        data[cnt][6] = int(data[cnt][6])
        if data[cnt][6] >= 3:
            data[cnt][6] = 3
        parch.append(data[cnt][6])

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
        fare.append(data[cnt][8])

        # 10
        if data[cnt][10] == '':
            data[cnt][10] = 'S'
        if data[cnt][10] == 'S':
            data[cnt][10] = 1
        elif data[cnt][10] == 'Q':
            data[cnt][10] = 2
        else:
            data[cnt][10] = 3
        embarked.append(data[cnt][10])

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
    ax.scatter(arr_x, arr_y, c = 'r', s = 1, alpha = 1)
    plt.show()
    # plt.waitforbuttonpress()

    return label, pclass, sex, age, sibsp, parch, fare, embarked


def count_IGR(label, pclass, sex, age, sibsp, parch, fare, embarked):
    outmap =  {
        'pclass':(pclass, 0.0), 
        'sex':(sex, 0.0), 
        'age':(age, 0.0), 
        'sibsp':(sibsp, 0.0), 
        'parch':(parch, 0.0), 
        'fare':(fare, 0.0), 
        'embarked':(embarked, 0.0)
    }

    dataset_entropy = 0.0
    cnt_0 = 0
    cnt_1 = 0
    for i in range(len(label)):
        if label[i] == 0:
            cnt_0 = cnt_0 + 1
        else:
            cnt_1 = cnt_1 + 1
    dataset_entropy = ( - ((cnt_0/len(label)) * math.log2(cnt_0/len(label)))) + \
        ( - ((cnt_1/len(label)) * math.log2(cnt_1/len(label))))

    print(dataset_entropy)
    print(outmap["age"])


if __name__ == "__main__":

    fn = "dataset/train.csv"
    train_test, test_test = read_train_data(fn)
    label, pclass, sex, age, sibsp, parch, fare, embarked = process_data(
        train_test)
    count_IGR(label, pclass, sex, age, sibsp, parch, fare, embarked)
