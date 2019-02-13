import matplotlib.pyplot as plt
import numpy as np
import struct
from PIL import Image


def loadImageSet(filename):

    # Read file
    binfile = open(filename, 'rb')
    buffers = binfile.read()

    # Get the first four integer, return a tuplie
    head = struct.unpack_from('>IIII', buffers, 0)

    # Reach the place of data begin
    offset = struct.calcsize('>IIII')
    imgNum = head[1]
    # print(imgNum)
    width = head[2]
    # print(width)
    height = head[3]
    # print(height)

    # data -> 60000*28*28
    bits = imgNum * width * height
    # fmt format：'>47040000B'
    bitsString = '>' + str(bits) + 'B'

    # Get data，return a tuple
    imgs = struct.unpack_from(bitsString, buffers, offset)

    binfile.close()
    # Reshape to array of [60000,784]
    imgs = np.reshape(imgs, [imgNum, width * height])

    return imgs, head


def loadLabelSet(filename):

    # Read file
    binfile = open(filename, 'rb')
    buffers = binfile.read()

    # Get the first two integer of label file
    head = struct.unpack_from('>II', buffers, 0)

    # Reach the place of the label data begin
    labelNum = head[1]
    offset = struct.calcsize('>II')

    # fmt format：'>60000B'
    numString = '>' + str(labelNum) + "B"
    # Get label
    labels = struct.unpack_from(numString, buffers, offset)

    binfile.close()
    # Reshape to an array
    labels = np.reshape(labels, [labelNum])

    return labels, head


if __name__ == "__main__":

    file1 = 'C:/Users/28012/Desktop/Machine Learning/Neural Networks/MLP for MNIST/MNIST/train-images.idx3-ubyte'
    file2 = 'C:/Users/28012/Desktop/Machine Learning/Neural Networks/MLP for MNIST/MNIST/train-labels.idx1-ubyte'

    imgs, data_head = loadImageSet(file1)
    # print('data_head:', data_head)
    # print(type(imgs))
    # print('imgs_array:', imgs)

    labels, labels_head = loadLabelSet(file2)
    # print('labels_head:', labels_head)
    # print(type(labels))
    # print(labels)

    # Print the first ten images to test the accuracy
    for i in range(30):
        img = imgs[i].reshape(28, 28)
        # plt.imshow(img, cmap='gray')
        # plt.show()
        print(labels[i])
        img = np.array(img, dtype='uint8')
        img_save = Image.fromarray(img)
        num = labels[i]
        # num = i
        num = str(num)
        Str = "test_" + num
        filename = "Pic/" + Str + ".bmp"
        img_save.save(filename, "bmp")

    f_train_img = open("Data_train_images.txt", "w")
    num = len(imgs)
    print(num)
    num = int(num)
    for i in range(num):
        num = labels[i]
        f_train_img.write(str(num) + " # ")
        # print(len(imgs))
        temp = imgs[i].reshape(28, 28)
        npArr = np.array(temp)
        # print(npArr)
        value_list = []
        # cnt = 0
        for x in range(28):
            temp_list = []
            for y in range(28):
                value = npArr[x][y]
                value = int(value)
                # print(value)
                temp_list.append(value)
            # print(temp_list)
            temp_list = str(temp_list)
            value_list.append(temp_list)
            # test = 1
            # test = str(test)
            # print(test)
            for m in range(len(temp_list)):
                # print(len(temp_list))
                if temp_list[m] != '[' and temp_list[m] != ']' and temp_list[m] != ' ':
                    if temp_list[m] == ',':
                        f_train_img.write(" ")
                        # cnt = cnt + 1
                    else:
                        f_train_img.write(temp_list[m])

            f_train_img.write(" ")
            # print("\n")

        # print(value_list)
        # flist = npArr.tostring()
        # print(flist)
        # f_train_img.write(value_list)
        # print(cnt)
        print("Done")
        f_train_img.write("\n")

    f_train_img.close()
    print("Done")
