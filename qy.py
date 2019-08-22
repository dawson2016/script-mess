#!/usr/bin/env python
#coding:utf-8
import time
import win32gui
import win32ui
import win32api
import win32con

def nb():
	time.sleep(3)
	win32api.keybd_event(34,0,0,0)  
	win32api.keybd_event(34,0,win32con.KEYEVENTF_KEYUP,0)  
	time.sleep(0.5)
	win32api.keybd_event(34,0,0,0)  
	win32api.keybd_event(34,0,win32con.KEYEVENTF_KEYUP,0) 
	time.sleep(3)
	win32api.SetCursorPos((923, 515))
	time.sleep(0.5)
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
	time.sleep(3)
	win32api.keybd_event(33,0,0,0)  
	win32api.keybd_event(33,0,win32con.KEYEVENTF_KEYUP,0)  
	time.sleep(1)
	win32api.keybd_event(33,0,0,0)  
	win32api.keybd_event(33,0,win32con.KEYEVENTF_KEYUP,0) 
	time.sleep(2)
	win32api.SetCursorPos((299, 583)) 
	time.sleep(0.5)
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
	time.sleep(2)
	win32api.SetCursorPos((402, 456))
	time.sleep(0.5)
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

for i in range(140):
	nb()
