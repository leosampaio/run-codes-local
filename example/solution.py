import imageio
import numpy as np

def main():
    
    filename = input().rstrip()
    coordinates  = (int(input().rstrip()), int(input().rstrip()))

    # step 1: load the image
    img = imageio.imread(filename)

    # step 2: get the pixel value
    pixel = img[coordinates]

    print(f"{pixel[0]} {pixel[1]} {pixel[2]}")

if __name__ == '__main__':
    main()
