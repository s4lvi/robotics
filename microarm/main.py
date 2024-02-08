import ikpy.chain
import ikpy.utils.plot as plot_utils

import numpy as np
import time
import math

import serial


import asyncio


my_chain = ikpy.chain.Chain.from_urdf_file("arm_urdf.urdf",active_links_mask=[False, True, True, True, True, True, True])

ser = serial.Serial('COM3',9600, timeout=1)

def sendCommand(a,b,c,d,e,f,move_time):
    command = '0{:.2f} 1{:.2f} 2{:.2f} 3{:.2f} 4{:.2f} 5{:.2f} t{:.2f}\n'.format(math.degrees(a),math.degrees(b),math.degrees(c),math.degrees(d),math.degrees(e),math.degrees(f),move_time)
    ser.write(command.encode('ASCII'))

def doIK():
    global ik
    old_position= ik.copy()
    ik = my_chain.inverse_kinematics(target_position, target_orientation, orientation_mode="Z", initial_position=old_position)

    
def move(x,y,z):
    global target_position
    target_position = [x,y,z]
    doIK()

    sendCommand(ik[1].item(),ik[2].item(),ik[3].item(),ik[4].item(),ik[5].item(),ik[6].item(),1)

async def main():
    x=0
    y=0.25
    z=0.1
    while con.buttons[9].value<1:
        xp=con.axes[0].value
        yp=con.axes[1].value
        zp=con.axes[2].value
        if(abs(xp)>0.1 or abs(yp)>0.1 or abs(zp)>0.1):
            x=x+xp/100
            y=y-yp/100
            z=z-zp/100
            move(x,y,z)
        await asyncio.sleep(0.05)


loop = asyncio.get_event_loop()
loop.create_task(main())

ser.close() 