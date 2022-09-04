from tkinter import *
import tkinter.messagebox as mb
from random import randint
import time

tk = Tk()
tk.title("Игра: Морской бой")
c = Canvas(tk, width=600, height=300, bg='green')
c.pack()
tk.update()

#класс точка
class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    #метод для сравнения двух точек
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    #метод для вывода точки
    def __repr__(self):
        return f"({self.x}, {self.y})"


#родительский класс исключений
class BoardException(Exception):
    pass

class BoardOutException(BoardException):
    def __str__(self):
        return "Выстрел за доску!"

class BoardUsedException(BoardException):
    def __str__(self):
        return "Уже стреляли в эту клетку"

class BoardWrongShipException(BoardException):
    pass


#класс коробля
class Ship:
    #в конструктор передаем точку головы коробля (bow), длину коробля,
    #и расположение o (если o=0, то горизонтальное, если o=1, то вертикальное)
    def __init__(self, bow, l, o):
        self.bow = bow
        self.l = l
        self.o = o
        self.lives = l
    
    #метод формирует список кординат коробля
    @property
    def dots(self):
        ship_dots = []
        for i in range(self.l):
            cur_x = self.bow.x 
            cur_y = self.bow.y
            
            if self.o == 0:
                cur_x += i
            
            elif self.o == 1:
                cur_y += i
            
            ship_dots.append(Dot(cur_x, cur_y))
        #возвращаем список точек нашего коробля
        return ship_dots
    
    #проверяем попали в корабль или нет
    def shooten(self, shot):
        return shot in self.dots

#класс поле 
class Board:
    #в конструктор передаем нужно ли поле скрывать, размер, холст и кординаты нашего поля
    def __init__(self, hid , size, canv, x_start, y_start):
        self.size = size
        self.hid = hid
        self.canv = canv
        self.x_start = x_start
        self.y_start = y_start
        
        self.tags1 = ''

        #количество пораженных кораблей
        self.count = 0
        
        #заполняем наше поле ноликами
        self.field = [ ["O"]*size for _ in range(size) ]
        
        #в списке будут храниться занятые точки
        self.busy = []
        #список кораблей на доске, изначально он пустой
        self.ships = []

        #точка куда будем щелкать мышкой, по умолчанию присвоили кординаты (-1;-1),
        #чтобы потом можно было осуществить проверку попали в доску или нет
        self.dot_cliack_mouse = Dot (-1,-1)
        self.text = ''
        self.text1 = ''
        self.text2 = ''
    
    #в переменную res записываем нашу доску, для вывода потом на печать
    def __str__(self):
        res = ""
        res += "      1    2    3    4   5   6  "
        for i, row in enumerate(self.field):
            res += f"\n{i+1}   " + "   ".join(row) + "  "
        
        #на доске пользователя меняем "O" на "K"
        if self.hid:
            res = res.replace("K", "O")
        return res

    #метод рисует поле на холсте
    def print_draw(self):
        self.tags1 = 'компьютера' if self.hid else 'пользователя'
        self.canv.delete(self.tags1) #очистка поля перед тем как будем рисовать новое
        x = self.x_start
        y = self.y_start
        self.canv.create_text(x+110, y-40, text=self.text, justify=LEFT, fill='red', font="Times 13 italic bold", tag=self.tags1)
        self.canv.create_text(x+110, y-60, text=self.text1, justify=LEFT, fill='orange', font="Times 13 italic bold", tag=self.tags1)
        self.canv.create_text(x+110, y-80, text=self.text2, justify=LEFT, fill='lime', font="Times 13 italic bold", tag=self.tags1)
        self.canv.create_text(x+110, y+200, text='Доска '+self.tags1, justify=LEFT, fill='coral', font="Times 14 italic bold", tag=self.tags1)
        
        self.canv.create_text(x+110, y+75, text=self.__str__(), justify=LEFT, fill='cyan', font="Times 20 italic bold", tag=self.tags1)
        #рисуем линии поля желтым цветом
        for _ in range(7):
            self.canv.create_line(x, y , x, y + 185, fill='yellow', width=2, tag=self.tags1)
            x = x + 40
        x = self.x_start
        for i in range(7):
            self.canv.create_line(x, y , x+240, y, fill='yellow', width=2, tag=self.tags1)
            y = y + 30
            if i == 5: y = y + 5
               
           
    #проверяем выходит ли точка за пределы доски
    def out(self, d):
        return not((0<= d.x < self.size) and (0<= d.y < self.size))
    

    #обводим корабль по контуру крестиками и используем его для расстановки кораблей
    def contour(self, ship, verb = False):
         
         near = [
            (-1, -1), (-1, 0) , (-1, 1),
            (0, -1), (0, 0) , (0 , 1),
            (1, -1), (1, 0) , (1, 1)
         ]
         for d in ship.dots:
             for dx, dy in near:
                 cur = Dot(d.x + dx, d.y + dy)
                 if not(self.out(cur)) and cur not in self.busy:
                     if verb:
                         self.field[cur.x][cur.y] = " ∙ "
                     self.busy.append(cur) 


    #добавление коробля на доску
    def add_ship(self, ship):
        
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "K" 
            self.busy.append(d)
        
        self.ships.append(ship)
        self.contour(ship)


    def shot(self, d):
        if self.out(d):
            raise BoardOutException()
        
        if d in self.busy:
            raise BoardUsedException()
        
        self.busy.append(d)
        
        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb = True)
                    self.text = "Корабль уничтожен!"
                    return False
                else:
                    self.text = "Корабль ранен!"  
                    return True
        
        self.field[d.x][d.y] = " ∙ "
        self.text = "Мимо!"
        return False
    
    def begin(self):
        self.busy = []


#класс компьютера
class AI():
    def __init__(self, board, enemy, canv):
        self.board = board
        self.enemy = enemy
        self.canv = canv

    def move(self):
        try:
            target = Dot(randint(0, 5), randint(0, 5))
            self.enemy.text1 = 'Выстрел '+ str(target.x+1) +' : '+ str(target.y+1)
            self.enemy.print_draw()
            repeat = self.enemy.shot(target)
            return repeat
        except BoardException as e:
            self.enemy.text = e
            self.enemy.print_draw()
            

#класс пользователя
class User():
    def __init__(self, board, enemy, canv):
        self.board = board
        self.enemy = enemy
        self.canv = canv
        #будем ловить событие нажатие левой клавиши мыши, если произошло событие,
        # то вызываем медод get_row_column
        self.canv.bind_all("<Button-1>", self.get_row_column)
        self.dot_cliack_mouse = Dot(-1, -1)
        #переменная флаг, если пользователь мышкой сщелкнул по полю,
        #то выставляем ее в значение yes_click, а значение кординат записываем в переменную dot_cliack_mouse
        self.flag = 'no_click'

    def get_row_column(self, event):
        mouse_x = int(self.canv.winfo_pointerx() - self.canv.winfo_rootx())
        mouse_y = int(self.canv.winfo_pointery() - self.canv.winfo_rooty())
        x_board = self.enemy.x_start
        y_board = self.enemy.y_start
        x_step = 40
        y_step = 30
        board_row = -1
        board_column = -1
        
        for i in range(6):
            if mouse_x in range(x_board, x_board + x_step):
                board_column = i 
            if mouse_y in range(y_board, y_board + y_step):
                board_row = i 
            x_board = x_board + x_step
            y_board = y_board + y_step

        self.dot_cliack_mouse = Dot (board_row, board_column)
        self.flag = 'yes_click'

    def move(self):
        try:
            target = self.dot_cliack_mouse
            self.enemy.text1 = 'Выстрел '+ str(target.x+1) +' : '+ str(target.y+1)
            self.enemy.print_draw()
            repeat = self.enemy.shot(target)
            return repeat
        except BoardException as e:
            self.enemy.text = e


class Game:
    def __init__(self, size, canv, tk):
        self.size = size
        self.canv = canv
        self.tk = tk
        pl = self.random_board(40, 90)
        co = self.random_board(350, 90)
        co.hid = True
        
        self.ai = AI(co, pl, self.canv)
        self.ai.flag = False 
        self.us = User(pl, co, self.canv)
        self.us.flag = True 
    
    def random_board(self, x, y):
        board = None
        while board is None:
            board = self.random_place(x, y)
        return board
    
    def random_place(self, x, y):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(hid = False, size = self.size, canv=self.canv, x_start=x, y_start=y)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0,1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    
    def update_canvas(self):
        self.us.board.print_draw()
        self.us.enemy.print_draw()
        self.tk.update()

        
    def loop(self):
        num = 0
        self.us.enemy.text2 = 'Ходит пользователь!'
        self.update_canvas()
        repeat = None
        while True:  
            self.update_canvas()
            #если num четное, то ходит user, если нечетное то computer
            if num % 2 == 0 and self.us.flag == 'yes_click':
                self.update_canvas()
                repeat = self.us.move()
                if repeat == False:
                    num += 1
                if repeat == True or repeat is None:
                    self.us.flag = 'no_click'
                self.update_canvas()

            if num % 2 == 1:
                self.us.enemy.text2 = ''
                self.us.board.text2 = 'Ходит компьютер!'
                self.us.board.text = ''
                self.us.board.text1 = ''
                self.update_canvas()
                time.sleep(2)
                repeat = self.ai.move()
                self.update_canvas()
                if repeat == False:
                    num += 1
                    self.us.flag = 'no_click'
                    self.us.enemy.text2 = 'Ходит пользователь!'
                    self.us.enemy.text = ''
                    self.us.enemy.text1 = ''
                    self.us.board.text2 = ''
                    self.update_canvas()
                if repeat is None or repeat:
                    self.update_canvas()
                    time.sleep(3)
                
            #это условие чтобы дать последний ход компьютеру,
            #если до этого он выстрелили в точку в которую уже стрелял
            if repeat == True or repeat == False:
                if self.ai.board.count == 7 and self.us.board.count == 7:
                    self.us.enemy.text2 = ''
                    self.us.board.text2 = ''
                    self.update_canvas()
                    mb.showinfo("Информация", 'Ничья!')
                    break
                    
                if self.ai.board.count == 7:
                    self.us.enemy.text2 = ''
                    self.us.board.text2 = ''
                    self.update_canvas()
                    mb.showinfo("Информация", 'Пользователь выиграл!')
                    break
                
                if self.us.board.count == 7:
                    self.us.enemy.text2 = ''
                    self.us.board.text2 = ''
                    self.update_canvas()
                    mb.showinfo("Информация", 'Компьютер выиграл!')
                    break
                  
    def start(self):
        self.loop()       

def start1():
    c.delete('all')
    g = Game(6, c, tk)
    g.start() 

c.create_text(300, 30, text='Приветсвуем вас в игре морской бой!', justify=CENTER, fill='red', font="Times 15 italic bold")
c.create_text(300, 100, text='Правила игры:\n -cтрельба по короблям противника осуществляется \nлевой клавишей мыши. \n- если кораболь был ранен, то игроку дается еще один ход.', justify=LEFT, fill='coral', font="Times 15 italic bold")
c.create_text(150, 230, text='Обозначения на поле: \n"O" - нужно стрелять \n "X" - корабаль ранен \n"∙" - выстрел мимо \n"K" - корабль пользователя', justify=LEFT, fill='yellow', font="Times 15 italic bold")


btn=Button(text='СТАРТ', background="cyan", command=start1)
btn.pack()
tk.mainloop()



