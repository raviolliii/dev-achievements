# cases where LambdaAchievement should unlock

# >> CASE
lambda x: x

# >> CASE
f = lambda x: x

# >> CASE
[lambda x: x for x in range(4)]

# >> CASE
def test(f):
    return f()

test(lambda _: None)
