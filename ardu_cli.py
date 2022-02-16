# -*- coding: utf-8 -*-
"""
Created on Tue Feb 15 13:06:57 2022

@author: gweiss01
"""
import pyfirmata, time, sys

def run(number_of_trains, inter_train_interval, train_dur, freq_list, pulse_ratio, port):
    
    try:
        board = pyfirmata.Arduino(port)
        it = pyfirmata.util.Iterator(board)
        it.start()
        out = board.get_pin('d:11:p')
        for i in range(number_of_trains):
            for freq in freq_list:
                time.sleep(inter_train_interval)
                period=(1/freq) #estimated time to cycle the laser
                pulse_dur=(pulse_ratio*period)
                trough_dur=((1-pulse_ratio)*period)
                print(pulse_dur,trough_dur, train_dur)
                tic=time.time()
                for i in range(int(freq*train_dur)):
                    out.write(1)
                    target_time = time.perf_counter() + pulse_dur
                    while time.perf_counter() < target_time:
                        pass
                    out.write(0)
                    target_time = time.perf_counter() + trough_dur
                    while time.perf_counter() < target_time:
                        pass
                print(time.time()-tic)
    finally:
        board.exit()
        
if __name__ == '__main__': 
    args = sys.argv
    number_of_trains=int(args[1])
    inter_train_interval=float(args[2])
    train_dur=float(args[3])
    freq_list=[int(i) for i in args[4].split(",")]
    pulse_ratio=float(args[5])/100
    port=args[6]
    run(number_of_trains, inter_train_interval, train_dur, freq_list, pulse_ratio, port)