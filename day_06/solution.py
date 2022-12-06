# %%
from collections import deque


def read_data():
    with open('input.txt') as f:
        while (c := f.read(1)) != '\n':
            yield c
            

def part1(): 
    stream = read_data()
    queue = deque()
    counter = {}

    for i, right in enumerate(stream, 1):
        
        queue.append(right)
        counter[right] = counter.get(right, 0) + 1
        
        if len(queue) < 4:
            continue
        
        if len(counter) == 4:
            return i
        
        left = queue.popleft()
        counter[left] -= 1
        if counter[left] == 0:
            counter.pop(left)
        
    
part1()