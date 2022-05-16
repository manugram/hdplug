#!/usr/bin/python3


################################################################
# Hard Drive Hot Plug & Unplug Tool....
################################################################
# Written by: Manuel Soto.
#
# This comes from:       
#     "echo 1 > /sys/block/sda/device/delete" shell command
# as shown in:
#     http://www.sakana.fr/blog/2009/05/04/linux-sata-hot-plug-unplug/
#  
################################################################

import sys
import subprocess as sp
import getopt as g
import time


TOOL_NAME = 'hdplug'

TOOL_MAJOR_VERSION = '0'
TOOL_MINOR_VERSION = '1'
TOOL_PATCH_LEVEL   = '0'

TOOL_VERSION = f"{TOOL_MAJOR_VERSION}.{TOOL_MINOR_VERSION}.{TOOL_PATCH_LEVEL}"
                              


def plug_drive(channel: str) -> None:
    
    
    scan_str     = '- - -'
    sata_channel = channel 
    param_path   = f'/sys/class/scsi_host/{sata_channel}/scan'
    shell_cmd    = f'fdisk -l | grep sd'
    
    try:
        with open(param_path, 'w') as f:
            print('Scanning for drive...')
            f.write(scan_str)
    except Exception as err:
        print('->',e)
        sys.exit(2)
        
    time.sleep(1)    
    p = sp.run(shell_cmd, capture_output=True, text=True, shell=True)
    print(p.stdout)
    
    return
        

def unplug_drive(device: str) -> None:
    
           
    param_one    = '1'
    drive        = device
    param_path  = f'/sys/block/{drive}/device/delete'
    #param_path   = f'/home/manuel/Documents/SRC/Python/{drive}/arch'

    try:        
        with open(param_path, 'w') as f:
            print('Drive shutting down.')
            f.write(param_one)
    except Exception as e:
        print('->',e)
        sys.exit(2)
    
    # Wait for a second, hopefully enougth to poweroff the drive...
    time.sleep(1)
    print('Done.\nVerify and unplug...')    
    
    return
        

def show_version() -> None:
    
    
    print(f'{TOOL_NAME}: v{TOOL_VERSION}')
    
    return
    

def help_usage() -> None:   
    
     
    show_version()
    
    text = f"""
    Usage: {TOOL_NAME} [OPTIONS] [DRIVE or DRIVE_CHANNEL]
    Where:
        -p, --plug      Plugin drive. (i.e. host0 to scan sata port 1 
                        to detect the conected drive.)
        -u, --unplug    Unplug drive. (i.e. sda or sdb or any sata drive.)
        -V, --version   Tool version info.
        -h, --help      This help.
        
    Remember unmount all file systems of the drive before use this tool.   
    
    """
    
    print(text)
    
    return


def main() -> None:
    
    
    arguments = sys.argv[1:]    
    short_opts= 'p:u:Vh'
    long_opts = ['plug=', 'unplug=', 'version', 'help']
    
    try:
        opts, rem = g.getopt(arguments, short_opts, long_opts)
    except g.GetoptError as err:
        print('Bad options.', err)        
        help_usage()
        sys.exit(2)

    if opts != []:
        for o, a in opts:
            if o in ('-h', '--help'):
                help_usage()
            elif o in ('-V', '--version'):
                show_version()
            elif o in ('-p', '--plug'):
                plug_drive(a)
            elif o in ('-u', '--unplug'):
                unplug_drive(a)
    else:          
        help_usage()
        sys.exit(3)

    return        
            


if __name__ == '__main__':
    main()
