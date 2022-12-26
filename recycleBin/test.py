class Man:
    id = 0 # 类变量
    def __init__(self, name):
        self.name = name
        self.id = self.id_number()
 
    @classmethod
    def id_number(cls):
        cls.id += 1
        return cls.id
 
a = Man('A')
print(a.id)
b = Man('B')
print(b.id)