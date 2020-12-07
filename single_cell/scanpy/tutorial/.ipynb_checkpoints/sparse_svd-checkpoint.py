import numpy as np
import numpy.linalg as nl
import scipy.linalg as sl
import scipy.sparse as ss
from scipy.sparse.linalg import svds
from sparsesvd import sparsesvd

def gen_sample_data(thres=0.6, random_seed=0, conversion=np.asarray):
    cell_num = np.arange(600, 1600, 100)
    gene_num = np.arange(1000, 2000, 100)
    rng = np.random.RandomState(random_seed)
    for i, j in zip(cell_num, gene_num):
        M = rng.normal(0, 1, (i, j))
        M[M > thres] = 0
        yield conversion(M)

        
# LAPACK
def lapack():
    data = gen_sample_data()
    for i in data:
        print(1)
        sl.svd(i, full_matrices=False)
        print(2)


# ARPACK
def arpack():
    data = gen_sample_data(conversion=ss.csc_matrix)
    for i in data:
        print(1)
        ss.linalg.svds(i, k=5)
        print(2)


# LOBPCG
def lobpcg():
    data = gen_sample_data(conversion=ss.csc_matrix)
    for i in data:
        u, s, vt = ss.linalg.svds(i, k=5, solver='lobpcg')


# SVDLIBC
def svdlibc():
    data = gen_sample_data(conversion=ss.csc_matrix)
    for i in data:
        u, s, vt = sparsesvd(i, k=5)
