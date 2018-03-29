import matplotlib.pyplot as plt
from PIL import Image

im = Image.open("autojump1.png")
plt.imshow(im, cmap=plt.get_cmap("gray"))
exit_this=False
while not exit_this:
    pos = plt.ginput(2)
    print(pos)
    center = pos[0]
    center_x,center_y = center[0],center[1]
    a = input("are you quit: ")
    if a!='':
        exit_this=True