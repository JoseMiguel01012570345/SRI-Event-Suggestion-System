from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import StandardScaler
import numpy as np

# Ejemplo de corpus
corpus = [
    'este es el primer documento',
    'este documento es el segundo documento',
    'y este es el tercero',
    'es este el primer documento',
]

# Convertir el corpus en una matriz de características TF-IDF
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(corpus)

matrix = tfidf_matrix.toarray()

# Realizar LSA en la matriz TF-IDF
scaler = StandardScaler()
x_test = scaler.fit_transform(matrix)

lsa = TruncatedSVD(n_components=4,algorithm='randomized')
lsa_matrix = lsa.fit_transform(matrix)

variance = lsa.explained_variance_ratio_

cumulative = np.cumsum(variance)
d = np.argmax(cumulative >= 0.95) + 1

lsa = TruncatedSVD(n_components=d)
lsa_matrix = lsa.fit_transform(matrix)
t = lsa_matrix.transpose()

rank = np.matmul(lsa_matrix,t)

# Imprimir la matriz LSA
print(lsa_matrix)
print('\n\n\n\n')
print(rank)
