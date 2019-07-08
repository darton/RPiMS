#!/usr/bin/python

import LCD_1in44
import LCD_Config
import redis
import socket
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageColor

#try:
def main():
#       ******Init redis DB*******  
        hostname = socket.gethostname()
        hostip = socket.gethostbyname(hostname)
        
        redis_db = redis.StrictRedis(host="localhost", port=6379, db=0, charset="utf-8", decode_responses=True)
        temperature = round(float(redis_db.get('Temperature')),1)
        humidity = round(float(redis_db.get('Humidity')),1)
        door_sensor_1 = redis_db.get('door_sensor_1')
        door_sensor_2 = redis_db.get('door_sensor_2')
        door_sensor_3 = redis_db.get('door_sensor_3')

        LCD = LCD_1in44.LCD()

#       **********Init LCD**********
        Lcd_ScanDir = LCD_1in44.SCAN_DIR_DFT  #SCAN_DIR_DFT = D2U_L2R
        LCD.LCD_Init(Lcd_ScanDir)    

        image = Image.new("RGB", (LCD.width, LCD.height), "WHITE")
        draw = ImageDraw.Draw(image)
#       font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 22)
#       ******draw line*******
        draw.line([(0,0),(127,0)], fill = "BLUE",width = 5)
        draw.line([(127,0),(127,127)], fill = "BLUE",width = 5)
        draw.line([(127,127),(0,127)], fill = "BLUE",width = 5)
        draw.line([(0,127),(0,0)], fill = "BLUE",width = 5)
#       *****draw rectangle*****
        draw.rectangle([(5,10),(120,35)],fill = "BLACK")

#       ******draw text******
        draw.text((10, 10), 'RPiMS', fill = "WHITE")
        draw.text((10, 24), 'IP:' + str(hostip), fill='WHITE')
        draw.text((10, 48), 'Temperature.' + str(temperature) + 'C', fill = "RED")
        draw.text((10, 60), 'Humidity....' + str(humidity) + '%', fill = "BLUE")
        draw.text((10, 72), 'Door 1......' + str(door_sensor_1), fill = "BLACK")
        draw.text((10, 84), 'Door 2......' + str(door_sensor_2), fill = "BLACK")
        draw.text((10, 96), 'Door 3......' + str(door_sensor_3), fill = "BLACK")

#       LCD.LCD_ShowImage(image,0,0)
#       LCD_Config.Driver_Delay_ms(5000)

#       image = Image.open('sky.bmp')
        LCD.LCD_ShowImage(image,0,0)

#    while (True):

if __name__ == '__main__':
        main()

#except:
#       print("except")
