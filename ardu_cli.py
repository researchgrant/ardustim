# -*- coding: utf-8 -*-
"""
Created on Tue Feb 15 13:06:57 2022

@author: gweiss01
"""
import pyfirmata, time, sys, math
import numpy as np


def run(train_list, inter_train_interval, port, wait, number_of_trains):
    # try:
    if 1:
        board = pyfirmata.Arduino(port)
        out = board.get_pin('d:11:p')
        TTL = board.get_pin('d:12:o')
        print("Running program: {} {} second trains with {} second inter-train intervals".format(number_of_trains,
                                                                                                 train_dur,
                                                                                                 inter_train_interval,
                                                                                                ))

        for i in range(number_of_trains):                                                    
            for train in train_list:
                print(len(train))
                time.sleep(inter_train_interval)
                tic=time.time()
                TTL.write(1)
                for y in train:
                    tic=time.perf_counter()
                    # print(y)
                    out.write(y)
                    while 1:
                        if time.perf_counter() - tic >= 1/time_resolution:
                            break
                TTL.write(0)
    
            time.sleep(wait)
    # finally:
        board.exit()
        return
        
if __name__ == '__main__': 
    args = sys.argv
    time_resolution=1000
    number_of_trains=int(args[1])
    shape=args[2]
    inter_train_interval=float(args[3])
    train_dur=float(args[4])
    freq_list=[int(i) for i in args[5].split(",")]
    pulse_ratio=float(args[6])/100
    port=args[7]
    wait=float(args[8])
    train_list=[]
    for freq in freq_list:
        times=np.arange(0,train_dur,1/time_resolution)
        sin_wave = np.sin(2*np.pi*times*freq) * (1 - ((40-freq)/100))
        sin_wave[sin_wave<0]=0
        if shape=="Sine Wave":
            train_list.append(sin_wave)
        if shape == "Square Pulse":
            cycle = [1]*math.ceil((time_resolution/freq)*pulse_ratio)
            cycle += [0]*math.floor((time_resolution/freq)*(1-pulse_ratio))
            cycle*= math.ceil(freq*(train_dur))
            cycle=cycle[:int(train_dur*time_resolution)]
            train_list.append(cycle)

        
    run(train_list, inter_train_interval, port, wait, number_of_trains)