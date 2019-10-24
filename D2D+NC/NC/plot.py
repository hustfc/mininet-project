import matplotlib.pyplot as plt

plt.xlabel('loss rate between BS and RU',fontsize = 16)
#plt.xlim(0,20)
plt.ylim(85, 100)
plt.ylabel('RU Throughput (kbps)',fontsize = 16)
error = ["10%", "15%", "20%", "25%", "30%", "35%", "40%"]
store = [970.016, 960.704, 948.192, 937.92, 926.944, 917.856, 909.376]
NC = [993.613, 983.395, 980.437, 973.176, 963.21, 957.685, 955.845]
for i in range(len(store)):
    store[i] = store[i] / 1024 * 100
    NC[i] = NC[i] / 1024 * 100
# plt.plot(cicle,result_fair,marker = '*',color = 'red',label='MOO')
plt.plot(error,store,marker = '^',color = 'slategray',label='Store and Forward')
plt.plot(error,NC,marker = '*',color = 'slateblue',label='Network Coding')
#plt.title('Register User Throughput')
# labelx = range(0,21)
# plt.xticks(cicle,labelx)

plt.tick_params(labelsize=16)
plt.legend(prop={'size':14})
plt.grid()

plt.show()