# Python: Mutable vs Immutable Objects — Everything You Need to Know

## Understanding Python's Object Model, Memory Management, and Why It Matters

---

### Cover Image Suggestion

A split diagram showing two Python variables pointing to the same list object
(on the left) and two variables pointing to separate integer objects (on the
right), with the labels "Mutable" and "Immutable."

---

### Table of Contents

1. Introduction
2. Everything Is an Object
3. `id()` and `type()` — Who Am I and Where Do I Live?
4. Mutable Objects — The Shapeshifters
5. Immutable Objects — The Bedrock
6. Lists of Mutable vs Immutable Built-in Types
7. Equality vs Identity — `==` vs `is`
8. Variable Assignment and Aliasing
9. How Python Passes Arguments to Functions
10. CPython Internals: Integer Caching
11. NSMALLPOSINTS and NSMALLNEGINTS
12. Special Cases: Tuples Containing Mutable Objects
13. Frozen Sets
14. Interactive Mode vs Scripts: A Common Source of Confusion
15. Common Mistakes and Interview Questions
16. Best Practices
17. Key Takeaways
18. Conclusion

---

### 1. Introduction

If you have spent any time writing Python, you have probably encountered a
moment where a variable changed in a way you did not expect.

```python
>>> a = [1, 2, 3]
>>> b = a
>>> a.append(4)
>>> b
```

You might expect `b` to still be `[1, 2, 3]`, right? After all, you only
modified `a`. But here is what actually happens:

```python
[1, 2, 3, 4]
```

Welcome to the heart of Python's object model.

Understanding why this happens — and how to predict when it will happen — is
one of the most important skills you can develop as a Python developer. It is
also one of the most common topics in Python technical interviews.

The confusion stems from a fundamental question: when you write `b = a`, does
Python copy the value, or does it create an alias? The answer depends on
whether the object is mutable or immutable. Understanding this distinction
will change how you think about every line of Python code you write.

This article will take you from a practical, intuitive understanding all the
way down to the CPython source code. You will learn:

- What it means for everything to be an object
- How `id()` and `type()` reveal an object's identity and type
- The difference between mutable and immutable objects
- How Python stores objects in memory
- Why `==` is different from `is`
- How function arguments actually work
- Why CPython caches small integers
- Common pitfalls and how to avoid them
- Interview questions you might face

By the end, you will never be surprised by how Python handles your variables
again.

---

### 2. Everything Is an Object

In Python, **everything is an object**. Integers, strings, lists, functions,
classes — even the module itself — are all objects.

An object is a chunk of memory that has:

- An **identity** (a unique identifier, its memory address in CPython)
- A **type** (which defines what you can do with it)
- A **value** (the actual data it holds)

```python
>>> x = 42
>>> id(x)
140735200843776
>>> type(x)
<class 'int'>
>>> x.bit_length()
6
```

This is fundamentally different from languages like C, where an integer is
just a raw sequence of bytes in memory. In Python, even the humble integer
`42` is a full-fledged object with methods and metadata.

Let us verify that functions and types are also objects:

```python
>>> def hello():
...     return "world"
...
>>> id(hello)
140735200843776
>>> type(hello)
<class 'function'>
>>> type(type)
<class 'type'>
```

Even `type` itself is an object of type `type`. This is the foundation of
Python's uniform object model.

**Real-world analogy:** Think of objects as houses on a street. Each house
has an address (its identity), a style (its type), and contents (its value).
When you tell Python `x = 42`, you are saying: "Take the label `x` and stick
it on the house that contains 42."

---

### 3. `id()` and `type()` — Who Am I and Where Do I Live?

#### `type()` — What kind of object is this?

`type()` returns the type of an object:

```python
>>> type(42)
<class 'int'>
>>> type([1, 2, 3])
<class 'list'>
>>> type("hello")
<class 'str'>
>>> type({"a": 1})
<class 'dict'>
>>> type({1, 2, 3})
<class 'set'>
>>> type((1, 2))
<class 'tuple'>
```

The type determines what operations are available on the object. Lists have
`.append()`, `.pop()`, and `.sort()`. Strings have `.upper()`, `.split()`,
and `.find()`. Integers have `.bit_length()` and `+`, `-`, `*`, `/`.

```python
>>> # Lists can be modified
>>> my_list = [1, 2, 3]
>>> my_list.append(4)  # Works

>>> # Tuples cannot
>>> my_tuple = (1, 2, 3)
>>> my_tuple.append(4)  # AttributeError!
```

The type of an object is fixed at creation and never changes. If you want a
different type, you must create a new object.

#### `id()` — Where does this object live?

`id()` returns a unique integer identifier for an object. In CPython (the
standard Python implementation), this is the memory address of the object.

```python
>>> a = [1, 2, 3]
>>> id(a)
140735200843776
```

Think of `id()` as the object's "home address" in computer memory. Two
variables share the same `id()` when they point to the exact same object.

```python
>>> b = a
>>> id(b) == id(a)
True
```

They are the same object. Both variables point to the same memory address.

```
Memory diagram:

Variable a ──→ Object A (id: 0x...100)
                  [value: [1, 2, 3]]
                  
Variable b ──→ Object A (id: 0x...100)
                  (same object! a and b are aliases)
                  
Variable c ──→ Object B (id: 0x...200)
                  [value: [1, 2, 3]]
                  (different object, same value)
```

**Real-world analogy:** The `id()` is a street address. Two different people
(variables) can live at the same address (reference the same object), or they
can live at different addresses (reference different objects). Just because
two houses look the same from the outside does not mean they are the same
house.

---

### 4. Mutable Objects — The Shapeshifters

A **mutable** object can change its value after it is created.

Think of mutable objects like a whiteboard. You can write on it, erase it,
and change what is written — but it is still the same whiteboard.

```python
>>> my_list = [1, 2, 3]
>>> id(my_list)
140735200843776
>>> my_list.append(4)
>>> my_list
[1, 2, 3, 4]
>>> id(my_list)  # Same object!
140735200843776
```

Even though the value changed, the identity stayed the same. The object
mutated in place.

```python
>>> my_dict = {"name": "Alice"}
>>> id(my_dict)
140735200843776
>>> my_dict["age"] = 30
>>> id(my_dict)  # Same object!
140735200843776
```

The dictionary was modified in place. The object itself changed.

```python
>>> my_set = {1, 2, 3}
>>> id(my_set)
140735200843776
>>> my_set.add(4)
>>> id(my_set)  # Same object!
140735200843776
```

Sets are also mutable. You can add and remove elements freely.

```
Mutable object in memory (before and after mutation):

Before:
my_list ──→ Object (id: 0x100)
                [1, 2, 3]

After my_list.append(4):
my_list ──→ Object (id: 0x100)  ← SAME object!
                [1, 2, 3, 4]
```

**Built-in mutable types:**

| Type | Example | Can modify? |
|------|---------|-------------|
| `list` | `[1, 2, 3]` | `.append()`, `.pop()`, `[] =` |
| `dict` | `{"a": 1}` | `[] =`, `.pop()`, `.update()` |
| `set` | `{1, 2, 3}` | `.add()`, `.remove()` |
| `bytearray` | `bytearray(b"abc")` | `[] =`, `.append()` |

---

### 5. Immutable Objects — The Bedrock

An **immutable** object cannot change its value after it is created.

Think of immutable objects like a printed book. Once the pages are printed,
you cannot change the text. If you want different text, you need a new book.

```python
>>> my_int = 42
>>> id(my_int)
140735200843776
>>> my_int += 1
>>> my_int
43
>>> id(my_int)  # Different object!
140735200843777
```

Wait — the `id()` changed? That is because `my_int += 1` did NOT modify the
integer `42`. It created a **new** integer `43` and assigned it to `my_int`.
The original `42` was left unchanged (and probably cleaned up by garbage
collection).

```python
>>> s = "hello"
>>> id(s)
140735200843776
>>> s += " world"
>>> id(s)  # Different object!
140735200843777
```

Same story with strings: the `+=` operator creates a brand new string.

```python
>>> t = (1, 2, 3)
>>> id(t)
140735200843776
>>> t += (4,)
>>> id(t)  # Different object!
140735200843777
>>> t[0] = 99  # This will fail
TypeError: 'tuple' object does not support item assignment
```

Tuples are immutable. You cannot change their elements. The `+=` operator
creates a new tuple.

```
Immutable object in memory:

Before:
my_int ──→ Object A (id: 0x100)
                [value: 42]

After my_int += 1:
my_int ──→ Object B (id: 0x200)  ← NEW object!
                [value: 43]

Object A (id: 0x100) still exists with value 42,
but nothing references it anymore (will be garbage collected).
```

**Built-in immutable types:**

| Type | Example | Modification behavior |
|------|---------|----------------------|
| `int` | `42` | Creates a new int |
| `float` | `3.14` | Creates a new float |
| `complex` | `1+2j` | Creates a new complex |
| `bool` | `True` | Creates a new bool |
| `str` | `"hello"` | Creates a new string |
| `tuple` | `(1, 2)` | Creates a new tuple |
| `frozenset` | `frozenset([1,2])` | Creates a new frozenset |
| `bytes` | `b"hello"` | Creates new bytes |

---

### 6. Lists of Mutable vs Immutable Built-in Types

| Mutable | Immutable |
|---------|-----------|
| `list` | `int` |
| `dict` | `float` |
| `set` | `complex` |
| `bytearray` | `bool` |
| | `str` |
| | `tuple` |
| | `frozenset` |
| | `bytes` |

A helpful mnemonic: if you can modify it in place with a method like
`.append()`, `.pop()`, `.add()`, or `.__setitem__()`, it is probably mutable.

Another way to think about it: ask yourself "can I change one part of this
object without changing its identity?" If yes, it is mutable. If any
"change" forces a new object, it is immutable.

```python
# Mutable: change content, same id
lst = [1, 2, 3]
original_id = id(lst)
lst[0] = 99
print(id(lst) == original_id)  # True

# Immutable: any change means new object
s = "abc"
original_id = id(s)
s = s.upper()
print(id(s) == original_id)  # False
```

---

### 7. Equality vs Identity — `==` vs `is`

This is one of the most commonly confused concepts in Python.

- **Equality (`==`):** Do two objects have the **same value**?
- **Identity (`is`):** Are two objects the **exact same object** in memory?

```python
>>> a = [1, 2, 3]
>>> b = [1, 2, 3]
>>> a == b
True
>>> a is b
False
```

`a` and `b` have the same value (`[1, 2, 3]`), so `==` is `True`. But they are
different objects in memory, so `is` is `False`.

```python
>>> c = a
>>> c is a
True
>>> c == a
True
```

When we assign `c = a`, `c` becomes an **alias** for `a`. They are literally
the same object.

```
Memory diagram:

a ──→ [1, 2, 3]  (id: 0x100)
b ──→ [1, 2, 3]  (id: 0x200)
c ──→ [1, 2, 3]  (id: 0x100, same as a)

a == b → True   (same value)
a is b → False  (different id)
a is c → True   (same id)
```

For immutable objects, this distinction is less visible because you cannot
change the value:

```python
>>> x = 42
>>> y = 42
>>> x is y  # True in CPython due to small integer caching
True
```

But this is an implementation detail. You should never rely on `is` for
value comparison of immutable types.

**Golden rule:** Use `is` when you care about object identity (checking for
`None`, `True`, `False`, singletons). Use `==` when you care about value
equality (the vast majority of cases).

```python
# Correct
if x is None:  # None is a singleton
    ...

if result is True:
    ...

# Correct
if my_list == [1, 2, 3]:
    ...

# WRONG
if my_list is [1, 2, 3]:  # This will be False even if values match
    ...
```

---

### 8. Variable Assignment and Aliasing

When you write `b = a`, Python does NOT copy the object. It copies the
**reference** (the memory address). Both `a` and `b` now point to the same
object.

```python
>>> a = [1, 2, 3]
>>> b = a          # b is an alias for a
>>> a.append(4)    # modify through a
>>> b              # b sees the change!
[1, 2, 3, 4]
```

This is called **aliasing**. Two names for the same object.

```
a ──→ [1, 2, 3, 4]
       ↑
b ────┘
```

For mutable objects, aliasing means you can modify the object through one
variable and the change is visible through all aliases. This is powerful but
can be dangerous if you do not expect it.

```python
>>> original = [1, 2, 3]
>>> alias = original
>>> original.append(4)
>>> alias
[1, 2, 3, 4]
```

For immutable objects, aliasing is harmless because you cannot change the
object:

```python
>>> x = 42
>>> y = x          # y is an alias for x
>>> x += 1         # creates NEW int 43, assigns to x
>>> y              # y still points to 42
42
```

```
Before x += 1:

x ──→ 42
y ──→ 42


After x += 1:

x ──→ 43  (new object)
y ──→ 42  (unchanged)
```

This is why integers, strings, and tuples behave "like you expect" — you
cannot accidentally modify them because they are immutable.

**How to make a real copy:**

If you want an independent copy of a list (not just an alias), you have
several options:

```python
original = [1, 2, 3]

# Option 1: slicing
copy1 = original[:]

# Option 2: list()
copy2 = list(original)

# Option 3: copy module (for deep copies)
import copy
copy3 = copy.copy(original)     # shallow copy
copy4 = copy.deepcopy(original) # deep copy

original[0] = 99
print(copy1)  # [1, 2, 3] — independent!
print(copy2)  # [1, 2, 3] — independent!
```

**Shallow vs Deep copy:**

A shallow copy creates a new container but the elements inside are still
shared:

```python
original = [[1, 2], [3, 4]]
shallow = copy.copy(original)
shallow[0].append(99)
print(original)  # [[1, 2, 99], [3, 4]] — modified!
```

A deep copy recursively copies everything:

```python
original = [[1, 2], [3, 4]]
deep = copy.deepcopy(original)
deep[0].append(99)
print(original)  # [[1, 2], [3, 4]] — unchanged!
```

---

### 9. How Python Passes Arguments to Functions

This is where the mutable/immutable distinction really matters.

Python uses a mechanism often called **"call by object reference"** or
**"pass by assignment."**

When you call a function, the parameter variable is assigned the reference
to the argument object. It is exactly the same as `b = a`.

```python
def modify(n):
    n.append(4)

my_list = [1, 2, 3]
modify(my_list)
print(my_list)  # [1, 2, 3, 4]
```

Inside the function, `n` is an alias for `my_list`. Both reference the same
list. When we call `n.append(4)`, the original list is modified.

```
Before function call:

my_list ──→ [1, 2, 3]

During function call:

my_list ──→ [1, 2, 3]
              ↑
n ────────────┘

After n.append(4):

my_list ──→ [1, 2, 3, 4]
              ↑
n ────────────┘
```

For immutable objects, "modification" inside the function does NOT affect the
caller — because what looks like modification is actually creating a new object
and reassigning the local variable:

```python
def increment(n):
    n += 1

a = 1
increment(a)
print(a)  # 1 — unchanged!
```

Inside `increment`, `n += 1` creates a new integer `2` and assigns it to the
local variable `n`. The original integer `1` (which `a` still points to) is
unchanged.

```
Before function call:

a ──→ 1

During function call:

a ──→ 1
      ↑
n ────┘

During n += 1:

a ──→ 1

n ──→ 2  (new object, local to function)
```

For mutable objects, reassignment inside the function also does NOT affect
the caller:

```python
def reassign(n):
    n = [4, 5, 6]   # n now points to a NEW object

my_list = [1, 2, 3]
reassign(my_list)
print(my_list)  # [1, 2, 3] — unchanged!
```

Inside the function, `n` was reassigned to a new list. But `my_list` still
points to the original list.

```
Before function call:

my_list ──→ [1, 2, 3]

During function call (step 1):

my_list ──→ [1, 2, 3]
              ↑
n ────────────┘

During function call (step 2: n = [4, 5, 6]):

my_list ──→ [1, 2, 3]

n ──→ [4, 5, 6]  (new object, my_list unaffected)
```

This explains tasks 14 through 18 in the project:

```python
# Task 14: l1.append(4) modifies the list in place
l1 = [1, 2, 3]
l2 = l1
l1.append(4)
print(l2)  # [1, 2, 3, 4]

# Task 15: l1 = l1 + [4] creates a new list
l1 = [1, 2, 3]
l2 = l1
l1 = l1 + [4]
print(l2)  # [1, 2, 3]

# Task 16: n += 1 creates a new integer
def increment(n):
    n += 1
a = 1
increment(a)
print(a)  # 1

# Task 17: n.append(4) modifies the list in place
def increment(n):
    n.append(4)
l = [1, 2, 3]
increment(l)
print(l)  # [1, 2, 3, 4]

# Task 18: n = v reassigns the local variable
def assign_value(n, v):
    n = v
l1 = [1, 2, 3]
l2 = [4, 5, 6]
assign_value(l1, l2)
print(l1)  # [1, 2, 3] — unchanged!
```

---

### 10. CPython Internals: Integer Caching

One of the most surprising optimizations in CPython is **integer caching**.

When you write:

```python
>>> a = 256
>>> b = 256
>>> a is b
True
>>> c = 257
>>> d = 257
>>> c is d
False  (in interactive mode)
```

Wait — `256 is 256` is `True`, but `257 is 257` is `False`? Yes!

CPython pre-allocates a fixed array of integer objects for small values. When
you use a small integer literal, Python simply returns a reference to the
pre-allocated object instead of creating a new one.

```
Memory diagram for small integers:

Small integer cache (allocated at CPython startup):
  [-5, -4, -3, ..., 0, 1, 2, ..., 255, 256]
   ↑                          ↑           ↑
   │                          │           └── index 261
   └── index 0                └── index 5

a = 256  →  points to cache[261]
b = 256  →  points to cache[261]  (same object!)

c = 257  →  new int object (not in cache)
d = 257  →  another new int object (not in cache)
```

This is an optimization based on the observation that small integers are used
extremely frequently in programs. Creating a new object each time would be
wasteful.

```python
>>> # Testing the caching range
>>> for i in range(-10, 260):
...     a = i
...     b = i
...     if a is not b:
...         print(f"{i} is NOT cached")
...
-10 is NOT cached
-9 is NOT cached
-8 is NOT cached
-7 is NOT cached
-6 is NOT cached
257 is NOT cached
258 is NOT cached
259 is NOT cached
```

The range [-5, 256] is cached. Everything outside that range creates new
objects.

---

### 11. NSMALLPOSINTS and NSMALLNEGINTS

In the CPython source code (file `Objects/longobject.c`), these caching limits
are defined as constants:

- `NSMALLPOSINTS` = 257 (covers integers 0 through 256)
- `NSMALLNEGINTS` = 5 (covers integers -5 through -1)

Together, they cache integers in the range **[-5, 256]**, which is 262 integers
total.

```c
#ifndef NSMALLPOSINTS
#define NSMALLPOSINTS           257
#endif
#ifndef NSMALLNEGINTS
#define NSMALLNEGINTS           5
#endif
```

CPython allocates an array of 262 integer objects at interpreter startup:

```c
static PyLongObject small_ints[NSMALLNEGINTS + NSMALLPOSINTS];
```

Every time you use an integer literal in this range, CPython returns a
reference to the pre-existing object from this array instead of allocating
new memory.

**Why these specific numbers?** Research and decades of experience showed that
the vast majority of integers used in typical programs fall within this range.
Index variables, loop counters, small offsets — almost all fit in [-5, 256].

```python
# These all use the cached integers
for i in range(100):  # i takes values 0-99, all cached
    pass

# Common operations use small integers
total = 0
for x in range(10):
    total += x  # 0-9 are cached

# Negative indices use cached values
my_list[-1]  # -1 is cached
my_list[-5]  # -5 is cached
```

Note: In a script file (as opposed to the interactive interpreter), CPython's
compiler also folds identical constants. So within the same `.py` file, even
`257` may reuse the same object because the compiler places the literal once
in the code object's `co_consts` table and references it multiple times.

---

### 12. Special Cases: Tuples Containing Mutable Objects

Here is where things get interesting. Tuples are immutable — you cannot add,
remove, or replace elements. But the objects **inside** a tuple can be mutable.

```python
>>> t = ([1, 2], [3, 4])
>>> t[0].append(99)
>>> t
([1, 2, 99], [3, 4])
```

Wait — we just modified a tuple? Not quite. The tuple still contains references
to the same two list objects. We just mutated one of those lists.

```
t ──→ ([1, 2, 99], [3, 4])
        ↑           ↑
        │           └── list B: [3, 4]
        │
        └── list A: [1, 2, 99]  (we mutated this list)
             changed from [1, 2]
```

The tuple itself was never modified. The references inside the tuple still
point to the same two list objects. It is the **contents** of one of those
lists that changed.

This is why the Python docs say "tuples are immutable" but add the important
qualification: "if the tuple contains a mutable object, that object can still
be modified."

A tuple is immutable only in the sense that you cannot change which objects it
references. You can still mutate those objects if they are mutable.

```python
>>> t = ([1], [2], [3])
>>> # This works: modifying the lists inside the tuple
>>> t[0].append(99)
>>> t[1].pop()
>>> # This does NOT work: reassigning a tuple element
>>> t[0] = [99]  # TypeError!
```

This distinction is crucial. When someone says an object is "immutable," they
mean its **reference count** and **contained references** are fixed. The
objects it references may still change.

**Practical implication:** A tuple of lists is not truly immutable. You can
use it as a dictionary key (because the tuple itself is hashable), but if you
modify a list inside it, you will corrupt the dictionary.

```python
>>> d = {([1],): "hello"}  # This works (tuple is hashable)
>>> d[([1],)]  # This might fail if the list was modified!
```

---

### 13. Frozen Sets

`frozenset` is the immutable version of `set`. Like tuples, frozensets are
immutable: you cannot add or remove elements after creation.

```python
>>> fs = frozenset([1, 2, 3])
>>> fs.add(4)
AttributeError: 'frozenset' object has no attribute 'add'
```

However, like tuples, frozensets can contain mutable objects (though in
practice, `frozenset` requires its elements to be hashable, and most mutable
objects are not hashable, so this rarely comes up).

```python
>>> fs = frozenset([[1, 2], [3, 4]])
TypeError: unhashable type: 'list'
```

The main use case for `frozenset` is when you need a set that is itself
hashable, for example as a dictionary key or as an element of another set.

```python
>>> valid_sets = {frozenset({1, 2}), frozenset({3, 4})}
>>> {1, 2} in valid_sets
True
```

Without `frozenset`, you cannot have a set of sets because `set` is mutable
and therefore not hashable.

```python
>>> set_of_sets = {{1, 2}, {3, 4}}
TypeError: unhashable type: 'set'
```

---

### 14. Interactive Mode vs Scripts: A Common Source of Confusion

One of the trickiest aspects of Python's object model is the difference
between running code in the interactive interpreter and running it as a
script file.

```python
# In interactive mode:
>>> a = "hello world"
>>> b = "hello world"
>>> a is b
False  (separate compilation units → separate objects)

# In a script file (same compilation unit):
a = "hello world"
b = "hello world"
print(a is b)  # True (same constant from co_consts)
```

When Python compiles a script, the entire file is compiled into a single code
object. All literal constants are stored in that code object's `co_consts`
table, and identical immutable literals are stored only once.

In interactive mode, each `>>>` line (or group of lines at a single prompt)
is compiled separately. So the same literal appearing on two different lines
creates two separate objects.

```python
# Script behavior:
x = 1000
y = 1000
print(x is y)  # True (same constant from co_consts)

# Interactive behavior:
>>> x = 1000
>>> y = 1000
>>> x is y  # False (separate objects)
```

This is why the project shows `>>>` prompts in some examples but the checker
runs your code as a script. Understanding this helps you predict which
answers depend on compilation mode.

---

### 15. Common Mistakes and Interview Questions

#### Mistake 1: Using `is` for value comparison

```python
# WRONG
if my_list is [1, 2, 3]:
    ...

# RIGHT
if my_list == [1, 2, 3]:
    ...
```

#### Mistake 2: Assuming function arguments are copies

```python
def add_item(item, target_list=[]):  # DANGER!
    target_list.append(item)
    return target_list

print(add_item(1))  # [1]
print(add_item(2))  # [1, 2] — surprise!
```

The default argument `[]` is evaluated ONCE at function definition time.
Every call shares the same list. Use `None` instead:

```python
def add_item(item, target_list=None):
    if target_list is None:
        target_list = []
    target_list.append(item)
    return target_list
```

#### Mistake 3: Confusing `+` and `+=` on lists

```python
# + creates a new list
a = [1, 2]
b = a
a = a + [3]
print(b)  # [1, 2] — unchanged

# += modifies in place (for mutable types)
a = [1, 2]
b = a
a += [3]
print(b)  # [1, 2, 3] — modified!
```

#### Mistake 4: Thinking tuple immutability prevents all changes

```python
t = ([1], [2])
t[0].append(99)  # Works! Tuple is immutable, but lists inside it are not
print(t)  # ([1, 99], [2])
```

#### Interview Question 1

Q: What does this print? Why?

```python
def func(x):
    x = x + [4]

y = [1, 2, 3]
func(y)
print(y)
```

A: `[1, 2, 3]`. Inside `func`, `x = x + [4]` creates a NEW list and assigns
it to the local variable `x`. The original list `y` is unchanged.

#### Interview Question 2

Q: What does this print? Why?

```python
def func(x):
    x += [4]

y = [1, 2, 3]
func(y)
print(y)
```

A: `[1, 2, 3, 4]`. Unlike `x = x + [4]`, `x += [4]` calls `__iadd__` on the
list, which modifies the list in-place and then assigns the same object back
to `x`. The original list is mutated.

#### Interview Question 3

Q: Why does `257 is 257` sometimes give different results?

A: In interactive mode, each `257` literal creates a new integer object
(257 is outside the small integer cache range [-5, 256]). In a script file,
the compiler merges identical integer literals into the same constant in
`co_consts`, so `257 is 257` is `True` in a script but `False` in interactive
mode.

#### Interview Question 4

Q: What is the difference between shallow copy and deep copy?

A: A shallow copy creates a new container but the elements inside reference
the same objects as the original. A deep copy recursively creates new copies
of all objects. Modifying a mutable element in a shallow copy affects the
original; in a deep copy it does not.

---

### 16. Best Practices

1. **Prefer `==` over `is` for value comparisons.** Use `is` only for `None`,
   `True`, `False`, and singletons.

2. **Use `copy.deepcopy()` for nested mutable structures** when you need a
   true independent copy.

   ```python
   import copy
   original = [[1, 2], [3, 4]]
   shallow = copy.copy(original)    # inner lists are shared
   deep = copy.deepcopy(original)    # everything is independent
   ```

3. **Avoid mutable default arguments.** Use `None` and create a new mutable
   inside the function.

4. **Use tuples for fixed collections** to signal that the data should not
   change. This makes your code more readable and safer.

5. **Document when a function modifies its arguments.** If your function
   mutates a list or dict passed in, make it clear in the docstring.

6. **Be aware of the small integer cache** when debugging identity checks.
   Never rely on `is` for integer comparison — always use `==`.

7. **Use `id()` sparingly.** In production code, you almost never need it.
   It is mainly useful for debugging and learning.

8. **When in doubt, test in the interpreter.** The fastest way to understand
   Python's behavior is to experiment. Open a REPL and try things.

---

### 17. Key Takeaways

- Everything in Python is an object with an identity, type, and value.
- `id()` returns the memory address (in CPython); `type()` returns the type.
- Mutable objects (list, dict, set, bytearray) can change in place.
- Immutable objects (int, str, tuple, frozenset, bytes) cannot change;
  any "modification" creates a new object.
- `==` checks value equality; `is` checks identity equality.
- Variable assignment (`b = a`) creates an alias — both names point to the
  same object.
- Python passes arguments by object reference (not by value, not by
  reference).
- Modifying a mutable argument inside a function affects the caller.
- Reassigning a parameter inside a function does NOT affect the caller.
- CPython caches small integers in the range [-5, 256] (NSMALLNEGINTS=5,
  NSMALLPOSINTS=257).
- Tuples are immutable, but they can contain mutable objects.
- Immutable objects with the same value are sometimes (but not always) the
  same object due to compiler optimizations and caching.
- In a script file, the compiler reuses identical immutable constants; in
  interactive mode, each line is compiled separately.

---

### 18. Conclusion

Understanding Python's object model is not an academic exercise. It is a
practical skill that will save you hours of debugging, help you write more
predictable code, and prepare you for technical interviews at top companies.

The key insight is simple: **know whether your objects are mutable or
immutable, and understand that variables are just names for objects in
memory.**

When you grasp this, you will never be surprised by how `append`, `+=`, or
function arguments behave again. You will write code that is cleaner, safer,
and more Pythonic.

Remember: everything is an object, variables are just labels, and mutability
determines what "change" really means.

Now go ahead — open a Python REPL and experiment. Try creating aliases,
mutating objects, checking identities. The best way to learn is by doing.
Every experiment will deepen your intuition, and soon the behavior will feel
natural.

---

*If you found this article helpful, please share it with your fellow Python
developers and leave a comment below. Happy coding!*
