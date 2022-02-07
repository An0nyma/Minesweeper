import random

class Minesweeper:
    alphabet = 'abcdefghijklmnopqrstuvwxyz'.upper()
    
    def __init__(self, x_len, y_len):
        if not 10<=x_len<=26:
            raise ValueError(f"x_len must be a value between 10 and 26 but instead is: {x_len}")
        elif not 10<=y_len<=26:
            raise ValueError(f"y_len must be a value between 10 and 26 but instead is: {y_len}")
        self.x_len = x_len
        self.y_len = y_len
        self.num_mines = round(self.x_len * self.y_len * 0.2)
        self.grid = [[' ' for x in range(0, self.x_len)] for y in range(0, self.y_len)]
        self.grid_show = [[False for x in range(0, self.x_len)] for y in range(0, self.y_len)]
        self.grid_flag = [[False for x in range(0, self.x_len)] for y in range(0, self.y_len)]
        self.create_grid()
    
    def create_grid(self):
        empty_spots = []
        [[empty_spots.append([y, x]) for x in range(0, self.x_len)] for y in range(0, self.y_len)]
        
        half_y = round(self.y_len/2)
        half_x = round(self.x_len/2)
        to_remove = [
            [half_y, half_x],
            [half_y+1, half_x+1], [half_y-1, half_x-1],
            [half_y+1, half_x-1], [half_y-1, half_x+1],
            [half_y-1, half_x], [half_y-2, half_x], [half_y-3, half_x],
            [half_y+1, half_x], [half_y+2, half_x], [half_y+3, half_x],
            [half_y, half_x-1], [half_y, half_x-2], [half_y, half_x-3],
            [half_y, half_x+1], [half_y, half_x+2], [half_y, half_x+3],
            [self.y_len-1, self.x_len-1], [0, self.x_len-1], [self.y_len-1, 0], [0, 0]
        ]
        
        for _remove in to_remove:
            del empty_spots[empty_spots.index(_remove)]
        
        for i in range(0, self.num_mines):
            rand_mine = random.randint(0, len(empty_spots)-1)
            self.grid[empty_spots[rand_mine][0]][empty_spots[rand_mine][1]] = 'Ơ'
            del empty_spots[rand_mine]
        
        for _remove in to_remove:
            empty_spots.append(_remove)
        
        while len(empty_spots)>0:
            over_six, corners_over_two = [], []
            for spot in empty_spots.copy():
                num_surrounding_mines = 0
                surrounding_spots = self.surrounding_spots(spot)
                for surr_spot in surrounding_spots:
                    if self.grid[surr_spot[0]][surr_spot[1]]=='Ơ':
                        num_surrounding_mines += 1
                if num_surrounding_mines>6:
                    over_six.append([spot, num_surrounding_mines])
                elif ((spot[0]==0 and spot[1]==0) or (spot[0]==self.y_len-1 and spot[1]==0) or (spot[0]==0 and spot[1]==self.x_len-1) or (spot[0]==self.y_len-1 and spot[1]==self.x_len)) and num_surrounding_mines>2:
                    corners_over_two.append(spot)
                else:
                    del empty_spots[empty_spots.index(spot)]
                num_surrounding_mines = str(num_surrounding_mines) if num_surrounding_mines>0 else ' '
                self.grid[spot[0]][spot[1]] = num_surrounding_mines
            for spot in over_six:
                while spot[1]>6:
                    off_set_x = [-1, 1][random.randint(0, 1)]
                    off_set_y = [-1, 1][random.randint(0, 1)]
                    edited_spot = [spot[0][0]+off_set_y, spot[0][1]+off_set_x]
                    self.grid[edited_spot[0]][edited_spot[1]] = ' '
                    for rc in self.surrounding_spots(edited_spot):
                        empty_spots.append(rc)
                    spot[1] -= 1
            for spot in corners_over_two:
                side = self.surrounding_spots(spot)[:-1]
                side = side[random.randint(0, 1)]
                self.grid[side] = ' '
                for rc in self.surrounding_spots(side):
                    empty_spots.append(rc)
        
        zero_spots = []
        for y in range(0, self.y_len):
            for x in range(0, self.x_len):
                if self.grid[y][x]==' ':
                    zero_spots.append([y, x])
        self.zero_clusters = {}
        while len(zero_spots)>0:
            current_cluster = None
            for zero_spot in zero_spots:
                for cluster in self.zero_clusters.keys():
                    if True in [True if spot in self.zero_clusters[cluster] else False for spot in self.surrounding_spots(zero_spot)]:
                        current_cluster = cluster
                        break
                if current_cluster==None:
                    current_cluster = "cluster_"+str(len(self.zero_clusters.keys())+1)
                    self.zero_clusters[current_cluster] = []
                    self.zero_clusters[current_cluster].append(zero_spot)
                    del zero_spots[zero_spots.index(zero_spot)]
            for zero_spot in zero_spots.copy():
                if True in [True if spot in self.zero_clusters[current_cluster] else False for spot in self.surrounding_spots(zero_spot)]:
                    self.zero_clusters[current_cluster].append(zero_spot)
                    del zero_spots[zero_spots.index(zero_spot)]

        self.num_flags = 0
        for y in range(0, self.y_len):
            for x in range(0, self.x_len):
                if self.grid[y][x]=='Ơ':
                    self.num_flags += 1
        # self.num_mines = self.num_flags
    
    def flag(self, xy):
        # Debug tool
        # for y in range(0, self.y_len):
        #     for x in range(0, self.x_len):
        #         if self.grid[y][x]=='Ơ':
        #             self.grid_flag[y][x] = True
        # return
        try:
            xy = xy.replace(' ', '')
            x = self.alphabet.index(xy[0].upper())
            y = int(xy[1:])-1
            if x<0 or y<0:
                return False
            if self.grid_flag[y][x]==True:
                self.grid_flag[y][x] = False
                self.num_flags += 1
            else:
                self.grid_flag[y][x] = True
                self.num_flags -= 1
            return f"{'Flagged' if self.grid_flag[y][x] else 'Unflagged'} {xy}"
        except:
            return False
    
    def guess(self, xy, guess=True, bypass_flag=False):
        try:
            xy = xy.replace(' ', '')
            x = self.alphabet.index(xy[0].upper())
            y = int(xy[1:])-1
            if x<0 or y<0:
                return False
            if self.grid_show[y][x]==True:
                return True
            elif guess:
                if self.grid_flag[y][x]:
                    if bypass_flag:
                        self.grid_flag[y][x] = False
                    else:
                        return None
                self.grid_show[y][x] = True
            if not guess:
                return
            def check_cluster_and_around(self, y, x):
                for cluster in self.zero_clusters.keys():
                    if True in [True if spot in self.zero_clusters[cluster] else False for spot in self.surrounding_spots([y, x])]:
                        current_cluster = cluster
                        break
                for zero_spot in self.zero_clusters[current_cluster]:
                    for surr_spot in self.surrounding_spots([zero_spot[0], zero_spot[1]]):
                        self.grid_show[surr_spot[0]][surr_spot[1]] = True
                del self.zero_clusters[current_cluster]
            if self.grid[y][x]==' ':
                check_cluster_and_around(self, y, x)
            for surr_spot in self.surrounding_spots([y, x]):
                if self.grid[surr_spot[0]][surr_spot[1]]==' ':
                    self.grid_show[surr_spot[0]][surr_spot[1]] = True
                    check_cluster_and_around(self, *surr_spot)        
            return self.grid[y][x]
        except:
            return False
    
    def surrounding_spots(self, spot):
        surrounding_spots = []
        # Check sides
        if spot[0]!=0:
            surrounding_spots.append([spot[0]-1, spot[1]])
        if spot[1]!=0:
            surrounding_spots.append([spot[0], spot[1]-1])
        if spot[0]!=self.y_len-1:
            surrounding_spots.append([spot[0]+1, spot[1]])
        if spot[1]!=self.x_len-1:
            surrounding_spots.append([spot[0], spot[1]+1])
        # Check corners
        if spot[0]!=0 and spot[1]!=0:
            surrounding_spots.append([spot[0]-1, spot[1]-1])
        if spot[0]!=self.y_len-1 and spot[1]!=0:
            surrounding_spots.append([spot[0]+1, spot[1]-1])
        if spot[0]!=0 and spot[1]!=self.x_len-1:
            surrounding_spots.append([spot[0]-1, spot[1]+1])
        if spot[0]!=self.y_len-1 and spot[1]!=self.x_len-1:
            surrounding_spots.append([spot[0]+1, spot[1]+1])
        return surrounding_spots
    
    def lose(self):
        for y in range(0, self.y_len):
            for x in range(0, self.x_len):
                if self.grid[y][x]=='Ơ':
                    self.grid_show[y][x] = True
        self.grid_flag = [[False for x in range(0, self.x_len)] for y in range(0, self.y_len)]
        return self.pretty

    @property
    def won(self):
        for y in range(0, self.y_len):
            for x in range(0, self.x_len):
                if self.grid[y][x]!='Ơ' and self.grid_show[y][x]==False:
                    return False
        return True
    
    @property
    def pretty(self):
        hidden = [[self.grid[y][x] if self.grid_show[y][x] else '?' for x in range(0, self.x_len)] for y in range(0, self.y_len)]
        hidden = [['⚑' if self.grid_flag[y][x] else hidden[y][x] for x in range(0, self.x_len)] for y in range(0, self.y_len)]
        # hidden = [[self.grid[y][x] for x in range(0, self.x_len)] for y in range(0, self.y_len)]
        all_y = []
        for y in range(0, len(hidden)):
            row_num = str(y+1) if len(str(y+1))>1 else ' '+str(y+1)
            all_y.append(' '+row_num+' | '+'  '.join(hidden[y]))

        flags = f" Flags: {self.num_flags} "
        num_dashes = (self.x_len*3-len(flags))/2
        if str(num_dashes)[-2:]!='.0':
            flags += '-'
        num_dashes = int(num_dashes)
        pretty = '----+'+'-'*(num_dashes)+flags+'-'*(num_dashes)+'+\n'
        for y in range(len(all_y)-1, -1, -1):
            pretty += all_y[y]+' |\n'
        pretty += '----+'+'-'*(self.x_len*3)+'+'
        pretty += '\n    | '+'  '.join([self.alphabet[x] for x in range(0, self.x_len)])+' |'
        return pretty

import replit
def main():    
    while True:
        while True:
            try:
                x_len = int(input("How long should the board be? Between 10 and 26: "))
                y_len = int(input("How tall should the board be? Between 10 and 26: "))
                print("Initializing...")
                minesweeper = Minesweeper(x_len, y_len)
                replit.clear()
            except ValueError:
                replit.clear()
                print("One or more of your values were not correct. Please use integers in the specified ranges.")
            else:
                break
        while True:
            print(minesweeper.pretty)
            row_col = input("Letter and number: ")
            guess = minesweeper.guess(row_col.upper(), guess=False)
            if guess==False:
                replit.clear()
                print("Your input was not recognised. Please try again.")
                continue
            elif guess==True:
                replit.clear()
                print("You've already guessed this spot!")
                continue
            while True:
                action = input("Choose your action. Toggle flag (f), or guess (g): ").lower()
                if action in ['f', 'g']:
                    break
                else:
                    replit.clear()
                    print("Your input was not recognised. Please try again.")
                    print(minesweeper.pretty)
                    print(f"Letter and number: {row_col}")
            replit.clear()
            if action[0]=='g':
                guess = minesweeper.guess(row_col.upper())
                if guess==None:
                    guess_flag = input("\n(y/n) Are you sure you would like to guess a flagged spot? ").lower()
                    if guess_flag not in ['y', 'yes']:
                        return#asdf
                if guess=='Ơ':
                    print(f"Guessed {row_col} and revealed {guess}. You lose :(")
                    print(minesweeper.lose())
                    break
                elif minesweeper.won:
                    print(f"Guessed {row_col} and revealed {guess}. You win :)")
                    print(minesweeper.pretty)
                    break
                else:
                    print(f"Guessed {row_col} and revealed {guess}.")
            elif action[0]=='f':
                print(minesweeper.flag(row_col.upper()))
            else:
                print("Your input was not recognised. Please try again.")
        play_again = input("\n(y/n) Would you like to play again? ").lower()
        if play_again not in ['y', 'yes']:
            return

if __name__=='__main__':
    main()