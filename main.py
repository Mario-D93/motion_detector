import cv2,time,pandas
from datetime import datetime as dt
initial_frame=None

data_frame=pandas.DataFrame(columns=['Start','End'])


#INPUT: index of the camera or path
record=cv2.VideoCapture(0)
status_ls=[None,None]
times=[]
while True:

	status=0
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
		status=1

		(x,y,w,h)=cv2.boundingRect(cnt)
		#rectangle method will drow a rectangle in a current frame if a moving object appears in front of the camera
		cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), 5)
	status_ls.append(status)

	status_ls=status_ls[-5:]

	if status_ls[-1]==1 and status_ls[-2]==0:
		times.append(dt.now())
	if status_ls[-1]==0 and status_ls[-2]==1:
		times.append(dt.now())

	#cv2.imshow('Record',gray_frame)
	#cv2.imshow('Threshold frame',threshold)

	cv2.imshow('Rectangle frame',frame)
	key=cv2.waitKey(1)
	if key == ord('q'):
		if status==1:
			times.append(dt.now())
		break


for i in range(0,len(times),2):
	data_frame=data_frame.append({'Start':times[i],'End':times[i+1]},ignore_index=True)
data_frame.to_csv("recorded_time.txt")	

#print(data_frame)
record.release()
cv2.destroyAllWindows