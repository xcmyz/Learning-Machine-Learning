import json
import jieba
import gensim
import time


def load_json_file(file_name):
    json_file = open(file_name, 'r', encoding='utf-8')
    data_list = json.load(json_file)

    json_file.close()
    return data_list


def remove_duplicates(data_list):
    out_list = []

    for word in data_list:
        if word not in out_list:
            out_list.append(word)

    # print(len(out_list))
    return out_list


def load_userdict(file_name):
    file_of_dict = open(file_name, "r", encoding='utf-8')
    data = file_of_dict.readlines()
    data_new = []
    for line in data:
        line = line.strip('\n')
        data_new.append(line)

    # print(len(data_new))
    data_out = remove_duplicates(data_new)
    file_of_dict.close()
    return data_out


def load_stop_words(file_name):
    file_of_stopwords = open(file_name, "r", encoding='utf-8')
    data = file_of_stopwords.readlines()
    data_new = []
    for line in data:
        line = line.strip('\n')
        data_new.append(line)

    # print(len(data_new))
    data_out = remove_duplicates(data_new)
    file_of_stopwords.close()
    # print(len(data_out))
    file_sw = open('stop_words.txt', 'w', encoding='utf-8')
    for ele in data_out:
        file_sw.write(ele)
        file_sw.write('\n')
    file_sw.close()

    file_of_stopwords_new = open('stop_words.txt', "r", encoding='utf-8')
    data_sw_new = file_of_stopwords_new.readlines()
    data_sw_out = []
    for line in data_sw_new:
        line = line.strip('\n')
        data_sw_out.append(line)

    # print(type(data_sw_out))
    # print(len(data_sw_out))
    # print(data_sw_out[0])
    return data_sw_out


def compose_dict(data_out_1, data_out_2):
    data_in_one = []
    data_in_one = data_out_1 + data_out_2

    data_in_one_new = remove_duplicates(data_in_one)

    # print(len(data_in_one_new))
    file_dict = open('dictionary.txt', 'w', encoding='utf-8')
    for ele in data_in_one_new:
        file_dict.write(ele)
        file_dict.write('\n')
    file_dict.close()


def add_userdict(file_name_of_userdict):
    jieba.load_userdict(file_name_of_userdict)


def cut_words(str_words, stopwords):
    words = list(jieba.cut(str_words))
    words_out = []
    for word in words:
        if word not in stopwords:
            words_out.append(word)

    return words_out


def process_data():
    cnt = 0
    time_start = time.clock()

    # Initial jieba
    d1 = load_userdict("disease.txt")
    d2 = load_userdict("diseases_symptoms.txt")
    compose_dict(d1, d2)
    add_userdict("dictionary.txt")
    stopwords = load_stop_words("stopword.txt")

    # Load train data
    train_data_1 = load_json_file("9939jb_medical_data.json")
    train_data_2 = load_json_file("9939zz_medical_data.json")
    train_data = []
    for i in range(len(train_data_1)):
        cnt = cnt + 1
        compose_temp = str(train_data_1[i])
        compose_temp = cut_words(compose_temp, stopwords)
        compose_new_temp = []
        for word in compose_temp:
            if word not in train_data_1[i].keys():
                compose_new_temp.append(word)

        # print(type(compose_new_temp))
        train_data.append(compose_new_temp)

        if cnt % 500 == 0:
            time_temp = time.clock()
            print("Training data has %d entries" % cnt)
            print("Time cost is %.2f s" % (time_temp - time_start))

    for i in range(len(train_data_2)):
        cnt = cnt + 1
        compose_temp = str(train_data_2[i])
        compose_temp = cut_words(compose_temp, stopwords)
        compose_new_temp = []
        for word in compose_temp:
            if word not in train_data_2[i].keys():
                compose_new_temp.append(word)

        # print(type(compose_new_temp))
        train_data.append(compose_new_temp)

        if cnt % 500 == 0:
            time_temp = time.clock()
            print("Training data has %d entries" % cnt)
            print("Time cost is %.2f s" % (time_temp - time_start))

    print("Training data has %d entries" % len(train_data))
    return train_data


def train(train_data):
    model = gensim.models.Word2Vec(train_data, min_count=10, size=60)
    model.save('mymodel')


def main():
    train_data = process_data()
    train(train_data)


if __name__ == "__main__":
    main()
