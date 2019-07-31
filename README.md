A simple rules-based decision engine.

[![Build Status](https://travis-ci.org/borfast/decision-engine.svg?branch=master)](https://travis-ci.org/borfast/decision-engine)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/0859ce60678b42d0a230c0819e5a6b5c)](https://www.codacy.com/app/borfast/decision-engine?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=borfast/decision-engine&amp;utm_campaign=Badge_Grade)
[![codecov](https://codecov.io/gh/borfast/decision-engine/branch/master/graph/badge.svg)](https://codecov.io/gh/borfast/decision-engine)


## Concepts

There are three base concepts: Sources, Comparisons and Rules:

* Sources are sources of data to be tested.
* Comparisons are algorithms to compare sources of data.
* Rules are where you combine Sources and Comparisons to create logic decisions.

There's also the Engine but it's pretty simple, as all it does is validate all the rules you feed into it. Its 
main logic is literally one line of code: `return all([rule.check(data) for rule in self.rules])` 

### Sources

Sources may be a little tricky to understand at first. When you define a Source, you don't necessarily define the 
data or where it is fetched; you are only telling the engine that there will be a source of data that behaves in a 
certain way but at the Source creation time, it doesn't matter what data there will be.

For example, when using a DictSource, you are creating a Source that expects a dictionary will be passed into it at 
some point in the future, and it will know (because you told it so when you instantiated it) which key in the 
dictionary contains the value you want it to use.

So for example, you could create two DictSources and give them different keys to fetch the value from, say 'age' and 
'minimum_age', like so:
```
source1 = DictSource('age')
source2 = DictSource('minimum_age')
```


Then you could create a rule that compares both DictSources and use a dict such as the following:

```
data = {
    'age': 17,
    'minimum_age': 18
}
```

When passing this data dictionary to an Engine along with your Rules, the Engine will pass the data to each Rule, 
which in turn will pass it to each Source - in this case, the two DictSources - which will each fetch the value from 
the key you instantiated them with.

To put it another way, a DictSource only knows you want it to fetch data from a dictionary that will show up sometime
in the future, and it knows which key in the dictionary you want it to fetch the data from.

FixedValueSource is an exception, as it is initialized with a specific value right from the start but just like any 
other Source, this value is only used when a Rule asks for its value.

A PercentageSource allows you to get a percentage of the value returned by another Source.

A RandomIntSource will return a random integer between the specified values.


### Comparisons

These are pretty simple: they take two Sources and compare them in some way, like "is A equal to B", or "is X greater
than or equal to Y". 


### Rules

This is where you combine Sources and Comparisons to create actual decision logic. When you instantiate a Rule, you 
tell it which Sources you want to compare, as well as the Comparison you want it to use. Continuing the example from 
above, you could create a Rule such as this:
```
rule = SimpleRule(source1, source2, GreaterThanOrEqual())
```

When `rule.check()` is called, this rule will make sure that the value we get from source1 (the one that comes from 
`data['age']`) is greater than or equal to the value we get from source2 (the one that comes from 
`data['minimum_age']`).



---

I suggest you read the tests to better understand how this works. Start with test_sources.py, which is pretty 
simple and should make things a lot more obvious. Then, look at test_comparisons.py, proceed to test_rules.py, and 
finally look at test_engine.py to see how everything can be put together. 

Pull requests for improvements are welcome! ;)
