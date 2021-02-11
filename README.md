# dev-achievements
Earn Achievements while learning how to code


Game-ify your experience while learning to code and get achievements for different concepts as you use them. Start off at a simple `print` statement and work your way up to `functions` and `classes` (and more to come).


<br/>


### Example

Just `import` the package at the top of your script (example):

```python
# my_script.py

import dev_achievements


def cumulative_sum(x):
    # calculates sum of numbers from 0 to x
    total = 0
    for i in range(x):
        total += i
    return total


result = cumulative_sum(4)
print('value: ', result)
```

And run it in terminal as you normally would:
```shell
$ python3 my_script.py

┌──────────────────────────────────┐
│ Achievement Unlocked: Loops!     │
│ Achievement Unlocked: Functions! │
└──────────────────────────────────┘

value:  6
```


<br/>


### Usage

To install and use:
1. Install the package with `pip install dev-achievements`
1. Use `import dev_achievements` at the top of your script
1. Run your `python` script as normal

To uninstall:
1. Uninstall the package with `pip uninstall dev-achievements`
1. Optionally, delete the directory `~/.dev_achievements` to remove any achievement progress. Keep this directory to save progress through installs.


<br/>


### Some things to note

1. Currently this _only_ works on single file scripts - if you import your own module (e.g. for utility functions) that module will _not_ be parsed (planning on fixing this though)
1. Some achievements have _dependencies_, and will only be unlocked once previous ones have been unlocked
1. Unlocked achievements will remain unlocked, so those "Achievement Unlocked" messages will should only show once per achievement


<br/>


### Future plans and contributing
1. The bare bones achievements are currently implemented (using `"hello world"`, `for` loops, `lists`, `functions`, etc.) - more achievements are in development (see issue [#1](https://github.com/raviolliii/dev-achievements/issues/1))
1. More details on how to contribute (along with code docs to help with the development process) are coming soon
