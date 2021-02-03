# cases where FunctionAchievement should not unlock

# >> CASE
def test():
    pass

# >> CASE
def func():
    pass

func

# >> CASE
def func():
    pass

f = func
f()

# >> CASE
func()

# >> CASE
func
