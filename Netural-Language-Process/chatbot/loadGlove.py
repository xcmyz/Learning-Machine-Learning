import json
import time
import gensim


def preprocess(filename):

    with open(filename, "rb") as datafile:
        lines = datafile.readlines()
        print("length ", len(lines))
        print("type ", type(lines))

        time_start = time.clock()

        data_dic = {}
        for line in lines:
            # print(line)
            line = str(line)
            # print(type(line))
            line = line.split(' ')
            # print(type(line))
            # print("length ",len(line))
            listVec = []
            for i in range(1, len(line)):
                # print(i)
                listVec.append(line[i])

            data_dic.update({line[0]: listVec})

        with open("./data/Glove.json", "w") as datafile:
            json.dump(data_dic, datafile, ensure_ascii=True)

        time_end = time.clock()
        print("Use time %.3f seconds" % (time_end-time_start))


def getFileLineNums(filename):
    f = open(filename, 'rb')
    count = 0
    for _ in f:
        count += 1
    # print(count)
    return count


def prepend(infile, outfile, line):
    time_start = time.clock()

    with open(infile, 'rb') as fin:
        lines = fin.readlines()
        # print(type(lines))
        with open(outfile, 'w') as fout:
            fout.write(line + "\n")
            # print(type(lines))
            for i in range(len(lines)):
                # print(type(lines[i]))
                lines[i] = str(lines[i])
                line_in = ""
                for j in range(2, (len(lines[i])-3)):
                    line_in = line_in + lines[i][j]
                # print(line_in)
                fout.write(line_in + "\n")

    time_end = time.clock()
    print("Processing file uses time %.3f seconds" % (time_end-time_start))


def load(filename, dimension):
    time_start = time.clock()
    num_lines = getFileLineNums(filename)
    gensim_file = 'glove_model.txt'
    gensim_first_line = "{} {}".format(num_lines, dimension)
    prepend(filename, gensim_file, gensim_first_line)

    model = gensim.models.KeyedVectors.load_word2vec_format(gensim_file)
    time_end = time.clock()
    print("Time used is %.3f seconds" % (time_end-time_start))

    return model


if __name__ == "__main__":

    # filename = "./glove.6B/glove.6B.200d.txt"
    # preprocess(filename)
    # model = load('./glove.6B/glove.6B.200d.txt', 200)
    model = gensim.models.KeyedVectors.load_word2vec_format("glove_model.txt")
    print(model.get_vector("apple"))
    print(model.most_similar(["apple"]))
