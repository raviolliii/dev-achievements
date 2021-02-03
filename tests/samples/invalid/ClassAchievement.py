# cases where ClassAchievement should not unlock

# >> CASE
class Foo:
    pass

# >> CASE
class Foo:
    pass

Foo

# >> CASE
class Foo:
    pass

f = Foo
f()

# >> CASE
Foo()

# >> CASE
Foo
