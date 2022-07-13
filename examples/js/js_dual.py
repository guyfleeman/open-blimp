import matplotlib.pyplot as plt
import numpy as np
import signal

from pyBlimp.blimp import BlimpManager
from pyBlimp.utils import *
from utils.js_utils import JoyStick_helper


# setup exit on ctrl-c
running = True
def exit_handle(signum, frame):
    global running
    running = False
    
signal.signal(signal.SIGINT, exit_handle)

# load desired configs
cfg_paths = ["configs/config1.yaml", "configs/config2.yaml"]
cfg = read_config(cfg_paths)

# build the blimp manager
b = BlimpManager(cfg, "/dev/ttyUSB0")

# setup the joystick reader
js = JoyStick_helper()

# show the FPV
#fig, axes = plt.subplots(1,2,figsize=(11,5))

# desired states to track
des1 = np.zeros(4)
des2 = np.zeros(4)

while running:
    # handle the joystick
    ax, on1, on2 = js.get_state()

    # decide inputs    
    if on1:
        des1[0] = -0.05*ax[0]
        des1[1] =  0.05*ax[1]
        des1[2] = wrap(des1[2]+0.05*ax[2])
        des1[3] = np.clip(des1[3]-0.05*ax[3], 0.0, 2.5)
        b.set_des(des1, 0)

    elif on2:
        des2[0] = -0.05*ax[0]
        des2[1] =  0.05*ax[1]
        des2[2] = wrap(des2[2]+0.05*ax[2])
        des2[3] = np.clip(des2[3]-0.05*ax[3], 0.0, 2.5)
        b.set_des(des2, 1)

    """
    # show the video feeds
    I1 = b1.get_image()
    I2 = b2.get_image()
    
    axes[0].clear()
    axes[0].imshow(I1)
    axes[0].set_xticks([])
    axes[0].set_yticks([])
    axes[0].set_title("FPV - Blimp 1")
    
    axes[1].clear()
    axes[1].imshow(I2)
    axes[1].set_xticks([])
    axes[1].set_yticks([])
    axes[1].set_title("FPV - Blimp 2")

    plt.draw(); plt.pause(0.0001)

    # break if the figure is closed
    if not plt.fignum_exists(fig.number): running = False
    """

b.shutdown()
