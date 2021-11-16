import Adafruit_CharLCD as LCD

def lcd():
    
    lcd_rs        = 25  # Note this might need to be changed to 21 for older revisi$
    lcd_en        = 24
    lcd_d4        = 23
    lcd_d5        = 17
    lcd_d6        = 18
    lcd_d7        = 22
    lcd_backlight = 4

    # Define LCD column and row size for 16x2 LCD.
    lcd_columns = 16
    lcd_rows    = 2

    # Alternatively specify a 20x4 LCD.
    # lcd_columns = 20
    # lcd_rows    = 4

    # Initialize the LCD using the pins above.
    
    lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                            lcd_columns, lcd_rows, lcd_backlight)

    return lcd