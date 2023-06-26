# Approxi.py

Because why would you use decimals, when you could use overly complicated approximations.

## Requirements
Python 3.10

## Run

Generate output .tex for test values:

    py .\approxi.py

Import as module to approximate custom values using `approxi.approx(values: Iterable, depth: int)`, where `depth`controls the maximum number of nested expressions. This is not an efficient implementation, don't even ask how the runtime scales with `depth`, just use a somewhat shallow value.

## Todo
- [ ] CLI
- [ ] AppVar.simplify()
    - [ ] Nested expressions
- [ ] Arithemtic error handling
- [ ] Caching
- [ ] Parallel implementation
