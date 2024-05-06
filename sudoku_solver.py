def solvable(grid, r, c, v):
    for i in range(9):
        if grid[r][i] == v and i != c: return False
        if grid[i][c] == v and i != r: return False
    sr = r // 3 * 3
    sc = c // 3 * 3
    for i in range(3):
        for j in range(3):
            if grid[sr+i][sc+j] == v:return False
    return True
def solve(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                for k in range(1, 10):
                    if solvable(grid, i, j, k):
                        grid[i][j] = k
                        if solve(grid):
                            return True
                        grid[i][j] = 0
                return False
    return True