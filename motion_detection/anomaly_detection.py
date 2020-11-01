import cv2 # импорт модуля cv2
import datetime

#cv2.VideoCapture("видеофайл.mp4"); вывод кадров из видео файла
cap = cv2.VideoCapture(0); # видео поток с веб камеры

#cap.set(3,1280) # установка размера окна
#cap.set(4,700)

th = 100

ret, frame1 = cap.read()
ret, frame2 = cap.read()

while cap.isOpened(): # метод isOpened() выводит статус видеопотока
 
    diff = cv2.absdiff(frame1, frame2) # нахождение разницы двух кадров, которая проявляется лишь при изменении одного из них, т.е. с этого момента наша программа реагирует на любое движение.
  
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY) # перевод кадров в черно-белую градацию
 
    blur = cv2.GaussianBlur(gray, (5, 5), 0) # фильтрация лишних контуров
 
    _, thresh = cv2.threshold(blur, th, 255, cv2.THRESH_BINARY) # метод для выделения кромки объекта белым цветом
   
    dilated = cv2.dilate(thresh, None, iterations = 3) # данный метод противоположен методу erosion(), т.е. эрозии объекта, и расширяет выделенную на предыдущем этапе область
 
 
    _, сontours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # нахождение массива контурных точек
   
    for contour in сontours:
        (x, y, w, h) = cv2.boundingRect(contour) # преобразование массива из предыдущего этапа в кортеж из четырех координат

        # метод contourArea() по заданным contour точкам, здесь кортежу, вычисляет площадь зафиксированного объекта в каждый момент времени, это можно проверить
        #print(cv2.contourArea(contour))

        if cv2.contourArea(contour) < 700: # условие при котором площадь выделенного объекта меньше 700 px
            continue
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2) # получение прямоугольника из точек кортежа
        cv2.putText(frame1, "Status: {}".format("Motion detected"), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA) # вставляем текст
   
    #cv2.drawContours(frame1, сontours, -1, (0, 255, 0), 2) #также можно было просто нарисовать контур объекта

    cv2.imshow("frame1", frame1)
    cv2.imshow("blur", blur)
    cv2.imshow("thresh", thresh)
    cv2.imshow("dilated", dilated)
    frame1 = frame2  #
    ret, frame2 = cap.read() #  
 
    if cv2.waitKey(40) == 27:
        break
 
 
 

cap.release()
cv2.destroyAllWindows()