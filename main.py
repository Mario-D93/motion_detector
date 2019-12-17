import cv2

initial_frame=None

#INPUT: index of the camera or path
record=cv2.VideoCapture(0)

while True:

	control,frame=record.read()
	#read() method returns boolean & numpy array

	gray_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	gray_frame=cv2.GaussianBlur(gray_frame,(19,19),0)

	if initial_frame is None:
		initial_frame = gray_frame
		continue

	#To compare/find differences between the first frame and then others
	distinction=cv2.absdiff(initial_frame,gray_frame)

	threshold=cv2.threshold(distinction,50,255, cv2.THRESH_BINARY)[1]

	#(cnts,_) = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	contours, hierarchy = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	for cnt in contours:
		if cv2.contourArea(cnt) < 1500:
			continue

		(x,y,w,h)=cv2.boundingRect(cnt)

		#rectangle method will drow a rectangle in a current frame if a moving object appears in front of the camera
		cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), 5)


	#cv2.imshow('Record',gray_frame)
	#cv2.imshow('Threshold frame',threshold)
	cv2.imshow('Rectangle frame',frame)

	key=cv2.waitKey(1)
	if key == ord('q'):
		break

record.release()
cv2.destroyAllWindows