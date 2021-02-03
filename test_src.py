import dev_achievements


# HelloWorldAchievement
print('Helo world', end='')
print('\nHello World!')


# AssignAchievement
x = 4


# MathOperatorsAchievement
x += 1


# BitwiseOperatorsAchievement
x << 2
x ^ 2


# ConditionalAchievement
if x < 4:
    x = 4
else:
    x = 5


# LoopsAchievement
for i in range(2):
    x + i

x = 0
while x < 5:
    x += 1


# ComprehensionAchievement
x = [i for i in range(10)]


# PassAchievement
for _ in range(2):
    pass


# FunctionAchievement
def some_func():
    pass

def some_other_func():
    pass

some_func()


# LambdaAchievement
lf = lambda x: x + 1


# ListAchievement
x = [4, 5, 6]


# DictAchievement
x = {'name': 'John Doe'}


# ClassAchievement
class Test:
    pass

class OtherTest:
    pass

t = Test()

