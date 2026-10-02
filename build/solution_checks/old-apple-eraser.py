def eraser_tool(pixel_graph):
    rows, cols = len(pixel_graph), len(pixel_graph[0])
    seen = [[False] * cols for _ in range(rows)]
    uses = 0
    for r in range(rows):
        for c in range(cols):
            if pixel_graph[r][c] == 'R' and not seen[r][c]:
                uses += 1
                stack = [(r, c)]
                seen[r][c] = True
                while stack:
                    x, y = stack.pop()
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and pixel_graph[nx][ny] == 'R' and not seen[nx][ny]:
                            seen[nx][ny] = True
                            stack.append((nx, ny))
    return uses

# ---- tests
assert eraser_tool(["RREEE", "RREEE", "EEREE", "EEERR"]) == 3
assert eraser_tool(["EE", "EE"]) == 0
assert eraser_tool(["RE", "ER"]) == 2
print('ok')
