from multiprocessing import Pool

def work(x):
    print(x+1)
    return x+1

if __name__ == "__main__":
    pool = Pool(processes=3) # 4个线程
    x = [1,2,3,4,5,6]
    results = pool.map(work, x)
    print (results)