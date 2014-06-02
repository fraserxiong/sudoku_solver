

sample = [[0,0,2,5,0,1,0,0,3],\
          [0,4,0,0,0,2,1,0,9],\
          [3,5,0,0,0,0,0,4,6],\
          [5,0,4,1,0,0,0,0,7],\
          [0,0,0,9,0,7,0,0,0],\
          [6,0,0,0,0,4,9,0,8],\
          [1,3,0,0,0,0,0,9,2],\
          [8,0,9,4,0,0,0,6,0],\
          [4,0,0,3,0,9,8,0,0]]
        # [3,6,6,4,9,4,6,6,3]

sample_3d = [[[0, 2, 7, 9], [0, 4, 6, 7, 8, 9], [2, 0], [5, 0], [0, 5, 4, 6, 7, 8, 9], \
              [1, 0], [0, 1, 7], [0, 2, 7, 8], [3, 0], 5], \
             [[0, 1, 7], [4, 0], [0, 3, 6, 7, 8], [0, 3, 6, 7, 8], [0, 4, 3, 6, 7, 8], \
              [2, 0], [1, 0], [0, 3, 5, 7, 8], [9, 0], 5], \
             [[3, 0], [5, 0], [0, 3, 1, 7, 8], [0, 2, 7, 8], [0, 3, 7, 8, 9], [0, 1, 8], \
              [0, 2, 2, 7], [4, 0], [6, 0], 5], \
             [[5, 0], [0, 3, 2, 8, 9], [4, 0], [1, 0], [0, 4, 2, 3, 6, 8], [0, 3, 3, 6, 8], \
              [0, 3, 2, 3, 6], [0, 2, 2, 3], [7, 0], 5], \
             [[0, 1, 2], [0, 3, 1, 2, 8], [0, 3, 1, 3, 8], [9, 0], [0, 5, 2, 3, 5, 6, 8], \
              [7, 0], [0, 5, 2, 3, 4, 5, 6], [0, 4, 1, 2, 3, 5], [0, 3, 1, 4, 5], 7], \
             [[6, 0], [0, 3, 1, 2, 7], [0, 3, 1, 3, 7], [0, 1, 2], [0, 3, 2, 3, 5], \
              [4, 0], [9, 0], [0, 4, 1, 2, 3, 5], [8, 0], 5], \
             [[1, 0], [3, 0], [0, 3, 5, 6, 7], [0, 3, 6, 7, 8], [0, 4, 5, 6, 7, 8], \
              [0, 3, 5, 6, 8], [0, 3, 4, 5, 7], [9, 0], [2, 0], 5], \
             [[8, 0], [0, 2, 2, 7], [9, 0], [4, 0], [0, 4, 1, 2, 5, 7], [0, 1, 5], \
              [0, 3, 3, 5, 7], [6, 0], [0, 2, 1, 5], 5], \
             [[4, 0], [0, 3, 2, 6, 7], [0, 3, 5, 6, 7], [3, 0], [0, 5, 1, 2, 5, 6, 7], \
              [9, 0], [8, 0], [0, 3, 1, 5, 7], [0, 2, 1, 5], 5], [3, 6, 6, 4, 9, 4, 6, 6, 3, 47]]


class sudoku:

    
    

    def __init__(self, _2d_map: list)-> None:
        '''
        initialize the 3d_map

        >>> sudo = sudoku(sample)
        >>> sudo._2d == sample
        True
        >>> sudo._3d == sample_3d
        True
        '''

        # 2d[10][10] contain the number of the space in empty
        # a 0 in any space means empty
        self._2d = _2d_map # 2d[row][col]
        self._3d = [] # 3d[row][col][hig]
        self.can_put = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.length = 9
        self.box_len = 3
        self.total_space_loc = 9
        self.init_3d_map()
        
    def __str__(self)-> str:
        _2d = self._3d_to_2d(self._3d)
        result = '{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}'.\
            format(_2d[0], _2d[1], _2d[2], _2d[3], _2d[4], _2d[5], _2d[6], _2d[7], _2d[8])
        return result
        
                
    def _3d_to_2d(self, _3d_map)-> list:
        _2d = []
        for i in range(self.length):
            _2d.append([])
            row = _3d_map[i]
            for col in range(self.length):
                _2d[i].append(row[col][0])
        return _2d
    

########## Initialize the 3d map ###############################

    def from_row_col_to_box(self, row: int, col: int)-> int:
        '''
        Retrun box_num by given row and col

        >>> sudo = sudoku(sample)
        >>> sudo.from_row_col_to_box(0, 0)
        0
        >>> sudo.from_row_col_to_box(0, 8)
        2
        >>> sudo.from_row_col_to_box(8, 0)
        6
        >>> sudo.from_row_col_to_box(8, 8)
        8
        '''
        box_num = 0
        if row < 3:
            if col // 3 == 1:
                box_num = 1
            elif col // 3 == 2:
                box_num = 2
        elif row < 6:
            if col // 3 == 0:
                box_num = 3
            elif col // 3 == 1:
                box_num = 4
            elif col // 3 == 2:
                box_num = 5
        elif row < 9:
            if col // 3 == 0:
                box_num = 6
            elif col // 3 == 1:
                box_num = 7
            elif col // 3 == 2:
                box_num = 8
        return box_num

    def row_check(self, row: int)-> list:
        '''
        Return the remain word that can put in the space at that row
        after the row check

        >>> sudo = sudoku(sample)
        >>> sudo.row_check(0)
        [4, 6, 7, 8, 9]
        >>> sudo.row_check(8)
        [1, 2, 5, 6, 7]
        '''
        result = self.can_put.copy()
        for cur_space in self._2d[row]:
            if cur_space in result:
                result.remove(cur_space)
        return result
    
    def row_space_count(self, row: int)-> int:
        '''
        Return the number of space at that row

        >>> sudo = sudoku(sample)
        >>> sudo.row_space_count(0)
        5
        >>> sudo.row_space_count(8)
        5
        '''
        result = 0
        for cur_space in self._2d[row]:
            if cur_space == 0:
                result += 1
        return result

    def col_check(self, col: int)-> list:
        '''
        Return the remain word that can put in the space at that col
        after the col check

        >>> sudo = sudoku(sample)
        >>> sudo.col_check(0)
        [2, 7, 9]
        >>> sudo.col_check(8)
        [1, 4, 5]
        '''
        result = self.can_put.copy()
        for row_num in range(self.length):
            cur_space = self._2d[row_num][col]
            if cur_space in result:
                result.remove(cur_space)
        return result
    
    def col_space_count(self, col: int)-> int:
        '''
        Return the number of space at that col

        >>> sudo = sudoku(sample)
        >>> sudo.col_space_count(0)
        3
        >>> sudo.col_space_count(8)
        3
        '''
        result = 0
        for row_num in range(self.length):
            cur_space = self._2d[row_num][col]
            if cur_space == 0:
                result += 1
        return result

    def box_check(self, box: int)-> list:
        '''
        Return the remain word that can put in the space at that box
        after the box check

        >>> sudo = sudoku(sample)
        >>> sudo.box_check(0)
        [1, 6, 7, 8, 9]
        >>> sudo.box_check(3)
        [1, 2, 3, 7, 8, 9]
        >>> sudo.box_check(8)
        [1, 3, 4, 5, 7]
        '''
        result = []
        cotain = []
        row_factor = 0
        col_factor = 0
        if box < 3:
            if box % 3 == 1:
                col_factor = 3
            elif box % 3 == 2:
                col_factor = 6
        elif box < 6:
            row_factor = 3
            if box % 3 == 1:
                col_factor = 3
            elif box % 3 == 2:
                col_factor = 6
        elif box < 9:
            row_factor = 6
            if box % 3 == 1:
                col_factor = 3
            elif box % 3 == 2:
                col_factor = 6
        for row_num in range(row_factor, self.box_len + row_factor) :
            for col_num in range(col_factor, self.box_len + col_factor):
                cotain.append(self._2d[row_num][col_num])
        for num in self.can_put:
            if num not in cotain:
                result.append(num)
        return result

    def _2d_space_is_empty(self, row: int, col: int)-> bool:
        '''
        Return true if the location at the space is 0

        >>> sudo = sudoku(sample)
        >>> sudo._2d_space_is_empty(0, 8)
        False
        >>> sudo._2d_space_is_empty(8, 8)
        True
        '''
        return self._2d[row][col] == 0

    def init_3d_map_data(self)-> None:
        '''
        Initialize the data in the map

        >>> sudo = sudoku(sample)
        >>> sudo._3d == sample_3d
        True
        '''
        row_list = [ self.row_check(row_num) for row_num in range(self.length)]
        col_list = [ self.col_check(col_num) for col_num in range(self.length)]
        box_list = [ self.box_check(box_num) for box_num in range(self.length)]
        for row_num in range(self.length) :
            for col_num in range(self.length):
                if self._2d_space_is_empty(row_num, col_num):
                    result = []
                    box_num = self.from_row_col_to_box(row_num, col_num)
                    for item in row_list[row_num]:
                        if item in col_list[col_num] and item in box_list[box_num]:
                            result.append(item)
                    self._3d[row_num][col_num].extend([len(result)] + result)
                else:
                    self._3d[row_num][col_num].append(0)
        col_space_list = []
        for row_num in range(self.length):
            self._3d[row_num].append(self.row_space_count(row_num))
        for col_num in range(self.length):
            col_space_list.append(self.col_space_count(col_num))
        self._3d.append(col_space_list)
        self._3d[self.total_space_loc].append(sum(col_space_list))
                    
    def init_3d_map(self)-> None:
        '''
        Initialize the the map

        >>> sudo = sudoku(sample)
        >>> sudo._3d == sample_3d
        True
        '''
        for row_num in range(self.length):
            self._3d.append([])
            for col_num in range(self.length):
                self._3d[row_num].append([self._2d[row_num][col_num]])
        self.init_3d_map_data()


######### End of Initialize the 3d map ##########################



if __name__ == "__main__":
    import doctest
    doctest.testmod()
