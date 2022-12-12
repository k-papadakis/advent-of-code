# %%
def read_data(input_file):
    with open(input_file) as f:
        for line in f:
            if line.startswith('noop'):
                yield None
            else:  # line.startswith('add')
                yield int(line.split()[1])

def part1(ops):
    cycle_start, cycle_end = None, 1
    x = 1
    res = 0

    for op in ops:
        if op is None:
            cycle_start, cycle_end = cycle_end, cycle_end + 1
        else:
            cycle_start, cycle_end = cycle_end, cycle_end + 2
            
        for cycle in range(20, 221, 40):
            if cycle_start <= cycle < cycle_end:
                res += cycle * x
        
        if op is not None:
            x += op
        
    return res


print(part1(read_data('input.txt')))
    