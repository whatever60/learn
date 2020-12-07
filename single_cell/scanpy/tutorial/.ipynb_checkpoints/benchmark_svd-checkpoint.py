from timeit import timeit


print(
    timeit(stmt='ss.svdlibc()', setup='import sparse_svd as ss', number=5)
)
