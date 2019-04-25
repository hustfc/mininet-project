import re

filename1 = '/media/psf/Home/Documents/GitHub/mininet-project-stackelberg/Stackelberg/Log/6.txt'
with open(filename1, 'r') as f1:
        buffer = f1.readlines()
        lenth = len(buffer)
        # filename2 = '/home/shlled/mininet-wifi/Log/new%s' % filename
        filename2 = '/media/psf/Home/Documents/GitHub/mininet-project-stackelberg/Stackelberg/Log/newmsg.txt'
        f2 = open(filename2, 'a+')
        current_index = 0
        total = 19
        while current_index < total:
            i = 0
            while i <total:    
                temp = buffer[i]
                span1 = re.search('filename:', temp).span()
                s1 = span1[0]
                e1 = span1[1]
                span3 = re.search('total:', temp).span()
                s3 = span3[0]
                e3 = span3[1]
                span4 = re.search('index:', temp).span()
                s4 = span4[0]
                e4 = span4[1]
                span5 = re.search('data:', temp).span()
                s5 = span5[0]
                e5 = span5[1]
                T_index = int(temp[e4:s5])
                if T_index == current_index:
                    print("T_index:",T_index)
                    f2.write(temp[e5:])
                    current_index += 1
                    break;
                i +=1
        f2.close()