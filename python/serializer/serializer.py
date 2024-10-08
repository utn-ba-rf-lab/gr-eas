#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2022 gr-serializer author.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy as np
import serial
from gnuradio import gr

BOARD= {"UTNv1":"Mercurial 8kHz","UTNv2":"Mercurial X kHz"}

class serializer(gr.sync_block):
    """
    docstring for block serializer
    """
    def __init__(self,device_path,board_feature,mode,samp_rate):
        gr.sync_block.__init__(self,
            name="serializer",
            in_sig=[np.float32],
            out_sig=None)

        self.tty = serial.Serial(device_path,timeout=10)
        self.mode=mode
        self.samp_rate=samp_rate
        print("[INFO] | Path: %s" %device_path);
        print("[INFO] | Mode: %s" %self.mode);
        print("[INFO] | Sample rate: %d" %self.samp_rate);

        if(board_feature):

            #Send keyword to detect which board is connected
            board_detect=bytes("UTN",'utf-8')
            self.tty.write(board_detect)
           
            print("[RX] | Detecting board..")

            try:
                board_data=self.tty.readline()
                encoding = 'utf-8'
                board_data=board_data.decode(encoding)
                print("[DEBUG] | RX: %s" %board_data)

                if(board_data == "UTNv1\n"):
                    print("[INFO] | Board detected:", BOARD["UTNv1"])
                
                elif(board_data == "UTNv2\n"):
                    print("[INFO] | Board detected:", BOARD["UTNv2"])
                    board_sample_rate = np.uint16(self.samp_rate)
                    self.tty.write(board_sample_rate.tobytes())

                    board_sample_rate_ack = self.tty.readline()
                    board_sample_rate_ack = board_sample_rate_ack.decode(encoding)
                    

                    if(board_sample_rate_ack == "OK\n"):
                        
                      print("[DEBUG] | RX: %s Hz sample rate confirmed" %board_sample_rate)
                       

                    elif(board_sample_rate_ack == "ERROR\n"):
                        
                      print("[ERROR] | RX: %s" %board_sample_rate_ack)
                      exit() 

                    else:

                      print("[ERROR] | Not a valid sample rate")
                      exit() 

                else:
                    print("[ERROR] | Not a valid board detected")
                    exit() 

            except:
                print("[ERROR] | No board detected")
                exit()


    def work(self, input_items, output_items):
        in0 = input_items[0]
        
        if(self.mode == "data"):
            saturated = np.abs(in0) > 1
            output = np.zeros_like(in0, dtype=np.uint16)

            # Saturated values
            output[saturated] = np.sign(in0[saturated]) * 32767 + 32768
            # Non-saturated values
            output[~saturated] = (in0[~saturated] * 32767 + 32768).astype(np.uint16)
            self.tty.write(output.tobytes())          
           
        
        elif (self.mode == "detector"):
            #num_recv = np.uint8(in0*127-128)
            num_recv=in0
            for x in range(len(num_recv)):
            
                b = np.uint8(0) 
             
                if(np.sign(num_recv[x]) == 1 or num_recv[x]==0):
                    b = np.uint8(ord("H"))
                elif(np.sign(num_recv[x]) == -1):
                    b = np.uint8(ord("L"))
   
                self.tty.write(b.tobytes())
        
       # elif (self.mode == "receiver"):
       #     data_mercurial=self.tty.read()
       #     print("[RX] | Data received: %s" %data_mercurial);
       #     num_recv=int.from_bytes(data_mercurial, byteorder='big', signed=True) 

       #     if(np.sign(num_recv) == 1):
       #         b = np.uint8(ord("H"))
       #         print("[TX] | Data send: %d" %b);
       #     elif(np.sign(num_recv) == -1):
       #         b = np.uint8(ord("L"))
       #         print("[TX] | Data send: %d" %b);
        else:
            print("Error")

        return len(input_items[0])
