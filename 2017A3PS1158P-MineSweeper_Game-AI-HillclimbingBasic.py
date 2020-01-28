#!/usr/bin/env python
# coding: utf-8



"""
Created Year 2019

@author: EASHAN SAPRE
ID: 2017A3PS1158P
"""
from tkinter import *
from tkinter import messagebox
from random import randint
import time
import timeit

class setupwindow():
    def __init__(window): #window is the master object of the setup window
        window.root = Tk()
        window.root.title("SETUP")
        window.root.grid()

        window.finish = "N"

        labels = ["HEIGHT : (less then 15) ", "WIDTH: (less than 15) ", "Mines : "]
        window.label = ["","",""]
        window.entry = ["","",""]
        
        window.root.option_add('*Dialog.msg.width', 80)
        
        for i in range(3):
            window.label[i] = Label(text = labels[i])
            window.label[i].grid(row = i, column = 1)
            window.entry[i] = Entry()
            window.entry[i].grid(row = i, column = 2)

        window.startbutton = Button(text = "Start", command = lambda: setupwindow.onclick(window))
        window.startbutton.grid(column = 2)
        window.root.mainloop()

    def onclick(window):
        setupwindow.verification(window)
        if window.verf == "Y":
            window.finish = "Y"
            window.root.destroy()
            return window

    def verification(window):
        height = window.entry[0].get()
        width = window.entry[1].get()
        mines = window.entry[2].get()

        window.verf = "N"
        if height.isdigit() and width.isdigit() and mines.isdigit():
            height = int(height)
            width = int(width)
            mines = int(mines)

            if height > 0 and height <= 15:
                totalsquares = height * width

                if width > 0 and width <= 15:

                    if mines > 0:
                        if mines < totalsquares:
                            window.verf = "Y"
                            window.height = height
                            window.width = width
                            window.mines = mines

                        else:
                            messagebox.showerror("Invalid", "You cannot have more mines than squares!")
                            
                    else:
                        messagebox.showerror("Invalid", "You can't play minesweeper without mines!")
                else:
                    messagebox.showerror("Invalid", "Hight & Width values must be between 1 and 15")
            else:
                messagebox.showerror("Invalid", "Hight & Width values must be between 1 and 15")
        else:
            messagebox.showerror("Invalid", "All values must be integers")


class gamewindow():
    def __init__(s, setup):  #s is the master object of the main game for HillClimbing Basic
        s.height = setup.height
        s.width = setup.width
        s.mines = setup.mines
        s.start=0
        s.stop=0
        totalsquares = s.height * s.width
        s.score = 0
        s.score_max = totalsquares - s.mines
        s.count_agent_step = 0
        
        s.Explored_Mines_Squares = list()
        s.Explored_Squares = list()
        s.Next_in_Queue = list()        

        #GO_FLAG
        s.GO_FLAG = "F"
        
        s.root = Tk()
        s.root.title("MINESWEEPER")
        s.root.grid()

        s.finish = "N"
        s.maingrid = list()
        
        for i in range(s.height):
            s.maingrid.append([])
            for x in range(s.width):
                s.maingrid[i].append(" ")
                s.maingrid[i][x] = Button(height = 0, width = 3, font = "Calibri 15 bold", text = "", bg = "gray90", command = lambda i=i, x=x: gamewindow.onclick(s, i, x))
                s.maingrid[i][x].grid(row = i, column = x)
                s.maingrid[i][x].mine = "False"
       
        location = int (s.width /2)
        s.startbutton = Button(height = 0, width = (s.width*3), padx=5, pady=5, font = "Calibri 10 bold", text = "Click Here To Start!", bg = "gray90", command = lambda: gamewindow.firstClick(s))
        s.startbutton.grid(row =s.height + 1, columnspan= s.width, padx=5, pady=5)
               
        indexlist = list() 
        for i in range(totalsquares):
            indexlist.append(i)     
        indexlist = gamewindow.MineGenerator(s, indexlist)
        
        s.root.mainloop()
        
    def MineGenerator(s, indexlist):
        spaceschosen = list()  
        for i1 in range(s.mines):
            chosenspace = randint(0, len(indexlist) - 1)
            spaceschosen.append(indexlist[chosenspace])
            del indexlist[chosenspace]
        for i1 in range(len(spaceschosen)):
            xvalue = int(spaceschosen[i1] % s.width)
            ivalue = int(spaceschosen[i1] / s.width)
            s.maingrid[ivalue][xvalue].mine = "True"
        return indexlist
    

    def onclick(s,i,x):
        if s.GO_FLAG == "T":  
            gamewindow.Nextclick(s,i,x) 
        return
    
    def Countmines(s, i, x):
        combinationsi = [1, 0, 1, -1, -1, 1, -1, 0]
        combinationsx = [1, 1, -1, 1, -1, 0, 0, -1]
        minecount1 = 0
        for combinations in range(len(combinationsi)):
            tempi = i + combinationsi[combinations]
            tempx = x + combinationsx[combinations]
                    
            if tempi < s.height and tempx < s.width and tempi >= 0 and tempx >= 0:
                square_number =  ((tempi * s.width) + (tempx + 1))
                k = square_number
                if s.maingrid[tempi][tempx].mine == "True":
                    minecount1 = minecount1 + 1
                    s.maingrid[tempi][tempx].configure(bg = "Red", text = "*")
                    if k not in s.Explored_Mines_Squares:
                                    s.Explored_Mines_Squares.append(k)
        return minecount1
    
    def firstClick(s):

        # for hill climbing taking first row as y and random x
        agent_y = 0
        agent_x = randint(0, s.width - 1)
        s.start = timeit.default_timer()
         
        if s.GO_FLAG == "F":
            s.GO_FLAG = "T"
            
            if s.startbutton["state"] == "normal":
                s.startbutton["state"] = "disabled"
         
        agent_next_y = agent_y       
        agent_next_x =  agent_x     
        time.sleep(2)
        temp_con = s.score_max + s.mines
        loop_counter = 0

        square_number =  ((agent_next_y * s.width) + (agent_next_x + 1))
        k = square_number
        s.Next_in_Queue.append(k)
        loop_flag = len(s.Explored_Squares)
        #value of loop_counter is less than temp_con 
        while(loop_flag <= temp_con and agent_next_y < s.height and s.finish != "Y"):
            s.root.update()    
            if agent_next_x != 0:
                agent_next_x = int(agent_next_x % s.width) 
                
            if s.count_agent_step == 0:
                s.count_agent_step = s.count_agent_step + 1
                s.maingrid[agent_next_y][agent_next_x].configure(bg = "Blue")
                s.maingrid[agent_next_y][agent_next_x].invoke()
                time.sleep(1)
                
            else:
                square_number =  ((agent_next_y * s.width) + (agent_next_x + 1))     
                if s.maingrid[agent_next_y][agent_next_x]["relief"] != "sunken" and square_number not in s.Explored_Mines_Squares:
                    s.count_agent_step = s.count_agent_step + 1
                    s.maingrid[agent_next_y][agent_next_x].configure(bg = "Blue")
                    s.maingrid[agent_next_y][agent_next_x].invoke()
                    time.sleep(1)
                        
            loop_flag = len(s.Explored_Squares) 
            
        # end of while loop
        if s.finish == "Y":
            s.root.destroy()
           
        return s
        
        
    def Nextclick(s, i, x):
        colourlist = ["PlaceHolder", "Black", "Black", "Black", "Purple", "Black", "Maroon", "Gray", "Turquoise"]
        recursionloop_k = 0
        if s.maingrid[i][x]["text"] != "F" and s.maingrid[i][x]["relief"] != "sunken":
            if s.maingrid[i][x].mine == "False":
                s.score += 1
                combinationsi = [1, 1, -1, -1, 0, 1, -1, 0]
                combinationsx = [1, -1, 1, -1,-1, 0, 0, 1] 
                Flag_FirstA = 0
                minecount = 0
                minecount1 = 0
                for combinations in range(len(combinationsi)):
                    tempi = i + combinationsi[combinations]
                    tempx = x + combinationsx[combinations] 
                    if tempi < s.height and tempx < s.width and tempi >= 0 and tempx >= 0:
                        square_number =  ((tempi * s.width) + (tempx + 1))
                        k = square_number
                        if s.maingrid[tempi][tempx].mine == "True":
                            minecount = minecount + 1
                            s.maingrid[tempi][tempx].configure(bg = "Red", text = "*")   
                            if k not in s.Explored_Mines_Squares:
                                    s.Explored_Mines_Squares.append(k)
                            
                        else:
                            if s.maingrid[tempi][tempx]["relief"] != "sunken" and s.maingrid[tempi][tempx]["text"] != "*":
                                minecount1 = gamewindow.Countmines(s, tempi, tempx)
                                if minecount1 == 0:
                                    minecount1 = ""
                                s.maingrid[tempi][tempx].configure(text = minecount1, bg = "Green")
                            if k not in s.Explored_Squares:
                                    s.Explored_Squares.append(k)
                            if Flag_FirstA == 0 and s.maingrid[tempi][tempx]["relief"] != "sunken":
                                if  k not in  s.Next_in_Queue:
                                    s.Next_in_Queue.append(k)
                                    Flag_FirstA = 1
                            else:
                                s.maingrid[tempi][tempx]["relief"] = "sunken"
                
                # if minecount is 0 it will print "" as text on squares               
                if minecount == 0:
                    minecount = ""
                    
                square_number =  int((i * s.width) + (x + 1))
                k = square_number
                if  k not in  s.Explored_Squares:
                    s.Explored_Squares.append(k)
               
                if k not in s.Next_in_Queue:
                    s.maingrid[i][x].configure(text = minecount, relief = "sunken", bg = "Green")
                else:
                    s.maingrid[i][x].configure(text = minecount, relief = "sunken", bg = "Blue")

                if str(minecount).isdigit():
                    s.maingrid[i][x].configure(fg = colourlist[minecount])
                    
                time.sleep(1)
                s.root.update() 
                
                for i in s.Next_in_Queue: 
                    if(k == i):
                        poped_square = s.Next_in_Queue.pop(0)       
                
                if len(s.Next_in_Queue) > 0 and s.mines != len(s.Explored_Mines_Squares):
                    recursionloop_k = 1
                else: 
                    recursionloop_k = 0       
                
                # if there is next square in queue
                if recursionloop_k == 1:
                    n = len(s.Next_in_Queue) - 1
                    next_xy = s.Next_in_Queue[n]
                    if next_xy == 1:
                        ivalue = 0
                        xvalue = 0
                    else:
                        ivalue = int((next_xy - 1)/ s.width) 
                        xvalue = int((next_xy - 1) % s.width)
                
                    if ivalue >= 0 and ivalue < s.height and xvalue >=0 and xvalue < s.width:
                        if s.maingrid[ivalue][xvalue]["relief"] != "sunken":
                            s.count_agent_step = s.count_agent_step + 1
                            gamewindow.Nextclick(s, ivalue, xvalue)
                            
                if s.mines == len(s.Explored_Mines_Squares) and len(s.Explored_Squares) != s.score_max and s.finish == "N":
                    if s.count_agent_step == 0:
                            s.count_agent_step = s.count_agent_step + 1
                    s.stop = timeit.default_timer()
                    str2 ="Mines Explored in Steps:" + str(s.count_agent_step)+ "\n" + "Time taken:  " + str(s.stop-s.start) + " sec" + "\n" + "Mines Explored:" + str(len(s.Explored_Mines_Squares))
                    messagebox.showinfo("YOU Won: Explored Mines!", str2)
                    s.finish = "Y"

                    
                else:
                    if len(s.Explored_Squares) == s.score_max and s.mines == len(s.Explored_Mines_Squares) and s.finish == "N":
                        if s.count_agent_step == 0:
                            s.count_agent_step = s.count_agent_step + 1
                        s.stop = timeit.default_timer()
                        str2 ="Cost = " + str(s.count_agent_step) + "\n" + "Time taken:  " + str(s.stop-s.start) + " sec" + "\n" + "Mines Explored:" + str(len(s.Explored_Mines_Squares))
                        messagebox.showinfo("YOU WON GAME!", str2)
                        s.finish = "Y"
                        
                    else:
                        if recursionloop_k == 0 and s.finish == "N":
                            if s.count_agent_step == 0:
                                s.count_agent_step = s.count_agent_step + 1
                            s.stop = timeit.default_timer()
                            str2 ="Cost = " + str(s.count_agent_step) + "\n" + "Time taken:  " + str(s.stop-s.start) + " sec" + "\n" + "Mines Explored:" + str(len(s.Explored_Mines_Squares))     
                            messagebox.showinfo("Local Minima reached!", str2)
                            s.finish = "Y"

            else:
                s.maingrid[i][x].configure(bg = "Red", relief = "flat", text = "*")
                # if s.maingrid[i][x].mine is True, AND agent steps on unexplored mine first time then game over 
                square_number =  ((i * s.width) + (x + 1))
                k = square_number
                if  k not in  s.Explored_Mines_Squares:
                    for a in range(len(s.maingrid)):
                        for b in range(len(s.maingrid[a])):
                            if s.maingrid[a][b].mine == "True":
                                if s.maingrid[a][b]["text"] == "F":
                                    s.maingrid[a][b].configure(bg = "Green")
                                elif s.maingrid[a][b]["bg"] != "Red":
                                    s.maingrid[a][b].configure(bg = "Pink", text = "*")
                            elif s.maingrid[a][b]["text"] == "F":
                                s.maingrid[a][b].configure(bg = "Yellow")
                                
                    if s.count_agent_step == 0:
                        s.count_agent_step = s.count_agent_step + 1
                    #msgtext = "Steps are :" + str(s.count_agent_step)
                    s.stop = timeit.default_timer()
                    str1= "Cost = " + str(s.count_agent_step) + "\n" + "Time taken:  "  + str((s.stop-s.start)) +" sec"
                    msgtext = str1
                    messagebox.showinfo("YOU LOST GAME! ", msgtext)
                    s.finish = "Y"    
        
        recursionloop_k = 0
        
        return s          
                
    def Dialog1Display():
        Dialog1 = Toplevel(height=100, width=100) 
    
     
                            
                            
    def rightclick(event, s, i, x):
        if s.maingrid[i][x]["relief"] != "sunken":
            if s.maingrid[i][x]["text"] == "":
                s.maingrid[i][x].config(text = "F")
            elif s.maingrid[i][x]["text"] == "F":
                s.maingrid[i][x].config(text = "?")
            else:
                s.maingrid[i][x].config(text = "")


if __name__ == "__main__":
    setup = setupwindow()
    
    if setup.finish == "Y":
        game = gamewindow(setup)
    quit() 

