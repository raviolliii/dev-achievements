# cases where LoopsAchievement should unlock

# >> CASE
for _ in range(4):
    pass

# >> CASE
while False:
    pass

# >> CASE
for _ in range(4):
    pass
else:
    pass

# >> CASE
while False:
    pass
else:
    pass
