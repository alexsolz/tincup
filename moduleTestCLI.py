# This program is for testing if the pi is capable of receiving information and outputing necessary signals based on correctness of input codes.
# This program is intended for CLI keyboard input tests.

from RPi import GPIO
from RPLCD.gpio import CharLCD
import confirmCode
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
# Specify channels for each GPIO.
pir = 36
redLED = 18
blueLED = 22
yellowLED = 8
buzzer = 32
r1 = 7
r2 = 11
r3 = 13
r4 = 15
c1 = 10
c2 = 12
c3 = 38
c4 = 40

# PIR 
GPIO.setup(pir, GPIO.IN)
# Red LED
GPIO.setup(redLED, GPIO.OUT)
# Green LED
GPIO.setup(blueLED, GPIO.OUT)
# Yellow LED
GPIO.setup(yellowLED, GPIO.OUT)
# Buzzer
GPIO.setup(buzzer, GPIO.OUT)
# LCD console
lcd = CharLCD(cols = 16, rows = 2, pin_rs = 37, pin_e = 35, pins_data = [33, 31, 29, 23], numbering_mode = GPIO.BOARD)


# Initial error count value and target code value.
errorCount = 0
TARGET = ""

# Infinite loop: Implementing a while loop may be harmful as it may cause potential run-time errors in the long run.
# Going forward more care should be made on stability.
while errorCount != 3:
    pirStatus = GPIO.input(pir)
    TARGET = confirmCode.returnPassCode()
    GPIO.output(yellowLED, False)

    # This part is to ensure module works only when user(intruder) is close-by.
    while pirStatus == 1:
        print("<This notification is only for demonstration purposes.>")
        print("There is someone around.")
        GPIO.output(yellowLED, True)
        for i in range(2):
            GPIO.output(buzzer, GPIO.HIGH)
            time.sleep(0.1)
            GPIO.output(buzzer, GPIO.LOW)
            time.sleep(0.1)

        # This message is intented for demonstration/testing purposes on the CLI.
        print("<This output is shown for proving the Pi can successfully communicate with the server and update passcodes.>")
        # Waiting on code to be fully updated.
        if (type(TARGET) != type("string")):
            print("Code generation needs more time to synchronize. Please wait for next prompt.")
            time.sleep(10)
        else:
            print("Current passcode: " + TARGET)

        lcd.write_string(u"Input PW\n")
        userInput = input("Type in info: ")

        # Termination option only for resetting system.
        if userInput == "q":
            GPIO.output(redLED, False)
            GPIO.output(blueLED, False)
            GPIO.cleanup()
            break

        # If the user inputs the correct code.
        if userInput == TARGET:
            GPIO.output(blueLED, True)
            lcd.clear()
            lcd.write_string("WELCOME!")

            for i in range(3):
                GPIO.output(buzzer, GPIO.HIGH)
                time.sleep(1)
                GPIO.output(buzzer, GPIO.LOW)
                time.sleep(1)
            GPIO.output(buzzer, False)

            time.sleep(10)
            lcd.clear()
            GPIO.output(blueLED, False)
            errorCount = 0
            lcd.clear()

        else:
            lcd.clear()
            lcd.write_string("INCORRECT!")
            GPIO.output(redLED, GPIO.HIGH)
            GPIO.output(buzzer, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(redLED, GPIO.LOW)
            GPIO.output(buzzer, GPIO.LOW)
            errorCount += 1
            lcd.clear()

        # If the user makes three consecutive mistakes, the system will create a beeping sound and the red LED will blink.
        if errorCount == 3:
            lcd.clear()
            GPIO.output(blueLED, False)
            lcd.write_string("INTRUDER ALERT!")
            for i in range(30):
                GPIO.output(redLED, GPIO.HIGH)
                GPIO.output(buzzer, GPIO.HIGH)
                time.sleep(0.1)
                GPIO.output(redLED, GPIO.LOW)
                GPIO.output(buzzer, GPIO.LOW)
                time.sleep(0.1)
            GPIO.output(redLED, False)
            GPIO.output(blueLED, False)
            GPIO.output(buzzer, False)
            lcd.clear()
            errorCount = 0
            break
