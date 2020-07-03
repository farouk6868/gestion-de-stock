# -*- coding: utf-8 -*-
"""
Created on Fri May 29 10:06:16 2020
@author: Senisna Brahim Djamel
"""
#..............
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication

import sys, os

from os import path
from PyQt5.uic import loadUiType

FORM_CLASS,_=loadUiType(path.join(path.dirname('__file__'),"main.ui"))

import sqlite3

x=0
idx=2

class Main(QMainWindow, FORM_CLASS):
    def __init__(self,parent=None):
        super(Main,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handel_Buttons()
        self.NAVIGATE()
        
        
    def Handel_Buttons(self):
        self.refresh_btn.clicked.connect(self.GET_DATA)
        self.search_btn.clicked.connect(self.SEARCH)
        self.check_btn.clicked.connect(self.LEVEL)
        self.update_btn.clicked.connect(self.UPDATE)
        self.delete_btn.clicked.connect(self.DELETE)
        self.add_btn.clicked.connect(self.ADD)
        self.next_btn.clicked.connect(self.NEXT)
        self.previous_btn.clicked.connect(self.PREVIOUS)
        self.last_btn.clicked.connect(self.LAST)
        self.first_btn.clicked.connect(self.FIRST)
        
    def GET_DATA(self):
        
        db=sqlite3.connect("stock.db")
        cursor=db.cursor()
        
        command=''' SELECT * FROM stock_table'''
        result=cursor.execute(command)
        
        self.table.setRowCount(0)
        
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number,column_number,QTableWidgetItem(str(data)))
                
    # Afficher le nombre de designation dans statistics Tab
    
        cursor2=db.cursor()
        cursor3=db.cursor()
        
        designation_nbr=''' SELECT COUNT (DISTINCT Designation ) FROM stock_table'''
        
        result_designation_nbr=cursor2.execute(designation_nbr)
        
        self.lbl_designation_nbr.setText(str(result_designation_nbr.fetchone()[0]))
        
        self.FIRST()
        self.NAVIGATE()
        
                
    def SEARCH(self):
        db=sqlite3.connect("stock.db")
        cursor=db.cursor()
        
        nbr=int(self.stock_filter_txt.text())
        command=''' SELECT * FROM stock_table WHERE Stock <=? '''
        result=cursor.execute(command, [nbr])
        
        self.table.setRowCount(0)
        
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number,column_number,QTableWidgetItem(str(data)))
                
    def LEVEL(self):
        db=sqlite3.connect("stock.db")
        cursor=db.cursor()
                
        command=''' SELECT Stock, Designation, Code FROM stock_table order by Stock asc LIMIT 6 '''
        result=cursor.execute(command)
        
        self.table2.setRowCount(0)
        
        for row_number, row_data in enumerate(result):
            self.table2.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table2.setItem(row_number,column_number,QTableWidgetItem(str(data)))
                
    def NAVIGATE(self):

        db=sqlite3.connect("stock.db")
        cursor=db.cursor()
        
        command=''' SELECT * from  stock_table'''
        
        result=cursor.execute(command)
        val=result.fetchone()
        
        self.id.setText(str(val[0]))
        self.code.setText(str(val[1]))
        self.designation.setText(str(val[2]))
        self.fournisseur.setText(str(val[3]))
        self.beneficiare.setText(str(val[4]))
        self.stock.setValue(val[5])
            
    def NEXT(self):
        db=sqlite3.connect("stock.db")
        cursor=db.cursor()
        command=''' SELECT * from stock_table '''
        result=cursor.execute(command)
        val=result.fetchall()
        tot=len(val)
        global x
        global idx
        x=x+1
        if x<tot:
           idx=val[x][0]
           self.NAVIGATE()
        else:
            x=tot-1
            print("END OF FILE")
            
    def PREVIOUS(self):
        db=sqlite3.connect("stock.db")
        cursor=db.cursor()
        command=''' SELECT * from stock_table '''
        result=cursor.execute(command)
        val=result.fetchall()
        global x
        global idx
        x=x-1
        if x>-1:
           idx=val[x][0]
           self.NAVIGATE()
        else:
            x=0
            print("Begin of file")
                
    def LAST(self):
        db=sqlite3.connect("stock.db")
        cursor=db.cursor()
        command=''' SELECT * from stock_table '''
        result=cursor.execute(command)
        val=result.fetchall()
        tot=len(val)
        global x
        global idx
        x=tot-1
        if x<tot:
           idx=val[x][0]
           self.NAVIGATE()
        else:
            x=tot-1
            print("End of file")
        
    def FIRST(self):
        db=sqlite3.connect("stock.db")
        cursor=db.cursor()
        command=''' SELECT * from stock_table '''
        result=cursor.execute(command)
        val=result.fetchall()
        global x
        global idx
        x=0
        if x>-1:
           idx=val[x][0]
           self.NAVIGATE()
        else:
            x=0
            print("Begin of file")
   
    def UPDATE(self):
       
       db=sqlite3.connect("stock.db")
       cursor=db.cursor()
        
       id_=int(self.id.text())
       code_=self.code.text()
       designation_=self.designation.text()
       fournisseur_=self.fournisseur.text()
       beneficiaire_=self.beneficiaire.text()
       stock_=str(self.stock.value())
        
       row = (code_,designation_,fournisseur_,beneficiaire_,stock_,id_)
        
       command=''' UPDATE stock_table SET Code=?,Designation=?,Fournisseur=?,Beneficiare=?,Stock=? WHERE ID=? '''
       
       cursor.execute(command, row)
       db.commit()
    
    def DELETE(self):
        db=sqlite3.connect("stock.db")
        cursor=db.cursor()
        
        d=self.id.text()
        
        command=''' DELETE FROM stock_table WHERE ID=? '''
        
        cursor.execute(command,d)
        db.commit()
        
    def ADD(self):
        db=sqlite3.connect("stock.db")
        cursor=db.cursor()
        
        code_=self.code.text()
        designation_=self.designation.text()
        fournisseur_=self.fournisseur.text()
        beneficiaire_=self.beneficiaire.text()
        stock_=str(self.stock.value())
        
        row = (code_,designation_,fournisseur_,beneficiaire_, stock_)
        
        command=''' INSERT INTO stock_table (Code,Designation,Fournisseur,Beneficiare,Stock) VALUES(?,?,?,?,?,?,?,?)  '''
       
        cursor.execute(command, row)
        
        db.commit()
   
   
   
   
   
def main():
    
    app=QApplication(sys.argv)
    window=Main()
    window.show()
    app.exec_()
    


if __name__=="__main__":
    main()
    
      
    