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

The way this works is you define Sources for data, Rules that use those Sources and make Comparisons between them, 
Engines that make use of rules, and then you call `Engine.decide()` and pass it some real/raw data that will be 
processed and fed to rules by the Sources.


### Sources

Sources may be a little tricky to understand at first. When you define a Source, you don't necessarily define the 
data or where it is fetched. Sources are more like placeholders that yield the necessary data when Rules are checked.

You can have Sources that always yield the same value, like the `FixedValueSource`, or Sources that will do some 
sort of processing to the data you feed the engine, like the `DictSource` which fetches the value of a given key in 
the dictionary. If you want you can also implement your own Sources that fetch or generate data in any way you like, 
like getting something from an API using HTTP, or generating a value depending on the time of the day.

#### Currently available Sources

* DictSource - yields the value of a given key in a dictionary.
* FixedValueSource - always yields the same value, which you set up when instantiating it.
* PercentageSource - yields a percentage of the value returned by another Source.
* RandomIntSource - yields a random integer between the values you specify when instantiating it.


### Comparisons

These are pretty simple: they take two Sources and compare them in some way, like "is A equal to B", or "is X greater
than or equal to Y". The values to be compared are passed to the Comparison automatically when `Rule.check()` is called.

#### Currently available Comparisons

The names should be self-explanatory.

* Equal
* NotEqual
* GreaterThan
* GreaterThanOrEqual
* LessThan
* LessThanOrEqual

### Rules

This is where you combine Sources and Comparisons to create actual decision logic. When you instantiate a Rule, you 
tell it which Sources you want to compare, as well as the Comparison you want it to use. Rules have a `check()` 
method which runs the rule logic. You can call it manually but it is normally called automatically by the Engine. You
can also implement custom Rules with custom logic in this method.

One important note: the Rules pass the Sources to the Comparisons in the same order you pass them to the Rule. For 
example, if you instantiate this rule: `rule = SimpleRule(source1, source2, GreaterThanOrEqual())`, the comparison 
made will be equivalent to `source1 >= source2`, whereas if you do `rule = SimpleRule(source2, source1, 
GreaterThanOrEqual())` it will result in `source2 >= source1`.

#### Currently available rules

* SimpleRule - Uses the provided Comparison to compare the two given Sources.
* BooleanOrRule - Takes two other Rules and returns True if **at least one of them** returns True.
* BooleanAndRule - Takes two other Rules and returns True if **both of them** return True.

When `rule.check()` is called, this rule will make sure that the value we get from source1 (the one that comes from 
`data['age']`) is greater than or equal to the value we get from source2 (the one that comes from 
`data['minimum_age']`).


### Engine

The Engine is currently the simples part of the system. When you instantiate it, you pass it all the rules you want 
it to use and when you call `Engine.decide()` it runs the `check()` method on all the rules. If all return True, the 
engine returns True.


## Example

Let's start with a very simple example and say you want to ensure someone is at least 18 years old. This could be 
expressed like so:

```
# First we define the data Sources
age = DictSource('age')
minimum_age = FixedValueSource(18)

# Then we create our rule and the engine the will use it
rule = SimpleRule(source1, source2, GreaterThanOrEqual()) # Equivalent to age >= minimum_age

engine = Engine([rule])

# Now let's come up with some real data
bob = {
    'name': 'Bob',
    'age': 17,
}

alice = {
    'name': 'Alice',
    'age': 32,
}

peter = {
    'name': 'Peter Parker',
    'age': 18,
}

# Finally, let's make decisions about our three personas
engine.decide(bob)  # This returns False
engine.decide(alice)  # This returns True
engine.decide(peter)  # This returns True
```

As you can see, the DictSource knows how to fetch the age from the data dictionaries. You can check this tiny bit by 
running `age.get_value(bob)` and it should return `17`. 

When passing the data dictionaries to the Engine along with the Rules we created, the Engine will pass the data to each 
Rule,  which in turn will pass it to each Source that requires it - in this case, the DictSource - which will then 
fetch the value from the key you instantiated it with.

To put it another way, a DictSource only knows you want it to fetch data from a dictionary that will show up sometime
in the future, and it knows which key in the dictionary you want it to fetch the data from.

FixedValueSource is an exception, as it is initialized with a specific value right from the start but just like any 
other Source, this value is only used when a Rule asks for its value.

---

I suggest you read the tests to better understand how this works. Start with test_sources.py, which is pretty 
simple and should make things a lot more obvious. Then, look at test_comparisons.py, proceed to test_rules.py, and 
finally look at test_engine.py to see how everything can be put together. 

Pull requests for improvements are welcome! ;)
