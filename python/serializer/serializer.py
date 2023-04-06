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

class serializer(gr.sync_block):
    """
    docstring for block serializer
    """
    def __init__(self,device_path,board_feature,mode):
        gr.sync_block.__init__(self,
            name="serializer",
            in_sig=[np.float32],
            out_sig=None)
        self.tty = serial.Serial(device_path)
        self.mode=mode
        print("[INFO] | Path: %s" %device_path);
        print("[INFO] | Mode: %s" %self.mode);
        
        if(board_feature):
            board_detect=bytes("UTN",'utf-8')
            for byte in board_detect:
                self.tty.write(byte)
            
            board_data=self.tty.read()
            print("[RX] | Board detected: %s" %board_data);

    def work(self, input_items, output_items):
        in0 = input_items[0]
        
        if(self.mode == "data"):

            b = np.uint8(in0*127-128) 
            self.tty.write(b.tobytes())
        
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
        
        elif (self.mode == "receiver"):
            data_mercurial=self.tty.read()
            print("[RX] | Data received: %s" %data_mercurial);
            num_recv=int.from_bytes(data_mercurial, byteorder='big', signed=True) 

            if(np.sign(num_recv) == 1):
                b = np.uint8(ord("H"))
                print("[TX] | Data send: %d" %b);
            elif(np.sign(num_recv) == -1):
                b = np.uint8(ord("L"))
                print("[TX] | Data send: %d" %b);
        else:
            print("Error")

        return len(input_items[0])
