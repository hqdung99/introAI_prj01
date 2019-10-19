# Project 01 of CSC14003: Search Algorithm

## Team info

## How to use

Please use file `example.ipynb` to check animated example for all levels

### use command line:
There are three arguments you need to focus on:
1. search_name: type of search that you want to use
2. input_file: your input file
3. allpoint_type: this argument is necessary when you choose search_name = 'AllPointSearch'

**_List of valid values for the arguments above:_**

- **search_name**: BFS, DFS, Greedy, A*, AllPointSearch

- **allpoint_type**: DP, BruteForce, Greedy

_For example_

**1. test blind search algorithms**

```
python3 main.py --search_name BFS --input_file sample_input.txt

python3 main.py --search_name DFS --input_file sample_input.txt

python3 main.py --search_name Greedy --input_file sample_input.txt
```

**2. A***

```
python3 main.py --search_name A* --input_file sample_input.txt
```

**3. level 3: get all points before reaching the goal**

```
python3 main.py --search_name AllPointSearch --input_file multi_points.txt --allpoint_type DP

python3 main.py --search_name AllPointSearch --input_file multi_points.txt --allpoint_type BruteForce

python3 main.py --search_name AllPointSearch --input_file multi_points.txt --allpoint_type Greedy
```