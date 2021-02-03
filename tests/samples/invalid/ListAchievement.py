# cases where ListAchievement should not unlock

# >> CASE
[i for i in range(10)]

# >> CASE
[i for i in range(10) if i % 2 == 0]

# >> CASE
x = 4, 5, 6

# >> CASE
x = (4, 5, 6)

# >> CASE
x = (i for i in range(10))
