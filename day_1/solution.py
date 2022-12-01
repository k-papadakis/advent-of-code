# %%
with open('input.txt') as f:
    data_string = f.read()

# %%
max_ = max(sum(map(int, s.split('\n'))) for s in data_string[:-1].split('\n\n'))

print(f"Max: {max_}")

# %%
sum_top_3 = sum(sorted(sum(map(int, s.split('\n'))) for s in data_string[:-1].split('\n\n'))[-3:])

print(f"Top 3 sum: {sum_top_3}")

# %%
