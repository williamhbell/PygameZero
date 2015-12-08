Pygame Zero examples
====================

A collection of Python example programs, showing how to build up a simple game using the Pygame Zero package [ https://pygame-zero.readthedocs.org/en/latest/index.html ].

Written by W. H. Bell [ http://www.whbell.net/ ]

Running the examples
====================

Pygame Zero programs should be run using the pgzrun command.  For example,
```
pgzrun python/spacecraft.py
```

Each of the example programs can be closed by closing the graphical window.

Raspbian Wheezy
===============
The dependencies are not part of the current Raspbian Wheezy image.  Pygame Zero 1.1 does not work even when they are installed.  Typing,

```
./wheezy-patch/install-PygameZero.sh
```
will install the dependencies and patch Pygame Zero.
