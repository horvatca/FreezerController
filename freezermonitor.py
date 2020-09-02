#This just records and logs the termp measured at a termometer probe.

#import socket to be abel to find the hostname of the rpi
import socket
#import GPIO package
import RPi.GPIO as GPIO
#import time package
import time
#import date and time package for inserting date into logs
import datetime
#import glob package used for finding files and paths according to patterns and Unix rules
import glob
#import os package for executing shell commands amd other useful OS stuff.
import os
#import sys package for error handling sys.exit()
import sys

#everythign in the try block will attempt to be executed
#on failure OR completion, the finally: block will be executed
try:

	##########################
    # SETUP AND FUNCTIONS#
    ##########################


    #set GPIO mode and pins
    GPIO.setmode(GPIO.BOARD)
    #Set "status" LED pin number
    statusLEDpin = 7
    GPIO.setup(statusLEDpin, GPIO.OUT)


    #setup the output log file
    log = open("/home/pi/freezermonitorlog.txt", "a+")


    #Thermometer setup stuff
    #set ds1820 thermometer prefix
    ds1820_prefix = '28'
    #thermometer calibration - if a thermo reads consistenaly high or low, adjust it here by offseting the reading in degrees F. Does accept negative numbers
    thermAdjust = 0
    #base directory for thermometer readings
    devices_base_dir ='/sys/bus/w1/devices/'
    #find the output file for the thermometer
    therm_folder = glob.glob(devices_base_dir + ds1820_prefix + '*')[0]
    therm_file = therm_folder + '/w1_slave'
    #initiate
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')
    #End thermometer setup


    #functions to read the temp of the thermometer
    def read_temp_raw():
        with open(therm_file, 'r')as deviceFile:
            lines=deviceFile.readlines()
        return lines

    def degCtoF(tempC):
        return 9.0/5.0 * tempC + 32

    def read_temp():
        lines = read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            return float(temp_string) / 1000.0

    #functions to set LED states
    def statusLEDon():
        GPIO.output(statusLEDpin,True)
        
    def statusLEDoff():
        GPIO.output(statusLEDpin,False)


    #grab the CPU temp for monitoring because we will put the Raspberry Pi in an enclosure and it may overheat
    def getCPUtemperature():
        res = os.popen('vcgencmd measure_temp').readline()
        return(res.replace("temp=","").replace("'C\n",""))


	#############
    # MAIN #
    #############

	#status light on
    statusLEDon()
    
    #create timestamp
    today=datetime.datetime.now()
    timestamp = str(today.strftime('%Y, %m, %d, %H, %M, %S'))
    
    #get host
    host = str(socket.gethostname())
    
    #get CPU temp
    cpuTemp = getCPUtemperature()
                                           
    #get temp
    currentTemp = degCtoF(read_temp()) + thermAdjust
   
    #assemble the message to log
    message = host + ', Temp: ' + str(currentTemp) + ', Timestamp: '+ timestamp + ', CPU Temp: ' + cpuTemp + '\n'
    
    print(message)
    log.write(message)
    
    #these line represent a sucessful completion of the main loop
    #after they are executed, the FINALLY will be executed.
    #really the only function is to pause long enough for the status LED to be visible

    #status light off after pause (for visible blink)
    time.sleep(.3)  
    statusLEDoff()




except KeyboardInterrupt:
    log.write('Program haulted by keyboard input. Aborting!')
    GPIO.cleanup() #this will turn the relay off
    sys.exit()
    
except:
    log.write('Unexpected error. Aborting.')
    GPIO.cleanup() #this will turnthe relay off
    sys.exit()


#finally is always executed even if there is an error in the try block
#put all the cleanup stuff here. This will always run.
finally:
    #close the log file
    log.close()
    #cleanup gpio settings which turns everythign off
    GPIO.cleanup()
    #show completion in terminal
    print('End')
    #exit python program
    sys.exit()