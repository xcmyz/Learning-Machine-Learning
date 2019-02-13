import gensim
import time

time_start = time.clock()
model = gensim.models.Word2Vec.load('mymodel')
time_end = time.clock()
print("Loading model cost %.2f s" % (time_end - time_start))

temp_list = ['发热']
tumple_list_word2vec = model.most_similar(temp_list)
print(temp_list)
for i in range(len(tumple_list_word2vec)):
    print(tumple_list_word2vec[i])

temp_list = ['肥胖症']
tumple_list_word2vec = model.most_similar(temp_list)
print(temp_list)
for i in range(len(tumple_list_word2vec)):
    print(tumple_list_word2vec[i])

temp_list = ['白血病']
tumple_list_word2vec = model.most_similar(temp_list)
print(temp_list)
for i in range(len(tumple_list_word2vec)):
    print(tumple_list_word2vec[i])