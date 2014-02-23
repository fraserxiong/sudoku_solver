import threading
from sudoku import sudoku
import copy


class sudoku_solver(sudoku):

    def __init__(self, _2d_map: list)-> None:
        super().__init__(_2d_map)
        self.thread_list = []
        self.result_list = []
        
    def print_3d(self, _3d_map)-> None:
        _2d = self._3d_to_2d(_3d_map)
        result = '{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n==========={}==={}\n'.\
            format(_2d[0], _2d[1], _2d[2], _2d[3], _2d[4], _2d[5],\
                   _2d[6], _2d[7], _2d[8], len(self.thread_list),\
                   _3d_map[self.total_space_loc][self.total_space_loc])
        print(result)

    def start(self)-> None:
        num = 0
        _3d_map = s._3d
        new_loc = s.get_new_loc(_3d_map)
        row = new_loc[0]
        col = new_loc[1]
        answers = s._3d_answer(_3d_map, row, col)
        thread_list = []
        for answer in answers:
            new_3d = copy.deepcopy(self._3d)
            self.update_answer(new_3d, row, col, answer)
            print('new, ({}, {}), answer: {}, answers: {}, loop_num: {}'.format(row, col, answer, answers, num))
            if _3d_map[self.total_space_loc][self.total_space_loc] == 0:
                print('================================Done=============')
                self._3d_result.append(_3d_map)
                break
            elif self.no_result(new_3d):
                self.print_3d(new_3d)
                print('No solution')
                del new_3d
            elif self.has_same_num(new_3d):
                self.print_3d(new_3d)
                print('Same result')
                del new_3d
            else:
                new_loc = self.get_new_loc(new_3d) # new_loc[row][col]
                
                thread_list.append(\
                threading.Thread(\
                    target = self.put_num, args = (new_3d, new_loc[0], new_loc[1])))
                thread_list[-1].start()
                self.thread_list.append(thread_list[-1])
            num += 1
        for thread in thread_list:
            thread.join()        
        del _3d_map
        return        
        
    def put_num(self, _3d_map: list, row: int, col: int, thread_num:int =0)-> None:
        num = 0
        answers = self._3d_answer(_3d_map, row, col)
        thread_list = []
        print('thread long: {}'.format(len(self.thread_list)))
        for answer in answers:
            new_3d = copy.deepcopy(_3d_map)
            self.update_answer(new_3d, row, col, answer)
            print('++++++++ ({}, {}), answer: {}, answers: {}, loop_num: {}, left: {}'.format(row, col, answer, answers, num, _3d_map[self.total_space_loc][self.total_space_loc]))
            if new_3d[self.total_space_loc][self.total_space_loc] == 0 :
                print('================================Done=============')
                self.result_list.append(new_3d
                                        )
                break
            elif self.no_result(new_3d):
                self.print_3d(new_3d)
                print('No solution')
                del new_3d
            elif self.has_same_num(new_3d):
                self.print_3d(new_3d)
                print('Same result')
                del new_3d
            else:
                new_loc = self.get_new_loc(new_3d) # new_loc[row][col]
                thread_list.append(\
                threading.Thread(\
                    target = self.put_num, args = (new_3d, new_loc[0], new_loc[1], thread_num + 1)))
                thread_list[-1].start()
                self.thread_list.append(thread_list[-1])
            print('thread_num = {}, num = {}'.format(thread_num, num))
            num += 1
        for thread in thread_list:
            thread.join()        
        del _3d_map
        return

    def no_result(self, _3d_map: list)-> bool:
        '''
        Return True if the map has no result

        >>> sudo = sudoku_solver(sample)
        >>> sudo.no_result(noresult_3d)
        True
        >>> sudo.no_result(sample_3d)
        False
        '''
        for row in range(self.length):
            for col in range(self.length):
                if _3d_map[row][col][0] == 0 and _3d_map[row][col][1] == 0:
                    return True
        return False
    
    def _3d_answer(self, _3d_map, row: int, col: int)-> list:
        '''
        Return a list of answer for that space

        >>> sudo = sudoku_solver(sample)
        >>> sudo._3d_answer(sudo._3d, 0, 0)
        [7, 9]
        >>> sudo._3d_answer(sudo._3d,8, 8)
        [1, 5]
        '''   
        return _3d_map[row][col][2:]
    
    def update_answer(self, _3d_map: list, row: int, col: int, answer: int)-> None:
        '''
        Return a list of answer for that space

        >>> sudo = sudoku_solver(sample)
        >>> sudo.update_answer(sudo._3d, 0, 0, 7)
        >>> sudo._3d == update_3d
        True
        '''
        def update_row(_3d_map: list, row: int, answer: int)-> None:
            for col_num in range(self.length):
                if self._3d_space_is_empty(_3d_map, row, col_num)\
                    and col_num != col:
                    cur_space = _3d_map[row][col_num]
                    up_space = cur_space[2:]
                    try:
                        up_space.remove(answer)
                        _3d_map[row][col_num] = cur_space[:2] + up_space
                    except:
                        pass
                    else:
                        _3d_map[row][col_num][1] -= 1
                            
                    
        def update_col(_3d_map: list, col: int, answer: int)-> None:
            for row_num in range(self.length):
                if self._3d_space_is_empty(_3d_map, row_num, col)\
                   and row_num != row:
                    cur_space = _3d_map[row_num][col]
                    up_space = cur_space[2:]
                    try:
                        up_space.remove(answer)
                        _3d_map[row_num][col] = cur_space[:2] + up_space
                    except:
                        pass
                    else:
                        _3d_map[row_num][col][1] -= 1
                    
        def update_box(_3d_map: list, box: int, answer: int)-> None:
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
                    if self._3d_space_is_empty(_3d_map, row_num, col_num)\
                       and row_num != row and col_num != col:
                        cur_space = _3d_map[row_num][col_num]
                        up_space = cur_space[2:]
                        try:
                            up_space.remove(answer)
                            _3d_map[row_num][col_num] = cur_space[:2] + up_space
                        except:
                            pass
                        else:
                            _3d_map[row_num][col_num][1] -= 1       
        update_row(_3d_map, row, answer)
        update_col(_3d_map, col, answer)
        box_num = self.from_row_col_to_box(row, col)
        update_box(_3d_map, box_num, answer)
        _3d_map[row][col][1] = 0
        _3d_map[row][col][0] = answer
        _3d_map[self.total_space_loc][self.total_space_loc] -= 1
        _3d_map[row][self.total_space_loc] -= 1
        _3d_map[self.total_space_loc][col] -= 1
        del _3d_map[row][col][2:]
                    
    def get_new_loc(self, _3d_map: list)-> tuple:
        '''
        Return a tuple which is a location such that (row, col)
        and the location has least anser
        
        >>> sudo = sudoku_solver(sample)
        >>> sudo.get_new_loc(sample_3d)
        (0, 6)
        '''
        new_loc = []
        last_value = 10
        for row_num in range(self.length) :
            for col_num in range(self.length):
                cur_value = _3d_map[row_num][col_num][1]
                if last_value > cur_value and cur_value != 0:
                    new_loc = [row_num, col_num]
                    last_value = cur_value
        return (new_loc[0], new_loc[1])

    def _3d_space_is_empty(self, _3d_map: list, row: int, col: int)-> bool:
        '''
        Return True if there is no empty space left
        
        >>> sudo = sudoku_solver(sample)
        >>> sudo._3d_space_is_empty(sample_3d, 0, 0)
        True
        >>> sudo._3d_space_is_empty(sample_3d, 0, 2)
        False
        '''        
        return _3d_map[row][col][0] == 0.

    def has_same_num(self, _3d_map: list)-> bool:
        '''
        Return True if there is same number in row or col or box
        
        >>> sudo = sudoku_solver(sample)
        >>> sudo.has_same_num(same_3d)
        True
        >>> sudo.has_same_num(sample_3d)
        False
        '''
        row_list = [ [ _3d_map[row][col][0] for row in range(self.length) ] for col in range(self.length)]
        col_list = [ [ _3d_map[row][col][0] for col in range(self.length) ] for row in range(self.length)]
        box_list = [ [ _3d_map[row + row_factor * 3][col + col_factor * 3][0] \
                       for row in range(self.box_len) for col in range(self.box_len)] \
                    for row_factor in range(self.box_len) for col_factor in range(self.box_len)]
        for row, col, box in zip(row_list, col_list, box_list):
            for i in range(self.length):
                if row[i] in row[i + 1:] and row[i] != 0 \
                   or col[i] in col[i + 1:] and col[i] != 0\
                   or box[i] in box[i + 1:] and box[i] != 0:
                    return True
        return False

if __name__ == "__main__":
    
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

    same_3d = [[[1, 0], [0, 4, 6, 7, 8, 9], [2, 0], [5, 0], [0, 5, 4, 6, 7, 8, 9], \
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
              [9, 0], [8, 0], [0, 3, 1, 5, 7], [0, 2, 1, 5], 5], \
             [3, 6, 6, 4, 9, 4, 6, 6, 3, 47]]

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
              [9, 0], [8, 0], [0, 3, 1, 5, 7], [0, 2, 1, 5], 5], \
             [3, 6, 6, 4, 9, 4, 6, 6, 3, 47]]

    update_3d = [[[7, 0], [0, 3, 6, 8, 9], [2, 0], [5, 0], [0, 4, 4, 6, 8, 9], [1, 0], \
              [0, 0], [0, 1, 8],[3, 0], 4], \
             [[0, 0], [4, 0], [0, 2, 6, 8], [0, 3, 6, 7, 8], [0, 4, 3, 6, 7, 8], \
              [2, 0], [1, 0], [0, 3, 5, 7, 8], [9, 0], 5], \
             [[3, 0], [5, 0], [0, 2, 1, 8], [0, 2, 7, 8], [0, 3, 7, 8, 9], [0, 1, 8], \
              [0, 2, 2, 7], [4, 0], [6, 0], 5], \
             [[5, 0], [0, 3, 2, 8, 9], [4, 0], [1, 0], [0, 4, 2, 3, 6, 8], \
              [0, 3, 3, 6, 8], [0, 3, 2, 3, 6], [0, 2, 2, 3], [7, 0], 5], \
             [[0, 1, 2], [0, 3, 1, 2, 8], [0, 3, 1, 3, 8], [9, 0], [0, 5, 2, 3, 5, 6, 8], \
              [7, 0], [0, 5, 2, 3, 4, 5, 6], [0, 4, 1, 2, 3, 5], [0, 3, 1, 4, 5], 7], \
             [[6, 0], [0, 3, 1, 2, 7], [0, 3, 1, 3, 7], [0, 1, 2], [0, 3, 2, 3, 5], \
              [4, 0], [9, 0], [0, 4, 1, 2, 3, 5], [8, 0], 5], \
             [[1, 0], [3, 0], [0, 3, 5, 6, 7], [0, 3, 6, 7, 8], [0, 4, 5, 6, 7, 8], \
              [0, 3, 5, 6, 8], [0, 3, 4, 5, 7], [9, 0], [2, 0], 5], \
             [[8, 0], [0, 2, 2, 7], [9, 0], [4, 0], [0, 4, 1, 2, 5, 7], [0, 1, 5], \
              [0, 3, 3, 5, 7], [6, 0], [0, 2, 1, 5], 5], \
             [[4, 0], [0, 3, 2, 6, 7], [0, 3, 5, 6, 7], [3, 0], [0, 5, 1, 2, 5, 6, 7], \
              [9, 0], [8, 0], [0, 3, 1, 5, 7], [0, 2, 1, 5], 5], \
             [2, 6, 6, 4, 9, 4, 6, 6, 3, 46]]

    noresult_3d = [[[0, 0], [0, 4, 6, 7, 8, 9], [2, 0], [5, 0], [0, 5, 4, 6, 7, 8, 9], \
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
    import doctest
    doctest.testmod()

hard1 = [[1,0,0,0,4,2,0,0,0],\
         [0,0,2,0,1,0,5,0,0],\
         [0,0,0,7,0,0,0,3,0],\
         [2,0,0,0,0,0,0,5,0],\
         [0,9,0,5,7,1,0,2,0],\
         [0,4,0,0,0,0,0,0,3],\
         [0,2,0,0,0,9,0,0,0],\
         [0,0,8,0,2,0,7,0,0],\
         [0,0,0,3,8,0,0,0,6]]


s = sudoku_solver(hard1)
s.start()
s.print_3d(s.result_list[0])