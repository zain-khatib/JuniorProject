grid = [ [3, 0, 8, 4], [2, 4, 5, 7],[9, 2, 6, 3],[0, 3, 1, 0] ]
row = []
col = [] 
cols = 0
for i in grid:
    row.append(max(i))
    cols=len(i)
for i in range(0,cols):
    ls=[]
    for j in range(0,len(row)):
        ls.append(grid[j][i])
    col.append(max(ls))
ret = 0
print('row=')
print(row)
print('col=')
print(col)
for i in range(0,len(col)):
    for j in range(0,len(row)):
        ret += max(grid[j][i],min(row[j],col[i]))-grid[j][i]
print(ret)