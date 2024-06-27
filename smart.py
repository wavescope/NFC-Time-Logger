# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 23:32:14 2024

@author: mcmah
"""
#Useful links
#https://pyscard.sourceforge.io/pyscard-wrapper.html#
#https://rpi4cluster.com/python-nfc-writer-reader/
#https://realpython.com/python-gui-tkinter/ 
#https://www.reddit.com/r/Crostini/comments/lc5p7n/tkinter_not_opening_a_window_when_using_spyder_3/

from smartcard.Exceptions import NoCardException
from smartcard.System import readers
from smartcard.util import toHexString
import sys
from tkinter import *
from tkinter import ttk
from time import sleep
from datetime import datetime
from PIL import Image, ImageTk
import itertools
import csv


sleepTime = 0 #counter for no card delay
Pcard = "ready" #string to set state of 
pathofCSV = 'time.csv'



def destroy_window():
    win.destroy()
    
def write_to_logfile(uid, logTime):
    
    with open(pathofCSV, 'a', newline='') as csvfile:
        timewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        timewriter.writerow([uid,logTime ])

def confirm_write(logTime):
    
    with open(pathofCSV, 'r', newline='') as csvfile:

        csvD =[]
        timereader = csv.reader(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in timereader:
            csvD.append(str(row))

        poo = csvD[-1].split(",")
        poo = poo[1].split("'")
        print(poo[1])    
            
tempMessage=0



while True:
    

    
    for reader in itertools.islice(readers(),0,1):  #only the PICC reader

        try:
            connection = reader.createConnection()
            connection.connect()
            
            #Get card UID
            SELECT = [0xFF, 0xCA, 0x00, 0x00, 0x00]
            response, sw1, sw2 = connection.transmit(SELECT)
            uid = toHexString(response)

            if len(uid) >1:   #do nothing if reader USB cable not plugged in

                #delay to reduce polling
                if Pcard == "ready":
                    logTime = datetime.now()
                    print(f"Card UID : {uid} --> Time:" + str(logTime))
                    Pcard = "not ready"
                    sleepTime =0
                    
                    logTime = datetime.now()
                    write_to_logfile(uid, logTime)

                    #TODO confirm write success
                    
                    #Alert user of successful UID write
                    win = Tk()
                    win.geometry("550x250")
                    win.title("RFID Tag")
                    tapMess = "UID : " + str(uid) +"\n" + "The patient time has been logged"
                                    
                    image = im = Image.open("C:\pilot\correct-sml.png")
                    tk_image = ImageTk.PhotoImage(image)

                    
                    Label(win, text= tapMess, font=('Helvetica 18 bold') ).place(x=130,y=40)
                    Label(win, image=tk_image, compound='center' ).place(x=200,y=100)


                    win.after(3000, destroy_window)
                    win.mainloop()
                    
                    
                   
                
                if sleepTime>1 and Pcard != "ready":
                    sleepTime =0
                    Pcard = "ready"
                    sleep(.1)
                    
                    
                sleepTime =sleepTime+1
    
        except NoCardException:
            if tempMessage > 20:
                logTime2 = datetime.now()
                print(reader, ' no card inserted, Time : ' +str(logTime2))
                tempMessage=0

            sleep(0.2)
            tempMessage=tempMessage+1
        
        except :
            print(reader, ' Pleas Try again, Time:' +str(logTime2))
            sleep(0.5)




'''if 'win32' == sys.platform:
    print('press Enter to continue')
    sys.stdin.read(1)'''
