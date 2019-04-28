import autopy
from autopy import screen
import time,win32api,win32gui,win32con
import sys
from PIL import ImageGrab
def action(name,xoffset=1,yoffset=1,staytime=1):
	a=autopy.bitmap.Bitmap.open('fuzhu/'+str(name)+'.png')
	sc=autopy.bitmap.capture_screen()
	pos = sc.find_bitmap(a,0.1)
	print pos
	#print x,y
	if pos==None:
		autopy.alert.alert('error')
		return 'error'
	x=pos[0]+xoffset
	y=pos[1]+yoffset		
	autopy.mouse.move(x,y)
	autopy.mouse.click()
	time.sleep(staytime)
win32api.keybd_event(115,0,0,0)
time.sleep(2)
myinput('hdpx.webtrn.cn/cms/')
win32api.keybd_event(13,0,0,0)
time.sleep(4)
action('dl',37,14)
time.sleep(2)

action('user',70,17)

myinput('用户名')
#action('password',116,12)
win32api.keybd_event(9,0,0,0)
myinput('密码')
#action('enter',120,15)
win32api.keybd_event(13,0,0,0)
time.sleep(3)
win32api.keybd_event(34,0,0,0)
time.sleep(3)
action('kcxx',71,14)
time.sleep(2)
action('jxxx',58,29)
time.sleep(2)
action('xxmb',50,10)
