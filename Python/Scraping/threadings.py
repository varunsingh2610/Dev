import threading

def prints(num):
    print(num)
t = threading.Thread(target=prints, args=(10, 20))

t.start()


t.join()


exit()
