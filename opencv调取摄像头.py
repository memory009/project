import cv2

cap = cv2.VideoCapture(0)
while True:
	# ret是True或者false，frame是目标图片
    ret, frame = cap.read()
    # 这里是未处理的视频
    cv2.imshow('frame', frame)
	#灰度视频
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('gray', gray)
	#将视频左右对调
    #frame = cv2.flip(frame, 1)
    #cv2.imshow("video", frame)
    #按q退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

