import numpy as np
import matplotlib.pyplot as plt
import os
class Analize:
    spendes=[[]]
    maxxx=0
    max_name=""
    min=-1
    min_name=""
    avg=0
    path=""
    all_spendes=0
    def __init__(self,a):
        self.spendes=a
        self.all_spendes=len(a)
    def analize(self,user_id):
        prices=[]
        names=[]
        for a in self.spendes:
            if not(a[2] in  names):
                names.append(a[2])
                prices.append(a[3])
            else:
                prices[names.index(a[2])]=prices[names.index(a[2])]+a[3]
            if self.maxxx<=a[3]:
                self.maxxx=a[3]
                self.max_name=a[2]
            if self.min>=a[3] or (self.min==-1):
                self.min=a[3]
                self.min_name=a[2]
        self.avg=np.mean(prices)

        plt.bar(names, prices)
        plt.xlabel('Категории трат')
        plt.ylabel('Сумма')
        plt.title('Распределение трат')
        plt.savefig(str(user_id)+'.jpg')
        plt.savefig(str(user_id)+'.jpg', dpi=300)
        self.path=str(user_id)+'.jpg'
    def delPhoto(self):
            os.remove(self.path)