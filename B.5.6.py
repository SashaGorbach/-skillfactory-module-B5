from tkinter import *
import tkinter.messagebox as mb


tk = Tk()
tk.title("Крестики-нолики")
c = Canvas(tk, width=300, height=300, bg='green')
c.pack()
tk.update()

#список будет состоять из девети ячеек, ячейка соответствует полю на доске
#в списке может храниться три значения 0 - клетка пустая; 1- крестик в поле; 2 - нолик в поле
List_Field = [0, 0, 0, 0, 0, 0, 0, 0, 0]
#с помощью этой переменой будем определять первый или второй игрок ходит будет принимать значения 1 или 2
Flag_Move = 1
#переменная которую будем использовать для вывода текстовой инвормации
l1=None
#логическая переменная для определения конца игры
END_Game = False 

def Start_Game ():
    global List_Field, l1, END_Game, Flag_Move
    END_Game = False
    c.delete("all") #очистка холста
    List_Field = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    Flag_Move = 1 # крестики всегда будут ходить первые
    #рисуем поле
    c.create_line(100, 0, 100, 300, fill='orange', width=3)
    c.create_line(200, 0, 200, 300, fill='orange', width=3)
    c.create_line(0, 100, 300, 100, fill='orange', width=3)
    c.create_line(0, 200, 300, 200, fill='orange', width=3)
    #разрушаем label если сыграли уже одну партию
    if l1 is not None:
        l1.destroy()
    #записываем информацию в label, чтобы было понятно, кто ходит следующий
    l1=Label(text='Ходит первый игрок (крестики)', background='lightgreen')
    l1.pack()
    

    
#процедура рисует или крестик или нолик в зависимости чья очередь ходить
#в нее передаются координаты квадрата, по которому сщелкнули мышкой, а
#также индекс списка, благодаря которому вносится информация в итоговый список 
def Draw_Cross_or_Toe (x, y, number_list):
    global Flag_Move, List_Field , l1
    if Flag_Move == 1:
        Flag_Move = 0
        List_Field [number_list] = 1
        #рисуем крест
        c.create_line(x + 10, y + 10, x + 90, y + 90, fill='blue', width=2)
        c.create_line(x + 90, y + 10, x + 10, y + 90, fill='blue', width=2)
        l1.destroy()
        l1=Label(text='Ходит второй  игрок (нолики)', background='lightgreen')
        l1.pack()
    else:
        Flag_Move = 1
        List_Field [number_list] = 2
        #рисуем ноль
        c.create_oval(x + 10, y + 10, x + 90, y + 90, outline='blue', width = 2)
        l1.destroy()
        l1=Label(text='Ходит первый игрок (крестики) ', background='lightgreen')
        l1.pack()
    
#процедурой проверяем произошла победа, ничья или продолжаем дальше играть
def Game_Over_Check ():
    global List_Field
    if ((List_Field[0] == List_Field[1] and List_Field[1] == List_Field[2] and List_Field[2] != 0) or #проверка первой строки
        (List_Field[3] == List_Field[4] and List_Field[4] == List_Field[5] and List_Field[5] != 0) or #проверка второй строки
        (List_Field[6] == List_Field[7] and List_Field[7] == List_Field[8] and List_Field[8] != 0) or #проверка третьей строки
        (List_Field[0] == List_Field[3] and List_Field[3] == List_Field[6] and List_Field[6] != 0) or #проверка первого столбца
        (List_Field[1] == List_Field[4] and List_Field[4] == List_Field[7] and List_Field[7] != 0) or #проверка второго столбца
        (List_Field[2] == List_Field[5] and List_Field[5] == List_Field[8] and List_Field[8] != 0) or #проверка третьего столбца
        (List_Field[0] == List_Field[4] and List_Field[4] == List_Field[8] and List_Field[8] != 0) or #проверка гланой диоганали
        (List_Field[2] == List_Field[4] and List_Field[4] == List_Field[6] and List_Field[6] != 0)    #проверка второстепеной диоганали
        ):
        return True, 'Победа'
    elif ( #если весь список заполнен не нулями, а победа не наступила, значит ничья
    List_Field[0] != 0 and List_Field[1] != 0 and List_Field[2] != 0 and
    List_Field[3] != 0 and List_Field[4] != 0 and List_Field[5] != 0 and
    List_Field[6] != 0 and List_Field[7] != 0 and List_Field[8] != 0
        ):
        return True, 'Ничья'
    else:
        return False, 'Игра продолжается'
    
       
def Сlick_Mouse(event):
    global END_Game, l1    
    #проверка, наступил конец игры
    if not END_Game: 
        #определяем кординаты мышки где был сделан щелчок
        mouse_x = int(c.winfo_pointerx() - c.winfo_rootx())
        mouse_y = int(c.winfo_pointery() - c.winfo_rooty())

        #если щелчок был в левом верхнем квадрате, то рисуем нолик или крестик
        if mouse_x in range(0,100) and mouse_y in range(0,100) and List_Field[0] == 0:
            Draw_Cross_or_Toe(0, 0, 0)
        #если щелчок был в среднем верхнем квадрате, то рисуем нолик или крестик
        if mouse_x in range(100,200) and mouse_y in range(0,100) and List_Field[1] == 0:
            Draw_Cross_or_Toe(100, 0, 1)
        #если щелчок был в правом верхнем квадрате, то рисуем нолик или крестик
        if mouse_x in range(200,300) and mouse_y in range(0,100) and List_Field[2] == 0:
            Draw_Cross_or_Toe(200, 0, 2)
        #если щелчок был в левом центральном квадрате, то рисуем нолик или крестик
        if mouse_x in range(0,100) and mouse_y in range(100,200) and List_Field[3] == 0:
            Draw_Cross_or_Toe(0, 100, 3)
        #если щелчок был в среднем центральном квадрате, то рисуем нолик или крестик
        if mouse_x in range(100,200) and mouse_y in range(100,200) and List_Field[4] == 0:
            Draw_Cross_or_Toe(100, 100, 4)
        #если щелчок был в правом центральном квадрате, то рисуем нолик или крестик
        if mouse_x in range(200,300) and mouse_y in range(100,200) and List_Field[5] == 0:
            Draw_Cross_or_Toe(200, 100, 5)
        #если щелчок был в левом нижнем квадрате, то рисуем нолик или крестик
        if mouse_x in range(0,100) and mouse_y in range(200,300) and List_Field[6] == 0:
            Draw_Cross_or_Toe(0, 200, 6)
        #если щелчок был в среднем нижнем квадрате, то рисуем нолик или крестик
        if mouse_x in range(100,200) and mouse_y in range(200,300) and List_Field[7] == 0:
            Draw_Cross_or_Toe(100, 200, 7)
        #если щелчок был в правом нижнем квадрате, то рисуем нолик или крестик
        if mouse_x in range(200,300) and mouse_y in range(200,300) and List_Field[8] == 0:
            Draw_Cross_or_Toe(200, 200, 8)

        #получаем данные о том произошла победа или ничья, если нет играем дальше
        Tuple_Game_Over = Game_Over_Check()
        if Tuple_Game_Over[0]:
            END_Game = True
            l1.destroy() # разрушаем Label так как конец игры
            if Tuple_Game_Over[1] == 'Победа':
                if Flag_Move == 1:
                    mb.showinfo("Информация", 'Победил Игрок 2 (нолики)!') #вывод информационного сообщения
                else:
                    mb.showinfo("Информация", 'Победил Игрок 1 (крестики)!') #вывод информационного сообщения
            else:
                mb.showinfo("Информация", 'Ничья!') #вывод информационного сообщения
        

#создаем кнопку, при нажатии на которую запускается функция Start_Game    
BtnStart=Button(text='Старт', command=Start_Game, background='lightblue', width=13)
BtnStart.pack(padx = 5, pady = 5)

#запускается событие при нажатии на левую клавишу мыши и вызывается функция Сlick_Mouse
c.bind_all("<Button-1>", Сlick_Mouse)
tk.mainloop()
