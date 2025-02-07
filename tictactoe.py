from tkinter import *
import numpy as np

board_size = 600
symbol_size = (board_size / 3 - board_size / 8) / 2
symbol_thickness = 50
symbol_X_color = '#FF69B4'
symbol_O_color = '#9ACD32'
Green_color = '#7BC043'

class tic_tac_toe():
     #init function
     def __init__(self):
          self.window = Tk()
          self.window.title('tic_tac_toe')
          self.canvas = Canvas(self.window, width=board_size, height=board_size)
          self.canvas.pack()

          # input from user in the form of clicks
          self.window.bind('<Button-1>', self.click)

          self.init_board()
          self.player_X_turns = True
          self.board_status = np.zeros(shape=(3,3))
          self.player_X_starts = True
          self.reset_board = False
          self.gameover = False
          self.tie = False
          self.X_wins = False
          self.O_wins = False

          self.X_score = 0
          self.O_score = 0
          self.tie_score = 0
     
     def mainloop(self):
          self.window.mainloop()

     def init_board(self):
          for i in range(2):
               self.canvas.create_line((i+1) * board_size /3, 0, (i+1)*board_size /3, board_size)
          
          for i in range(2):
               self.canvas.create_line(0, (i+1)* board_size/3, board_size, (i+1)* board_size/3)

     def play_again(self):
          self.init_board()
          self.player_X_starts = not self.player_X_starts
          self.player_X_turns = self.player_X_starts
          self.board_status = np.zeros(shape=(3,3))

     # drawing functions
     
     def draw_O(self, logical_pos):
          logical_pos = np.array(logical_pos)
          # logical pos is the grid value on the board
          # grid_pos = actual pixel values of the center of the grid
          grid_pos = self.convert_logical_to_grid_pos(logical_pos)
          self.canvas.create_oval(grid_pos[0] - symbol_size, grid_pos[1] - symbol_size,
                                    grid_pos[0] + symbol_size, grid_pos[1] + symbol_size, width=symbol_thickness,
                                    outline=symbol_O_color)
          
     def draw_X(self, logical_pos):
          grid_pos = self.convert_logical_to_grid_pos(logical_pos)
          self.canvas.create_line(grid_pos[0] - symbol_size, grid_pos[1] - symbol_size,
                                  grid_pos[0] + symbol_size, grid_pos[1] + symbol_size, width=symbol_thickness,
                                  fill=symbol_X_color)
          self.canvas.create_line(grid_pos[0] - symbol_size, grid_pos[1] + symbol_size,
                                  grid_pos[0] + symbol_size, grid_pos[1] - symbol_size, width=symbol_thickness,
                                  fill=symbol_X_color)
          
     def display_gameover(self):
          if self.X_wins:
               self.X_score += 1
               text = 'Winner: player 1(X)'
               color = symbol_X_color
          elif self.O_wins:
               self.O_score += 1
               text = 'Winner: player 2(O)'
               color = symbol_O_color
          else:
               self.tie_score += 1
               text = 'Its a tie'
               color = 'violet'
          
          self.canvas.delete("all")
          self.canvas.create_text(board_size / 2, board_size / 3, font="helvetica 50 bold", fill=color, text=text)

          score_text = 'Scores \n'
          self.canvas.create_text(board_size/2, 5* board_size/8, font="helvetica 30 bold", fill=Green_color,
                                  text=score_text)
          
          score_text = 'player 1(X): ' + str(self.X_score) + '\n'
          score_text += 'player 2 (O): ' + str(self.O_score) + '\n'
          score_text += 'Tie      : ' + str(self.tie_score)
          self.canvas.create_text(board_size/2, 3*board_size/4, font="helvetica 20 bold", fill=Green_color,
                                  text=score_text)
          self.reset_board = True
          score_text = 'Click to play again \n'
          self.canvas.create_text(board_size/2, 15*board_size/16, font="helvetica 20 bold", fill="gray",
                                  text=score_text)
          
     # Logical functions
          
     def convert_logical_to_grid_pos(self, logical_pos):
          logical_pos = np.array(logical_pos, dtype=int)
          return (board_size/3) * logical_pos+board_size/6

     def convert_grid_to_logical_pos(self,grid_pos):
          grid_pos = np.array(grid_pos)
          return np.array(grid_pos // (board_size /3), dtype=int)
     
     def is_grid_occupied(self, logical_pos):
          if self.board_status[logical_pos[0]][logical_pos[1]] ==0:
               return False
          else:
               return True
          
     def is_winner(self, player):
          player = -1 if player == 'X' else 1

          for i in range(3):
               if self.board_status[i][0] == self.board_status[i][1] == self.board_status[i][2] == player:
                    return True
               if self.board_status[0][i] == self.board_status[1][i] == self.board_status[2][i] == player:
                    return True
               
          # diagonals
          if self.board_status[0][0] == self.board_status[1][1] == self.board_status[2][2] == player:
               return True
          if self.board_status[0][2] == self.board_status[1][1] == self.board_status[2][0] == player:
               return True
          return False
     
     def is_tie(self):
          r, c = np.where(self.board_status == 0)
          tie = False
          if len(r) == 0:
               tie = True
          return tie
     
     def is_gameover(self):
          self.X_wins = self.is_winner('X')
          if not self.X_wins:
               self.O_wins = self.is_winner('O')

          if not self.O_wins:
               self.tie = self.is_tie()

          gameover = self.X_wins or self.O_wins or self.tie

          if self.X_wins:
               print('X wins')
          if self.O_wins:
               print('O wins')
          if self.tie:
               print('Its a tie')

          return gameover
     
     def click(self, event):
          grid_pos = [event.x, event.y]
          logical_pos = self.convert_grid_to_logical_pos(grid_pos)

          if not self.reset_board:
               if self.player_X_turns:
                    if not self.is_grid_occupied(logical_pos):
                         self.draw_X(logical_pos)
                         self.board_status[logical_pos[0]][logical_pos[1]] = -1
                         self.player_X_turns = not self.player_X_turns
               
               else:
                    if not self.is_grid_occupied(logical_pos):
                         self.draw_O(logical_pos)
                         self.board_status[logical_pos[0]][logical_pos[1]] = 1
                         self.player_X_turns = not self.player_X_turns

               # check if game is over
               if self.is_gameover():
                    self.display_gameover()
          else:
               self.canvas.delete("all")
               self.play_again()
               self.reset_board = False

game_instance = tic_tac_toe()
game_instance.mainloop()