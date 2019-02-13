import json
import jieba
import gensim
import time


def process_json_file(file_name):
    with open(file_name, 'r', encoding = 'utf-8')as json_file:
        data_list = json.load(json_file)
        symptom_dict =  {}
        for i in range(len(data_list)):
            for word in data_list[i]["症状"]["典型症状"]:
                if word not in symptom_dict.keys():
                    symptom_dict.update( {word:0})
                else:
                    symptom_dict[word] = symptom_dict[word] + 1

        print("Length of symtom_dict is %d ." % len(symptom_dict))
        symptom_dict_new =  {}
        for key in symptom_dict.keys():
            if symptom_dict[key] >= 12:
                symptom_dict_new.update( {key:symptom_dict[key]})

        print("Length of symtom_dict_new is %d ." % len(symptom_dict_new))
        print(symptom_dict_new["发热伴咳嗽、咯痰、胸痛"])
        sorted_list = sorted(symptom_dict_new.items(), 
                             key = lambda e:e[1], reverse = True)
        for j in range(10):
            a = 0
            # print(sorted_list[j][0])
            # print(sorted_list[j][1])

        # print(sorted_list[600][0])
        # print(sorted_list[600][1])
        return symptom_dict_new


def process_json_section_office(file_name):
    with open(file_name, 'r', encoding = 'utf-8')as json_section_office:
        data_list = json.load(json_section_office)
        print(len(data_list))
        # print(data_list[12]["挂号科室"])

        section_office =  {}
        for i in range(len(data_list)):
            for ele in data_list[i]["挂号科室"]:
                # print(data_list[i]["挂号科室"])
                # print("test")
                if ele not in section_office:
                    section_office.update( {ele:0})
                else:
                    section_office[ele] = section_office[ele] + 1

        # print(len(section_office))
        for key in section_office.keys():
            a = 0
            # print("%s , %d" % (key, section_office[key]))

        return data_list


def find_ele(dataset, name):
    for i in range(len(dataset)):
        if dataset[i]["病名"] == name:
            return i


def create_dataset(file_name, data_symptom, data_section_office):
    time_start = time.clock()

    # key -  > list; value -  > str
    data_set = []
    with open(file_name, 'r', encoding = 'utf-8')as json_data:
        dict_list = json.load(json_data)

        cnt = 0

        # disease name list
        disease_name = []
        for i in range(len(data_section_office)):
            disease_name.append(data_section_office[i]["病名"])

        for i in range(len(dict_list)):
            name = dict_list[i]["病名"]
            if name in disease_name:
                # process feature
                list_symptom = []
                symptom_list = dict_list[i]["症状"]["典型症状"]
                for symptom in data_symptom.keys():
                    if symptom in symptom_list:
                        list_symptom.append((symptom, 1))
                    else:
                        list_symptom.append((symptom, 0))

                index = find_ele(data_section_office, name)
                for j in range(len(data_section_office[index]["挂号科室"])):
                    # print(len(data_section_office[index]["挂号科室"]))
                    # print(type(data_section_office[index]["挂号科室"]))
                    # print(index)
                    data_set.append( {data_section_office[index]["挂号科室"][j]:list_symptom})
            else:
                cnt = cnt + 1

        '''分诊室与医疗数据不匹配的数量'''
        print("'jbks <-> jb_medical_data' don't have %d time(s)." % cnt)

    time_end = time.clock()
    print("Creating dataset use %.2f s." % (time_end - time_start))
    return data_set


print(type(process_json_file("9939jb_medical_data.json")))
process_json_section_office("9939jbks.json")
# print(process_json_file("9939jb_medical_data.json"))


file_name = "9939jb_medical_data.json"
data_symptom = process_json_file(file_name)
data_section_office = process_json_section_office("9939jbks.json")
data_set = create_dataset(file_name, data_symptom, data_section_office)
# print(data_set[12])
print(len(data_set))
