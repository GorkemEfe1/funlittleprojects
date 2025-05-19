import cv2
cap =  cv2.VideoCapture('C:\\Users\\revas\\Source\\Repos\\funlittleprojects\\badapple\\BadAppleOriginal.mp4')
length = cap.get(cv2.CAP_PROP_FRAME_COUNT)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
fps = cap.get(cv2.CAP_PROP_FPS)

ret, img = cap.read()
print(f'Returned {ret} and img of shape {img.shape}')
print(f'FPS : {fps:0.2f}')
print(f'Height {height}, Width {width}')
print(length)
cap.release()