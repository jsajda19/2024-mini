#!/usr/bin/env python3
"""
PWM Tone Generator

based on https://www.coderdojotc.org/micropython/sound/04-play-scale/
"""

import machine
import utime

# GP16 is the speaker pin
SPEAKER_PIN = 16

# create a Pulse Width Modulation Object on this pin
speaker = machine.PWM(machine.Pin(SPEAKER_PIN))

#List of Notes
C4 = 261.63
D4 = 293.66
E4 = 329.63
F4 = 349.23
G4 = 392
A4 = 440
Bb4 = 466.16
C5 = 523.25
D5 = 587.33
freq = [C4,E4,F4,A4,C5,0,D5,D5,D5,C5,0,Bb4,Bb4,Bb4,A4,0,G4,G4,G4,F4,F4,F4,F4,F4,0,F4,F4,E4,F4,G4,A4,A4,A4,0]

#Note durations
quart = 0.6
eighth = quart/2
half = quart*2
dot = 0.75*quart
whole = 12*quart
duration = [eighth,eighth,dot,eighth,half,eighth,eighth,eighth,eighth,half,eighth,eighth,eighth,eighth,half,eighth,eighth,eighth,eighth,half,eighth,eighth,quart,eighth,eighth,half,quart,eighth,eighth,eighth,eighth,quart,whole,whole,whole,0]

def playtone(frequency: float, duration: float) -> None:
    speaker.duty_u16(65000)
    speaker.freq(int(frequency))
    utime.sleep(duration)


def quiet():
    speaker.duty_u16(0)


#freq: float = 30
#duration: float = 0.1  # seconds

print("Playing frequency (Hz):")

for i in range(32):
    if freq[i] == 0:
        quiet()
    else:
        print(freq[i])
        playtone(freq[i], duration[i])
        #freq = int(freq * 1.1)
    quiet()
    utime.sleep(.1)

# Turn off the PWM
quiet()
