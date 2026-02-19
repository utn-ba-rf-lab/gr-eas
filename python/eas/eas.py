#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2022 gr-eas author.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy as np
import serial
from gnuradio import gr

BOARD= {"UTNv1":"Mercurial 8kHz","UTNv2":"Mercurial X kHz","UTNv3":"Mercurial X kHz / X Vref"}

class eas(gr.sync_block):
    """
    docstring for block eas
    """
    def __init__(self,device_path,input_type,board_feature,mode,samp_rate,vref):
        if input_type == float:
            gr.sync_block.__init__(self,
                name="eas",
                in_sig=[np.float32],
                out_sig=None)

            self.input_type = 2
        elif input_type == complex:  
            gr.sync_block.__init__(self,
            name="eas",
            in_sig=[np.complex64],
            out_sig=None)

            self.input_type = 4
        else:
            raise ValueError(f"Unsupported input_type: {input_type}")

        self.tty = serial.Serial(device_path,timeout=10)
        self.mode=mode
        self.samp_rate=samp_rate
        self.board_vref= vref

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
                elif(board_data == "UTNv3\n"):
                    print("[INFO] | Board detected:", BOARD["UTNv3"])
                    board_sample_rate = np.uint16(self.samp_rate)
                    board_data_type = np.uint8(self.input_type )
                    board_vref=np.uint16(self.board_vref/ 4.096* 65535)

                    board_setup_bytes= board_sample_rate.tobytes() + board_data_type.tobytes()+ board_vref.tobytes()
                    print(board_setup_bytes)
                    self.tty.write(board_setup_bytes)                                       
                    board_setup_ack = self.tty.readline()
                    board_setup_ack = board_setup_ack.decode(encoding)
                    print(board_setup_ack)

                    if(board_setup_ack == "OK\n"):
                        
                      print("[DEBUG] | RX: %s Hz sample rate and %sV ref confirmed" %(board_sample_rate, self.board_vref))
                       

                    elif(board_setup_ack == "ERROR\n"):
                        
                      print("[ERROR] | RX: %s" %board_setup_ack)
                      exit() 

                    else:

                      print("[ERROR] | Not valid board setup")
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
            # Input is float
            if (self.input_type == 2):

                saturated = np.abs(in0) > 1
                output = np.zeros_like(in0, dtype=np.uint16)

                # Saturated values
                output[saturated] = np.sign(in0[saturated]) * 32767 + 32768
                # Non-saturated values
                output[~saturated] = (in0[~saturated] * 32767 + 32768).astype(np.uint16)

            # Input is complex
            if (self.input_type == 4):
                real_part = np.real(in0)
                imag_part = np.imag(in0)


                real_clipped = np.clip(real_part, -1.0, 1.0)
                imag_clipped = np.clip(imag_part, -1.0, 1.0)

                real_uint16 = ((real_clipped * 32767) + 32768).astype(np.uint16)
                imag_uint16 = ((imag_clipped * 32767) + 32768).astype(np.uint16)

                # Interleave real and imag as [real0, imag0, real1, imag1, ...]
                interleaved = np.empty(real_uint16.size * 2, dtype=np.uint16)
                interleaved[0::2] = real_uint16
                interleaved[1::2] = imag_uint16

                output = interleaved

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
