import numpy as np
import os
import cv2
import face_recognition as fr
import csv
from datetime import datetime
import pyttsx3
import threading

path='Images'
os.listdir(path)
mylist=os.listdir(path)
imgs=[]
classnames=[]
for i in mylist:
    imgpath=os.path.join(path,i)
    curr_img=cv2.imread(imgpath)
    imgs.append(curr_img)
    classnames.append(i.split('.')[0])

def face_encodings(images):
    encodings=[]
    for img in images:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        face_locations=fr.face_locations(img)
        face_encodings=fr.face_encodings(img,face_locations)[0]
        encodings.append(face_encodings)
    return encodings

encodelist_knownfaces=face_encodings(imgs)
csv_file = 'attendance.csv'

with open(csv_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Name', 'Time'])
attendence_marked=set()

# Function to speak in a separate thread
def speak_name(name):
    txt_sp = pyttsx3.init()
    voices = txt_sp.getProperty('voices')
    txt_sp.setProperty('voice', voices[0].id)
    text = f"Attendance marked for {name}"
    txt_sp.say(text)
    txt_sp.runAndWait()

video=cv2.VideoCapture(0)
while True:
    suc,frame=video.read()
    frame1=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    face_in_frame=fr.face_locations(frame1)
    face_encode=fr.face_encodings(frame1,face_in_frame)
    
    for enc_face,loc_face in zip(face_encode,face_in_frame):
        matches=fr.compare_faces(encodelist_knownfaces,enc_face)
        face_dis=fr.face_distance(encodelist_knownfaces,enc_face)
        
        if len(face_dis)>0:
            match_index=np.argmin(face_dis)
            
            if matches[match_index]:
                name=classnames[match_index]
                
                if name not in attendence_marked:
                    attendence_marked.add(name)
                    
                    now = datetime.now().strftime('%H:%M:%S')
                    with open(csv_file, 'a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([name, now])
                    
                    print(f'Attendance marked for {name} at {now}')
                    
                    # Speak in a separate thread so it doesn't block
                    threading.Thread(target=speak_name, args=(name,), daemon=True).start()
                    
            else:
                name="Unknown Face"
                    
        else:
            name="Unknown Face"
        
        # Draw rectangle and name on frame
        y1,x2,y2,x1=loc_face
        cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
        cv2.putText(frame,name,(x1,y1-10),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,0,0),2)
        
    cv2.imshow('img',frame)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break

video.release()
cv2.destroyAllWindows()