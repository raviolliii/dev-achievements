# cases where ConditionalAchievement should unlock

# >> CASE
if True:
    pass

# >> CASE
if False:
    pass
else:
    pass

# >> CASE
if False:
    pass
elif True:
    pass
else:
    pass

# >> CASE
4 if True else 5
