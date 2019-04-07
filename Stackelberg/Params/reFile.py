index=0
    num = 0 #packge number
    "find the size of the data"
    filename2 = "/home/shlled/mininet-wifi/Log/msg.txt"
    f2 = open(filename2,'r')
    buffer2= f2.readlines()
    lenth = len(buffer2)
    f2.close()
    while index<lenth:
        flag = True
        while flag:
            try:
                thread.start_new_thread(command,(h2,"python receive.py 10.0.0.2 h2-eth0 0.15"))
                thread.start_new_thread(command,(h1,"python send.py 10.0.0.1 h1-eth0 10.0.0.2 msg.txt %d" % num))
            except:
                print("send error")
            time.sleep(18) # wait thread finish
            print("send finish")
            filename3 = "/home/shlled/mininet-wifi/Log/final.txt"
            f3 = open(filename3,'r')
            buffer3 = f3.readlines()
            temp = len(buffer3)
            f3.close()
            if temp == index + 10 or temp >= lenth:
                flag = False
        index += 10
        num += 1