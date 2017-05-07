# pygraph
A graph manipulation library in pure Python

Pygraph aims to be an easy-to-use and functional graph library that doesn't sacrifice advanced capabilities or usability in the process.

By implementing the library in pure Python, it can be installed without any dependencies aside from the Python core, enabling maximum ease of use.

Graph Types Supported:
* Directed Graphs
* Undirected Graphs

Common Algorithms Supported:
* DFS
* BFS
* Minimum Spanning Tree
* Connected Components
* Biconnected Components
* Articulation Vertices

Advanced algorithms supported will include:
* Triconnected Components
* Separation Pairs
* Lipton-Tarjan Separator Theorem
* Planarity Testing
* Fully Dynamic Planarity Testing
* Planar Embedding

## Current Algorithm Support
Algorithm | Status
--------- | ------
DFS | :white_check_mark: Supported
BFS | :white_check_mark: Supported
MST | :white_check_mark: Supported
Connected Components | :white_check_mark: Supported
Biconnected Components | :white_check_mark: Supported
Triconnected Components | :x: Unsupported
Articulation Vertices | :white_check_mark: Supported
Separation Pairs | :x: Unsupported
L-T Separator Theorem | :x: Unsupported
Planarity Testing | :white_check_mark: Supported
Planar Embedding | :x: Unsupported
Fully-Dynamic Planarity Testing | :x: Unsupported


## Running the Test Suite
The entire test suite is written using the standard library unittest module, so you should be able to run it with whichever framework you most prefer. We recommend [nose](http://nose.readthedocs.io/).

With nose installed, navigate to the root of the project and run `nosetests`. It should recognize the `tests` subdirectory and run through the entire test suite.

All algorithm implementations should have test cases written and passing.


## Contributions
Contributions are more than welcome! Algorithm suggestions, implementations, or even additional tests for existing algorithms are all great ways to contribute. Not a coder? That's fine too! This project is in dire need of documentation and examples.

### Planarity Test Cases
The planarity testing algorithm is extremely complicated. As such, more tests with more graphs are desired. Good sources of known graphs are:

* [WolframAlpha Planar Graphs](http://mathworld.wolfram.com/PlanarGraph.html)
* [WolframAlpha Non-Planar Graphs](http://mathworld.wolfram.com/NonplanarGraph.html)

For non-planar graphs, priority should be given to ones that don't fall afoul of Euler's Formula, so that the actual planarity testing algorithm is tested.