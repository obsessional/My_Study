# -*- coding: utf-8 -*-

class asdf(object):
    def __init__(self,a):
        self.a = a

    def __str__(self):
        return "%s==>%s" %(self.a,self.a)

    __repr__ = __str__

    def log_print(self):
        print(self.a)


if __name__ == '__main__':
    aa = asdf(222)
    aa
    # asdf.log_print()