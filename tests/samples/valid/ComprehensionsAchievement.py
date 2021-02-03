# cases where ComprehensionsAchievement should unlock

# >> CASE
[None for _ in range(10)]

# >> CASE
[None for i in range(10) if i % 2 == 0]

# >> CASE
{i: i for i in range(10)}

# >> CASE
{i: i for i in range(10) if i % 2 == 0}

# >> CASE
{i for i in range(10)}

# >> CASE
{i for i in range(10) if i % 2 == 0}

# >> CASE
(True for _ in range(10))

# >> CASE
(True for i in range(10) if i % 2 == 0)
