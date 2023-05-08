class Test():
    def function(self):
        foo = 0
        choo = 1
        return foo, choo
    def function2(self):
        foo1 = self.function()[0]
        choo1 = self.functoin()[1]

        return foo1, choo1
test = Test()
print(test.function())


