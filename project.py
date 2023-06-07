import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
import json
import psutil

for proc in psutil.process_iter(): #수행되다만 흔적이 있다면 없애기
    if proc.name() == 'libgpiod_pulsein':
        proc.kill()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

MQTT_HOST = "broker.emqx.io"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 60

MQTT_PUB_TOPIC = "mobile/eastnux/message"

RED = 27
YELLOW = 22
GREEN = 23
BUTTON = 24
TRIG = 13
ECHO = 19

GPIO.setup(RED, GPIO.OUT)
GPIO.setup(YELLOW, GPIO.OUT)
GPIO.setup(GREEN, GPIO.OUT)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

client = mqtt.Client()

client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
client.loop_start()

try:
    while True:
        # 무한 루프 코드
        GPIO.output(GREEN, GPIO.HIGH)
        time.sleep(1)
        
        GPIO.output(TRIG, False)
        time.sleep(0.5)

        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        while GPIO.input(ECHO) == 0 :
            pulse_start = time.time()

        while GPIO.input(ECHO) == 1 :
            pulse_end = time.time()
        
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17000
        distance = round(distance, 2)
        
        while (GPIO.input(BUTTON)==True) and distance <= 30 :
            GPIO.output(GREEN, GPIO.LOW)
            GPIO.output(YELLOW, GPIO.HIGH)
            time.sleep(2)
            GPIO.output(YELLOW, GPIO.LOW)
            GPIO.output(RED, GPIO.HIGH)
                
    
            for i in range(5, 0, -1):
                client.publish(MQTT_PUB_TOPIC, i)
                print(i)
                time.sleep(1)
            GPIO.output(RED, GPIO.LOW)

except KeyboardInterrupt:
    print("사용자가 프로그램을 종료했습니다.")
finally: #종료 시 정리 코드
    GPIO.output(RED, GPIO.LOW)
    GPIO.output(YELLOW, GPIO.LOW)
    GPIO.output(GREEN, GPIO.LOW)
    GPIO.cleanup()

