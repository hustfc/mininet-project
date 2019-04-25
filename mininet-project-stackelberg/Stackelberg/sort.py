# -*- coding:utf-8 -*-
import operator 

BSLog={
    'h1':{
        'F_BS' : 3,
        'IP' : 'h1',
        # 'POWER' : 'UEPOWER',
        # 'PRICE' : 'UEPRICE',
        # 'LOSS' : 'UELOSS',
        # 'MAX' : 'UEMAX',
        # 'P_k' : 1,
        # 'b_k' : 2,
        
        'F_UE' : 4
    },
    'h2':{
        'F_BS' : 7,
        'IP' : 'h2',
        # 'POWER' : 'UEPOWER',
        # 'PRICE' : 'UEPRICE',
        # 'LOSS' : 'UELOSS',
        # 'MAX' : 'UEMAX',
        # 'P_k' : 1,
        # 'b_k' : 2,
        
        'F_UE' : 6
    },
    'h3':{
        'F_BS' : 5,
        'IP' : 'h3',
        # 'POWER' : 'UEPOWER',
        # 'PRICE' : 'UEPRICE',
        # 'LOSS' : 'UELOSS',
        # 'MAX' : 'UEMAX',
        # 'P_k' : 1,
        # 'b_k' : 2,
        
        'F_UE' : 8
    }
    # {
    #     'F_BS' : 11,
    #     'IP' : 'h4',
    #     # 'POWER' : 'UEPOWER',
    #     # 'PRICE' : 'UEPRICE',
    #     # 'LOSS' : 'UELOSS',
    #     # 'MAX' : 'UEMAX',
    #     # 'P_k' : 1,
    #     # 'b_k' : 2,
        
    #     'F_UE' : 12
    # },
    # {
    #     'F_BS' : 9,
    #     'IP' : 'h5',
    #     # 'POWER' : 'UEPOWER',
    #     # 'PRICE' : 'UEPRICE',
    #     # 'LOSS' : 'UELOSS',
    #     # 'MAX' : 'UEMAX',
    #     # 'P_k' : 1,
    #     # 'b_k' : 2,
        
    #     'F_UE' : 10
    # }
}
EQ = []
EQ.append(BSLog['h1'])
EQ.append(BSLog['h2'])
EQ.append(BSLog['h3'])
# print(after)
after = sorted(EQ,key = lambda x:x['F_BS'],reverse = True)

print(after)
# print(BSLog)
# sorted(BSLog,key=lambda x : x['F_BS'])
# after = sorted(BSLog,key=lambda x : x['F_BS'], reverse=True)
# print(after)