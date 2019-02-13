import gensim
import time
import random
import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import NullFormatter

time_start = time.clock()
model = gensim.models.Word2Vec.load('mymodel')
time_end = time.clock()
print("Loading model cost %.2f s" % (time_end - time_start))
print(model.most_similar(['发热']))
print(type(model))
# print(model.wv.vocab)
print(type(model.wv.vocab))
print(len(model.wv.vocab))
# print(model["癌症"])
# print(model["发热"])
# print(model["放射性肺炎"])
# print(model["放射性"])
# print(model["肺炎"])

vacob_np = []
# cnt = 0
for word in model.wv.vocab.keys():
    # cnt = cnt + 1
    # if cnt % 10000 == 0:
    #     print(cnt)
    vacob_np.append(model[word])

vacob_np = np.array(vacob_np)
vacob_np_new = []
for i in range(1000):
    cnt = random.randint(0, len(model.wv.vocab))
    vacob_np_new.append(vacob_np[cnt])
# print(vacob_np)

time_start = time.clock()
tsne = TSNE(n_components = 3)
# print("Done")
tsne.fit_transform(vacob_np_new)
time_end = time.clock()
print("Time used: %.2f s." % (time_end - time_start))
# print(tsne.embedding_)
# print(type(tsne.embedding_))
v_visualize = tsne.embedding_

fig = plt.figure(figsize = (16, 8))
ax = fig.add_subplot(111, projection = '3d')
ax.scatter(v_visualize[:, 0], v_visualize[:, 1], 
           v_visualize[:, 2], c = "blue")
ax.view_init(6, -36)
plt.show()
