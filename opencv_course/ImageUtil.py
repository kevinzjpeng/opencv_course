import cv2
import matplotlib.pyplot as plt

def imshow(images, columns=1, rows=1, figsize=(10, 10), cvtColor=cv2.COLOR_BGR2RGB):
    for image in images:
        fig=plt.figure(figsize=figsize)
    for i in range(1, columns*rows +1):
        fig.add_subplot(rows, columns, i)
        if cvtColor is not None:
            plt.imshow(cv2.cvtColor(images[i-1], cvtColor))
        else:
            plt.imshow(images[i-1])
    plt.show()