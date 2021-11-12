import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(40, GPIO.OUT) #servo setup
p = GPIO.PWM(40, 50)

GPIO.setup(8, GPIO.IN) # ir sensor 1 (Parking A)
GPIO.setup(10, GPIO.IN) # ir sensor 2 (Parking B)
GPIO.setup(11, GPIO.IN) # ir sensor 3 (Parking C)
GPIO.setup(12, GPIO.IN) # ir sensor 4 (for car detection)

p.start(5)


def detect_parking_sensor(pin):
    if GPIO.input(pin):
        return True
    else:
        return False


def get_free_slots():
    free_slots = ['A','B','C']
    if detect_parking_sensor(8):
        free_slots.append('A')
        free_slots = list(set(free_slots))
    else:
        free_slots.remove('A')
        
    if detect_parking_sensor(10):
        free_slots.append('B')
        free_slots = list(set(free_slots))
    else:
        free_slots.remove('B')
    
    if detect_parking_sensor(11):
        free_slots.append('C')
        free_slots = list(set(free_slots))
    else:
        free_slots.remove('C')
        
    free_slots = free_slots.sort()
    return free_slots



#Main Function
if __name__ == '__main__':
    try:
        while True:
            car_detect = GPIO.input(12)
            if car_detect != True:
                if len(get_free_slots()) != 0:  #checking if slot is available or not
                    print("Parking slot "+str(get_free_slots())+" is available.")
                    time.sleep(1.5)
                    p.ChangeDutyCycle(7.5)   #open gate
                    time.sleep(3)
                    p.ChangeDutyCycle(5)   # close gate after 3 seconds
                else:
                    print("Sorry!!! Parking slots are full.")
                
            else:
                print("Welcome to smart parking system")

    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        lcd.clear()
        lcd.message('Thank You!')
        GPIO.cleanup()




























