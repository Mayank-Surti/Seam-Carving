import imagematrix

class ResizeableImage(imagematrix.ImageMatrix):
    def best_seam(self, dp=True):

        if dp == True: 
            return self.best_seam_dp()
        elif dp == False: 
            return self.best_seam_recr()

    def best_seam_dp(self):

        width = self.width
        height = self.height
        table = []
        path = {}

        for col in range(width):
            rows = []
            for row in range(height):
                rows.append([])
            table.append(rows)

        for col in range(width):
            table[col][0] = self.energy(col, 0)
            path[(col, 0)] = None
        
        for row in range(1, height):
            for col in range(width):
                if col == 0:
                    cost = self.energy(col, row) + min(table[col+1][row-1], table[col][row-1])
                    table[col][row] = cost
                    if table[col+1][row-1] > table[col][row-1]:
                        path[(col, row)] = (col, row-1)
                    else:
                        path[(col, row)] = (col+1, row-1)

                elif col == width - 1:
                    cost = self.energy(col, row) + min(table[col-1][row-1], table[col][row-1]) 
                    table[col][row] = cost
                    if table[col-1][row-1] > table[col][row-1]:
                        path[(col, row)] = (col, row-1)
                    else:
                        path[(col, row)] = (col-1, row-1)

                else:
                    cost = self.energy(col, row) + min(table[col+1][row-1], table[col-1][row-1], table[col][row-1]) 
                    table[col][row] = cost
                    prev = min(table[col+1][row-1], table[col-1][row-1], table[col][row-1])
                    if prev == table[col+1][row-1]:
                        path[(col ,row)] = (col+1, row-1)
                    elif prev == table[col-1][row-1]:
                        path[(col, row)] = (col-1, row-1)
                    else: 
                        path[(col, row)] = (col, row-1)
                
        new_path = []
        cost = float('inf')

        for col in range(width):
            if table[col][height-1] < cost:
                cost = table[col][height-1]
                end_col = col
        
        next_col = end_col
        next_row = height-1
        new_path.append((next_col, next_row))

        while next_row != 0:
            next_step = path[(next_col, next_row)]
            next_col = next_step[0]
            next_row = next_step[1]
            new_path.append((next_col, next_row))

        return list(reversed(new_path))


    def best_seam_recr(self):

        width = self.width
        height = self.height

        def helper(col, row):
            if row == 0:
                return [(col, row)], self.energy(col, row)

            energy = self.energy(col, row)
            best_cost = float('inf')
            new_path = []

            if col == 0:
                p1, c1 = helper(col, row-1)
                p2, c2 = helper(col+1, row-1)
                total = min(c1, c2) + energy

                if total < best_cost:
                    best_cost = total
                    if c1 > c2:
                        new_path = p2
                    else:
                        new_path = p1
            elif col == width-1:
                p1, c1 = helper(col, row-1)
                p2, c2 = helper(col-1, row-1)
                total = min(c1, c2) + energy

                if total < best_cost:
                    best_cost = total
                    if c1 > c2:
                        new_path = p2
                    else:
                        new_path = p1
            else:
                p1, c1 = helper(col, row-1)
                p2, c2 = helper(col-1, row-1)
                p3, c3 = helper(col+1, row-1)
                total = min(c1, c2, c3) + energy

                if total < best_cost:
                    best_cost = total
                    lowest_cost = min(c1, c2, c3)
                    if lowest_cost == c1:
                        new_path = p1
                    elif lowest_cost == c2:
                        new_path = p2
                    else:
                        new_path = p3
            
            new_path.append((col, row))
            return new_path, best_cost
        
        final_cost = float('inf')
        final_path = []
        for col in range(width):
            path, cost = helper(col, height-1)
            if cost < final_cost:
                final_cost = cost
                final_path = path

        return list(reversed(final_path))