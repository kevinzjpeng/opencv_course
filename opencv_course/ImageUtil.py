import cv2
import matplotlib.pyplot as plt

def imshow(images, columns=1, rows=1, figsize=(10, 10)):
    for image in images:
        fig=plt.figure(figsize=figsize)
    for i in range(1, columns*rows +1):
        fig.add_subplot(rows, columns, i)
        img = cv2.cvtColor(images[i-1], cv2.COLOR_BGR2RGB)
        plt.imshow(img)
    plt.show()