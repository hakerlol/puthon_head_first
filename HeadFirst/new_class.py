class CountFromBy:
    def __init__(self, v: int = 0, i: int = 1) -> None:
        self.val = v
        self.incr = i

    def __repr__(self) -> str:
        return 'val: ' + str(self.val)

    def increase(self) -> None:
        self.val += self.incr


a = CountFromBy(100, 10)
print(a)
a.increase()
print(a)

i = CountFromBy()
print(i)
i.increase()
print(i)
