import gensim
model = gensim.models.KeyedVectors.load_word2vec_format(
    'GoogleNews-vectors-negative300.bin', binary=True)

print(model.get_vector("apple"))
print(model.most_similar(["apple"]))