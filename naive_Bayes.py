import numpy as np
import jieba
import time
import math


# read the stop word list
def init_stopwords():
    stopwords_file = open('stopwords.txt', 'r', encoding='UTF-8')
    stopwords_list = []
    for line in stopwords_file.readlines():
        # if '\n' in line:
        #     cnt = 0
        #     for ele in line:
        #         cnt = cnt + 1
        #         if ele == '\\':
        #             # print(ele)
        #             break
        #     line = line[:cnt-1]
        #     # print(line)
        # print(line.strip("\n"))
        # print(line)
        line = line.strip("\n")
        stopwords_list.append(line)
    # print(stopwords_list)
    # print(stopwords_list[0])
    swList = np.array(stopwords_list)
    return swList


# Use jieba library to devide words
def devide_words(raw_word, swList):
    # use jieba
    # words = np.array(jieba.cut(raw_word, cut_all=False))
    words = list(jieba.cut(raw_word, cut_all=False))
    # print(words)
    # swList.tolist()
    # print(swList)
    copy_words = words[:]
    for word in words:
        # print(word)
        if word in swList:
            # print("Done")
            # print(word)
            # Woc, 这个bug是真tm坑人啊
            copy_words.remove(word)

    temp = '\n'
    if temp in copy_words:
        # words.remove('\n')
        copy_words.remove('\n')
    #words = np.array(words)
    copy_words = np.array(copy_words)
    return copy_words


def loadtoFiles():
    # Devide data into two parts
    # One is training data, the other is test data
    # The number of training data is 4000, the number of test data is 1000

    # file name
    file_input = 'news_data.txt'
    file_output_test_labels = 'C:/Users/28012/Desktop/Statistical Learning/naive Bayes/'
    file_output_test_labels = file_output_test_labels + \
        "Dataset/test_labels.txt"

    file_output_training_car = 'C:/Users/28012/Desktop/Statistical Learning/naive Bayes/'
    file_output_training_car = file_output_training_car + \
        'Dataset/train_data_car.txt'
    file_output_test_car = 'C:/Users/28012/Desktop/Statistical Learning/naive Bayes/'
    file_output_test_car = file_output_test_car + \
        'Dataset/test_data_car.txt'

    file_output_training_finance = 'C:/Users/28012/Desktop/Statistical Learning/naive Bayes/'
    file_output_training_finance = file_output_training_finance + \
        'Dataset/train_data_finance.txt'
    file_output_test_finance = 'C:/Users/28012/Desktop/Statistical Learning/naive Bayes/'
    file_output_test_finance = file_output_test_finance + \
        'Dataset/test_data_finance.txt'

    file_output_training_science = 'C:/Users/28012/Desktop/Statistical Learning/naive Bayes/'
    file_output_training_science = file_output_training_science + \
        'Dataset/train_data_science.txt'
    file_output_test_science = 'C:/Users/28012/Desktop/Statistical Learning/naive Bayes/'
    file_output_test_science = file_output_test_science + \
        'Dataset/test_data_science.txt'

    file_output_training_health = 'C:/Users/28012/Desktop/Statistical Learning/naive Bayes/'
    file_output_training_health = file_output_training_health + \
        'Dataset/train_data_health.txt'
    file_output_test_health = 'C:/Users/28012/Desktop/Statistical Learning/naive Bayes/'
    file_output_test_health = file_output_test_health + \
        'Dataset/test_data_health.txt'

    file_output_training_sports = 'C:/Users/28012/Desktop/Statistical Learning/naive Bayes/'
    file_output_training_sports = file_output_training_sports + \
        'Dataset/train_data_sports.txt'
    file_output_test_sports = 'C:/Users/28012/Desktop/Statistical Learning/naive Bayes/'
    file_output_test_sports = file_output_test_sports + \
        'Dataset/test_data_sports.txt'

    file_output_training_education = 'C:/Users/28012/Desktop/Statistical Learning/naive Bayes/'
    file_output_training_education = file_output_training_education + \
        'Dataset/train_data_education.txt'
    file_output_test_education = 'C:/Users/28012/Desktop/Statistical Learning/naive Bayes/'
    file_output_test_education = file_output_test_education + \
        'Dataset/test_data_education.txt'

    file_output_training_culture = 'C:/Users/28012/Desktop/Statistical Learning/naive Bayes/'
    file_output_training_culture = file_output_training_culture + \
        'Dataset/train_data_culture.txt'
    file_output_test_culture = 'C:/Users/28012/Desktop/Statistical Learning/naive Bayes/'
    file_output_test_culture = file_output_test_culture + \
        'Dataset/test_data_culture.txt'

    file_output_training_military = 'C:/Users/28012/Desktop/Statistical Learning/naive Bayes/'
    file_output_training_military = file_output_training_military + \
        'Dataset/train_data_military.txt'
    file_output_test_military = 'C:/Users/28012/Desktop/Statistical Learning/naive Bayes/'
    file_output_test_military = file_output_test_military + \
        'Dataset/test_data_military.txt'

    file_output_training_joy = 'C:/Users/28012/Desktop/Statistical Learning/naive Bayes/'
    file_output_training_joy = file_output_training_joy + \
        'Dataset/train_data_joy.txt'
    file_output_test_joy = 'C:/Users/28012/Desktop/Statistical Learning/naive Bayes/'
    file_output_test_joy = file_output_test_joy + \
        'Dataset/test_data_joy.txt'

    file_output_training_fashion = 'C:/Users/28012/Desktop/Statistical Learning/naive Bayes/'
    file_output_training_fashion = file_output_training_fashion + \
        'Dataset/train_data_fashion.txt'
    file_output_test_fashion = 'C:/Users/28012/Desktop/Statistical Learning/naive Bayes/'
    file_output_test_fashion = file_output_test_fashion + \
        'Dataset/test_data_fashion.txt'

    # Initialization
    data = open(file_input, 'r', encoding='UTF-8')
    labels = open(file_output_test_labels, "w")
    swList = init_stopwords()
    # print(swList)

    train_set_car = []
    f_train_car = open(file_output_training_car, "w")
    f_test_car = open(file_output_test_car, "w")

    train_set_finance = []
    f_train_finance = open(file_output_training_finance, "w")
    f_test_finance = open(file_output_test_finance, "w")

    train_set_science = []
    f_train_science = open(file_output_training_science, "w")
    f_test_science = open(file_output_test_science, "w")

    train_set_health = []
    f_train_health = open(file_output_training_health, "w")
    f_test_health = open(file_output_test_health, "w")

    train_set_sports = []
    f_train_sports = open(file_output_training_sports, "w")
    f_test_sports = open(file_output_test_sports, "w")

    train_set_education = []
    f_train_education = open(file_output_training_education, "w")
    f_test_education = open(file_output_test_education, "w")

    train_set_culture = []
    f_train_culture = open(file_output_training_culture, "w")
    f_test_culture = open(file_output_test_culture, "w")

    train_set_military = []
    f_train_military = open(file_output_training_military, "w")
    f_test_military = open(file_output_test_military, "w")

    train_set_joy = []
    f_train_joy = open(file_output_training_joy, "w")
    f_test_joy = open(file_output_test_joy, "w")

    train_set_fashion = []
    f_train_fashion = open(file_output_training_fashion, "w")
    f_test_fashion = open(file_output_test_fashion, "w")

    cnt1 = 0
    cnt2 = 0
    cnt3 = 0
    cnt4 = 0
    cnt5 = 0
    cnt6 = 0
    cnt7 = 0
    cnt8 = 0
    cnt9 = 0
    cnt10 = 0

    cnt = 0

    for line in data.readlines():
        if line[0] == '汽' and line[1] == '车':
            # print("get")
            cnt1 = cnt1 + 1
            # print(words)
            # print(words)
            if cnt1 <= 400:
                line = line[3:]
                words = devide_words(line, swList)
                words = words.tolist()
                train_set_car.extend(words)
            else:
                labels.write("汽车")
                labels.write('\n')
                line = line[3:]
                words = devide_words(line, swList)
                words = words.tolist()
                for word in words:
                    f_test_car.write(word + " ")
                f_test_car.write('\n')
        elif line[0] == '财' and line[1] == '经':
            # print("get")
            cnt2 = cnt2 + 1
            if cnt2 <= 400:
                line = line[3:]
                words = devide_words(line, swList)
                words = words.tolist()
                train_set_finance.extend(words)
            else:
                labels.write("财经")
                labels.write('\n')
                line = line[3:]
                words = devide_words(line, swList)
                words = words.tolist()
                for word in words:
                    f_test_finance.write(word + " ")
                f_test_finance.write('\n')
        elif line[0] == '科' and line[1] == '技':
            cnt3 = cnt3 + 1
            if cnt3 <= 400:
                line = line[3:]
                words = devide_words(line, swList)
                words = words.tolist()
                train_set_science.extend(words)
            else:
                labels.write("科技")
                labels.write('\n')
                line = line[3:]
                words = devide_words(line, swList)
                words = words.tolist()
                for word in words:
                    f_test_science.write(word + " ")
                f_test_science.write('\n')
        elif line[0] == '健' and line[1] == '康':
            cnt4 = cnt4 + 1
            if cnt4 <= 400:
                line = line[3:]
                words = devide_words(line, swList)
                words = words.tolist()
                train_set_health.extend(words)
            else:
                labels.write("健康")
                labels.write('\n')
                line = line[3:]
                words = devide_words(line, swList)
                words = words.tolist()
                for word in words:
                    f_test_health.write(word + " ")
                f_test_health.write('\n')
        elif line[0] == '体' and line[1] == '育':
            cnt5 = cnt5 + 1
            if cnt5 <= 400:
                line = line[3:]
                words = devide_words(line, swList)
                words = words.tolist()
                train_set_sports.extend(words)
            else:
                labels.write("体育")
                labels.write('\n')
                line = line[3:]
                words = devide_words(line, swList)
                words = words.tolist()
                for word in words:
                    f_test_sports.write(word + " ")
                f_test_sports.write('\n')
        elif line[0] == '教' and line[1] == '育':
            cnt6 = cnt6 + 1
            if cnt6 <= 400:
                line = line[3:]
                words = devide_words(line, swList)
                words = words.tolist()
                train_set_education.extend(words)
            else:
                labels.write("教育")
                labels.write('\n')
                line = line[3:]
                words = devide_words(line, swList)
                words = words.tolist()
                for word in words:
                    f_test_education.write(word + " ")
                f_test_education.write('\n')
        elif line[0] == '文' and line[1] == '化':
            cnt7 = cnt7 + 1
            if cnt7 <= 400:
                line = line[3:]
                words = devide_words(line, swList)
                words = words.tolist()
                train_set_culture.extend(words)
            else:
                labels.write("文化")
                labels.write('\n')
                line = line[3:]
                words = devide_words(line, swList)
                words = words.tolist()
                for word in words:
                    f_test_culture.write(word + " ")
                f_test_culture.write('\n')
        elif line[0] == '军' and line[1] == '事':
            cnt8 = cnt8 + 1
            if cnt8 <= 400:
                line = line[3:]
                words = devide_words(line, swList)
                words = words.tolist()
                train_set_military.extend(words)
            else:
                labels.write("军事")
                labels.write('\n')
                line = line[3:]
                words = devide_words(line, swList)
                words = words.tolist()
                for word in words:
                    f_test_military.write(word + " ")
                f_test_military.write('\n')
        elif line[0] == '娱' and line[1] == '乐':
            cnt9 = cnt9 + 1
            if cnt9 <= 400:
                line = line[3:]
                words = devide_words(line, swList)
                words = words.tolist()
                train_set_joy.extend(words)
            else:
                labels.write("娱乐")
                labels.write('\n')
                line = line[3:]
                words = devide_words(line, swList)
                words = words.tolist()
                for word in words:
                    f_test_joy.write(word + " ")
                f_test_joy.write('\n')
        elif line[0] == '时' and line[1] == '尚':
            cnt10 = cnt10 + 1
            if cnt10 <= 400:
                line = line[3:]
                words = devide_words(line, swList)
                words = words.tolist()
                train_set_fashion.extend(words)
            else:
                labels.write("时尚")
                labels.write('\n')
                line = line[3:]
                words = devide_words(line, swList)
                words = words.tolist()
                for word in words:
                    f_test_fashion.write(word + " ")
                f_test_fashion.write('\n')

        cnt = cnt + 1
        if cnt % 1000 == 0:
            print("%d done" % cnt)

    # print(train_set_car[0])
    # print(train_set_car[1])
    # print(train_set_car[12])
    # print(cnt)

    # print(train_set_car.tostring())
    # train_set_car = str(train_set_car, encoding='utf-8')
    # test_set_car = str(test_set_car.tostring())
    for word in train_set_car:
        f_train_car.write(word + " ")
    # f_test_car.write(test_set_car)
    # print(train_set_car)
    f_train_car.close()
    f_test_car.close()

    for word in train_set_finance:
        f_train_finance.write(word + " ")
    f_train_finance.close()
    f_test_finance.close()

    for word in train_set_science:
        f_train_science.write(word + " ")
    f_train_science.close()
    f_test_science.close()

    for word in train_set_health:
        f_train_health.write(word + " ")
    f_train_health.close()
    f_test_health.close()

    for word in train_set_sports:
        f_train_sports.write(word + " ")
    f_train_sports.close()
    f_test_sports.close()

    for word in train_set_education:
        f_train_education.write(word + " ")
    f_train_education.close()
    f_test_education.close()

    for word in train_set_culture:
        f_train_culture.write(word + " ")
    f_train_culture.close()
    f_test_culture.close()

    for word in train_set_military:
        f_train_military.write(word + " ")
    f_train_military.close()
    f_test_military.close()

    for word in train_set_joy:
        f_train_joy.write(word + " ")
    f_train_joy.close()
    f_test_joy.close()

    for word in train_set_fashion:
        f_train_fashion.write(word + " ")
    f_train_fashion.close()
    f_test_fashion.close()

    print("\n")


# def init():
#     # Initial dictionary
#     # init_arr = np.zeros(10)
#     # print(init_arr)
#     temp_dic = {}
#     word_set_dic = temp_dic.fromkeys(string_of_class)
#     print(word_set_dic)

# temp_dic = {}
# word_set_dic = temp_dic.fromkeys(string_of_class)
# print(word_set_dic)


def load_test_label():

    file_labels = 'C:/Users/28012/Desktop/Statistical Learning/naive Bayes/'
    file_labels = file_labels + "Dataset/test_labels.txt"

    # f_label = open(file_labels, 'r', encoding='UTF-8')
    return file_labels


def load_test_file(own_class):

    file_input_name = "C:/Users/28012/Desktop/Statistical Learning/naive Bayes/"
    file_input_name = file_input_name + 'Dataset/test_data_' + own_class + '.txt'

    # f_test = open(file_input_name, 'r', encoding='UTF-8')
    return file_input_name


def load_train_file(own_class):

    file_input_name = "C:/Users/28012/Desktop/Statistical Learning/naive Bayes/"
    file_input_name = file_input_name + 'Dataset/train_data_' + own_class + '.txt'

    # f_test = open(file_input_name, 'r', encoding='UTF-8')
    return file_input_name

# Test


def count_word_train(file_class, name_class):

    word_list = np.loadtxt(file_class, str)
    # print(len(word_list))
    # print(type(word_list))
    # print(word_list)
    word_list = word_list.tolist()
    # print(type(word_list))
    # print(word_list)
    # print(len(word_list))
    # print(word_set_dic)
    if name_class in word_set_dic:
        word_set_dic[name_class] = {}
    else:
        print("ERROR")
        return
    for word in word_list:
        if word in word_set_dic[name_class]:
            word_set_dic[name_class][word] += 1
        else:
            word_set_dic[name_class][word] = 1

    # """ Function Programming """
    # sorted_list = sorted(word_set_dic[name_class].items(
    # ), key=lambda item: item[1], reverse=True)
    # # print(sorted_list)

    # print(word_set_dic)
    return name_class


def Change_list_to_dict(list_process):

    # cnt = 0
    # out_dict = {}
    out_dict_test = {}
    list_key = {}
    # list_key_name = []
    list_key_test = []
    # list_value = []

    t3 = time.clock()
    print("list_process's length is %d" % len(list_process))
    for num in range(len(list_process)):
        # ifok = 0
        # cnt = 0
        # t1 = time.clock()

        # # print(num)
        # # print(len(list_key))
        # for c in range(len(list_key)):
        #     if list_process[num][0] == list_key[c][0]:
        #         ifok = 1
        #         cnt = c
        #         # print("Done")
        #         break

        # if ifok:
        #     # Tuple can't be write
        #     list_key[cnt][1] = list_key[cnt][1] + list_process[num][1]
        # else:
        #     list_key.append([list_process[num][0], list_process[num][1]])

        # # if list_process[num][0] in list_key:
        list_key_test.append(list_process[num][0])

        if list_process[num][0] not in list_key:
            list_key[list_process[num][0]] = list_process[num][1]
        else:
            list_key[list_process[num][0]] += list_process[num][1]

        # t2 = time.clock()
        # print(t2-t1)

    t4 = time.clock()
    print(t4-t3)
    # print(list_key)
    print("list_key's length is %d" % len(list_key))
    # cnt = 0
    out_dict_test = out_dict_test.fromkeys(list_key_test, 0)
    print("out_dict_test's length is %d" % len(out_dict_test))
    if len(out_dict_test) == len(list_key):
        print("Right")

    # for key in out_dict.keys():
    #     n = 0
    #     t1 = time.clock()
    #     for i in range(len(list_process)):
    #         if list_process[i][0] == key:
    #             n = n + list_process[i][1]
    #             # print("Done")

    #     t2 = time.clock()
    #     print(t2-t1)
    #     out_dict[key] = n
    #     # cnt = cnt + 1

    # for j in range(len(list_key)):
    #     list_key_name.append(list_key[j][0])

    # out_dict = out_dict.fromkeys(list_key_name)
    # for k in range(len(list_key)):
    #     if list_key[k][0] in out_dict.keys():
    #         out_dict[list_key[k][0]] = list_key[k][1]
    #     else:
    #         print("ERROR")

    # print("out_dict's length is %d" % len(out_dict_test))
    out_dict = list_key.copy()
    return out_dict


def process_train_word(file_class, name_class):

    word_list = np.loadtxt(file_class, str)
    # print(len(word_list))
    # print(type(word_list))
    # print(word_list)
    word_list = word_list.tolist()
    # print(type(word_list))
    # print(word_list)
    # print(len(word_list))
    # print(word_set_dic)
    cnt = 0
    if name_class in word_set_dic:
        word_set_dic[name_class] = {}
    else:
        print("ERROR")
        return
    for word in word_list:
        cnt = cnt + 1
        if word in word_set_dic[name_class]:
            word_set_dic[name_class][word] += 1
        else:
            word_set_dic[name_class][word] = 1

    """ Function Programming """
    sorted_list = sorted(word_set_dic[name_class].items(
    ), key=lambda item: item[1], reverse=True)
    # print(sorted_list)

    # # print(cnt)
    # copy = word_set_dic[name_class].copy()
    # for key in copy.keys():
    #     copy[key] = copy[key]/cnt

    # """ Function Programming """
    # sorted_copy_list = sorted(
    #     copy.items(), key=lambda item: item[1], reverse=True)
    # # print(sorted_copy_list)
    # print(word_set_dic)

    return word_set_dic[name_class], sorted_list, cnt


def calculate_B(A):
    # d_len = len(dict_all)
    # l_len = len(list_class)

    # times = d_len / l_len
    # for cnt in range(len(list_class)):
    #     if list_class[cnt][0] in dict_all:
    #         word = list_class[cnt][0]
    #         A = 1000*(list_class[cnt][1]/l_len)
    #         B = 1000*(dict_all[word]/d_len)
    #         print("The value of A is %d" % A)
    #         print("The value of B is %d" % B)

    #         X2 = A*()-B*()

    #     else:
    #         print("All_dict don't contain all the elements.")

    B = {}
    for key in A:
        B[key] = {}
        for word in A[key]:
            B[key][word] = 0

            for key_value in A:
                if key_value != key and (word in A[key_value]):
                    B[key][word] += A[key_value][word]
    return B


# A is a element of CHI; B is a element of CHI
# count is a storage of one class's number
# N is all the number
# word_set is a dictionary for all the word
def feature_select_use_new_CHI(A, B, count, N, word_set):

    # word_dict = []
    word_features = {}

    string_of_class = ['car',
                       'finance',
                       'science',
                       'health',
                       'sports',
                       'education',
                       'culture',
                       'military',
                       'joy',
                       'fashion']

    word_features = word_features.fromkeys(string_of_class)

    for num in range(len(string_of_class)):

        CHI = {}
        name = string_of_class[num]
        M = N - count[num]

        for word in A[name]:
            chi_t_1 = A[name][word] * (M - B[name][word]) - \
                (count[num] - A[name][word]) * B[name][word]
            chi_t_2 = math.pow(chi_t_1, 2)
            chi_t_3 = (A[name][word] + B[name][word]) * \
                (N - A[name][word] - B[name][word])
            chi_t_4 = (chi_t_2 / chi_t_3)

            CHI[word] = math.log10(
                N / (A[name][word] + B[name][word])) * chi_t_4
            # print(CHI[word])

        """ Function Programming """
        # sorted_list = sorted(word_set_dic[name_class].items(
        # ), key=lambda item: item[1], reverse=True)
        # # print(sorted_list)
        sorted_list = sorted(
            CHI.items(), key=lambda item: item[1], reverse=True)
        sorted_list = sorted_list[:200]
        # print(len(sorted_list))
        # print(sorted_list)

        # b = []
        # for aa in a:
        #     b.append(aa[0])
        # word_dict.extend(b)
        # for word in word_dict:
        #     if word not in word_features:
        #         word_features.append(word)

        word_features[name] = {}
        for u in range(len(sorted_list)):
            if sorted_list[u][0] in word_set[name]:
                w = sorted_list[u][0]
                word_features[name][w] = word_set[name][w]
            else:
                print("ERROR")

    print("The value of CHI has been counted.")
    return word_features


def bulid_dict_for_one_class(l, d1, d2, d3, d4, d5, d6, d7, d8, d9, d10):
    out = {}

    for u in range(len(l)):
        # print(d1)

        cnt = 0
        temp = l[u][0]
        # print(temp)
        # cnt = True
        cnt += int(temp in d1)
        cnt += int(temp in d2)
        cnt += int(temp in d3)
        cnt += int(temp in d4)
        cnt += int(temp in d5)
        cnt += int(temp in d6)
        cnt += int(temp in d7)
        cnt += int(temp in d8)
        cnt += int(temp in d9)
        cnt += int(temp in d10)
        # print(cnt)

        out[temp] = cnt

    return out


def count_tf_idf(word_features, count):

    string_of_class = ['car',
                       'finance',
                       'science',
                       'health',
                       'sports',
                       'education',
                       'culture',
                       'military',
                       'joy',
                       'fashion']

    out = {}
    out = out.fromkeys(string_of_class)

    for num in range(len(string_of_class)):
        class_name = string_of_class[num]
        out[class_name] = {}

        for word in word_features[class_name]:

            word_file = 0
            for c_n in word_features:
                if word in word_features[c_n]:
                    word_file = word_file + 1
            # print(word_file)

            # print(word_features[class_name][word])
            # print(count[num])
            tf = word_features[class_name][word] / count[num]
            idf = math.log10(10 / word_file)
            tf_idf = tf * idf * 1000000

            out[class_name][word] = tf_idf + 1

    # """ Function Programming """
    # sorted_list = sorted(out["car"].items(
    # ), key=lambda item: item[1], reverse=True)
    # print(sorted_list)
    # print(len(sorted_list))

    # print(out)
    print("The value of tf-idf has been counted.")
    return out


def naiveBayes():

    # print(word_set_dic)
    # print(word_set_dic)
    # print(count_word_train(f_train_car, 'car') + " Done")
    # print(wd)
    # print(nc)

    string_of_class = ['car',
                       'finance',
                       'science',
                       'health',
                       'sports',
                       'education',
                       'culture',
                       'military',
                       'joy',
                       'fashion']

    f_train_car = load_train_file('car')
    f_train_finance = load_train_file('finance')
    f_train_science = load_train_file('science')
    f_train_health = load_train_file('health')
    f_train_sports = load_train_file('sports')
    f_train_education = load_train_file('education')
    f_train_culture = load_train_file('culture')
    f_train_military = load_train_file('military')
    f_train_joy = load_train_file('joy')
    f_train_fashion = load_train_file('fashion')

    print(count_word_train(f_train_car, 'car') + " Done")
    print(count_word_train(f_train_finance, 'finance') + " Done")
    print(count_word_train(f_train_science, 'science') + " Done")
    print(count_word_train(f_train_health, 'health') + " Done")
    print(count_word_train(f_train_sports, 'sports') + " Done")
    print(count_word_train(f_train_education, 'education') + " Done")
    print(count_word_train(f_train_culture, 'culture') + " Done")
    print(count_word_train(f_train_military, 'military') + " Done")
    print(count_word_train(f_train_joy, 'joy') + " Done")
    print(count_word_train(f_train_fashion, 'fashion') + " Done")

    d1, l1, n1 = process_train_word(f_train_car, "car")
    d2, l2, n2 = process_train_word(f_train_finance, 'finance')
    d3, l3, n3 = process_train_word(f_train_science, 'science')
    d4, l4, n4 = process_train_word(f_train_health, 'health')
    d5, l5, n5 = process_train_word(f_train_sports, 'sports')
    d6, l6, n6 = process_train_word(f_train_education, 'education')
    d7, l7, n7 = process_train_word(f_train_culture, 'culture')
    d8, l8, n8 = process_train_word(f_train_military, 'military')
    d9, l9, n9 = process_train_word(f_train_joy, 'joy')
    d10, l10, n10 = process_train_word(f_train_fashion, 'fashion')

    # print(d1)
    # num = n1 + n2 + n3 + n4 + n5 + n6 + n7 + n8 + n9 + n10
    all_list = l1 + l2 + l3 + l4 + l5 + l6 + l7 + l8 + l9 + l10
    count = [n1, n2, n3, n4, n5, n6, n7, n8, n9, n10]
    # print(count)
    # print(num)
    # print(len(all_list))

    all_dict = Change_list_to_dict(all_list)

    # For count CHI
    all_class_dict = {}
    N = len(all_dict)
    # print(N)

    word_set = {}
    word_set = word_set.fromkeys(string_of_class)
    word_set[string_of_class[0]] = d1
    word_set[string_of_class[1]] = d2
    word_set[string_of_class[2]] = d3
    word_set[string_of_class[3]] = d4
    word_set[string_of_class[4]] = d5
    word_set[string_of_class[5]] = d6
    word_set[string_of_class[6]] = d7
    word_set[string_of_class[7]] = d8
    word_set[string_of_class[8]] = d9
    word_set[string_of_class[9]] = d10
    # print(word_set)

    c1 = bulid_dict_for_one_class(l1, d1, d2, d3, d4, d5, d6, d7, d8, d9, d10)
    c2 = bulid_dict_for_one_class(l2, d1, d2, d3, d4, d5, d6, d7, d8, d9, d10)
    c3 = bulid_dict_for_one_class(l3, d1, d2, d3, d4, d5, d6, d7, d8, d9, d10)
    c4 = bulid_dict_for_one_class(l4, d1, d2, d3, d4, d5, d6, d7, d8, d9, d10)
    c5 = bulid_dict_for_one_class(l5, d1, d2, d3, d4, d5, d6, d7, d8, d9, d10)
    c6 = bulid_dict_for_one_class(l6, d1, d2, d3, d4, d5, d6, d7, d8, d9, d10)
    c7 = bulid_dict_for_one_class(l7, d1, d2, d3, d4, d5, d6, d7, d8, d9, d10)
    c8 = bulid_dict_for_one_class(l8, d1, d2, d3, d4, d5, d6, d7, d8, d9, d10)
    c9 = bulid_dict_for_one_class(l9, d1, d2, d3, d4, d5, d6, d7, d8, d9, d10)
    c10 = bulid_dict_for_one_class(
        l10, d1, d2, d3, d4, d5, d6, d7, d8, d9, d10)

    all_class_dict[string_of_class[0]] = c1
    all_class_dict[string_of_class[1]] = c2
    all_class_dict[string_of_class[2]] = c3
    all_class_dict[string_of_class[3]] = c4
    all_class_dict[string_of_class[4]] = c5
    all_class_dict[string_of_class[5]] = c6
    all_class_dict[string_of_class[6]] = c7
    all_class_dict[string_of_class[7]] = c8
    all_class_dict[string_of_class[8]] = c9
    all_class_dict[string_of_class[9]] = c10

    # print(all_class_dict.keys())

    # l = d1.keys()
    # print(d1['新辉腾'])
    # print(type(l))
    # print(type(l[0]))
    # print("新辉腾" in d1.keys())
    # print(d1)
    # print(c1)

    # print(all_class_dict)

    # print(len(all_dict))
    # print(len(all_list))
    # print(len(all_dict))
    # print(num)

    B = calculate_B(all_class_dict)
    # print(B)
    # print(B.keys())

    word_features = feature_select_use_new_CHI(
        all_class_dict, B, count, N, word_set)
    # print(word_features["car"])
    # print(word_features["military"])
    # print(len(word_features["military"]))

    out = count_tf_idf(word_features, count)

    # print(out.keys())
    return out


def test(model):

    accuracy = [0]*10
    f_test = [0]*10

    string_of_class = ['car',
                       'finance',
                       'science',
                       'health',
                       'sports',
                       'education',
                       'culture',
                       'military',
                       'joy',
                       'fashion']

    # Load data
    # test_label = load_test_label()

    for i in range(10):
        f_test[i] = load_test_file(string_of_class[i])

    for u in range(10):
        # Load data
        # np.loadtxt(f_test[u], str)
        word_list_test = []

        f = open(f_test[u], "r")
        for line in f.readlines():
            l = list(jieba.cut(line, cut_all=False))
            word_list_test.append(l)

        # word_list_test = np.loadtxt(f_test[u], str)
        # word_list_test = word_list_test.tolist()
        # print(word_list_test)

        # print(len(word_list_test))

        # Test begin
        acc_temp = 0
        for y in range(len(word_list_test)):
            score_list = {}
            score_list = score_list.fromkeys(string_of_class, 1)

            for t in range(10):

                for word in word_list_test[y]:
                    t_w = string_of_class[t]

                    # print(word)
                    if word in model[string_of_class[t]]:
                        # python nb support big number calculate
                        score_list[t_w] *= model[t_w][word]
                    else:
                        score_list[t_w] = score_list[t_w] * 1

                """ Function Programming """
                s_list = sorted(score_list.items(
                ), key=lambda item: item[1], reverse=True)
                # print(s_list)

                # if s_list[0][0] == string_of_class[u]:
                #     acc_temp = acc_temp + 1
                # else:
                #     pass

            if s_list[0][0] == string_of_class[u]:
                acc_temp = acc_temp + 1
            else:
                pass

        # print(acc_temp)
        accuracy[u] = acc_temp / 100
        print("%s has been classified, and the accuracy is %.2f" %
              (string_of_class[u], accuracy[u]))

        # for word in word_list:
        #     cnt = cnt + 1
        #     if word in word_set_dic[name_class]:
        #         word_set_dic[name_class][word] += 1
        #     else:
        #         word_set_dic[name_class][word] = 1

    # f_test_car = load_test_file('car')
    # f_test_finance = load_test_file('finance')
    # f_test_science = load_test_file('science')
    # f_test_health = load_test_file('health')
    # f_test_sports = load_test_file('sports')
    # f_test_education = load_test_file('education')
    # f_test_culture = load_test_file('culture')
    # f_test_military = load_test_file('military')
    # f_test_joy = load_test_file('joy')
    # f_test_fashion = load_test_file('fashion')

    accuracy_ave = 0
    for i in range(len(accuracy)):
        accuracy_ave += accuracy[i]
    accuracy_ave = accuracy_ave / 10

    return accuracy_ave


if __name__ == "__main__":

    t_1 = time.clock()

    # Load files

    # arr_sw = init_stopwords()
    # # print(arr_sw)
    # test = "12我是一个有很强自我【约束能力】的帅哥"
    # arr_w = devide_words(test, arr_sw)
    # print(arr_w)
    loadtoFiles()
    t_2 = time.clock()
    t_cost = t_2 - t_1
    t_cost = int(t_cost)
    print("Loading files cost %d second" % t_cost)

    # Initialization
    dic = {}
    string_of_class = ['car',
                       'finance',
                       'science',
                       'health',
                       'sports',
                       'education',
                       'culture',
                       'military',
                       'joy',
                       'fashion']

    # init()
    # word_set_dic.fromkeys(string_of_class)
    word_set_dic = dic.fromkeys(string_of_class)

    model = naiveBayes()
    # print(word_set_dic)
    # print(word_set_dic["car"])
    # print(word_set_dic["joy"])

    print("\n")
    acc = test(model)
    print("Accyracy is  %.2f" % acc)

    t_last = time.clock()
    t_all = t_last - t_1
    t_all = int(t_all)
    print("All time cost is %d s" % t_all)
