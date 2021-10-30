import math
import time

import cv2
import mediapipe as mp

import requests

cap = cv2.VideoCapture(0)

mpMallaFacial = mp.solutions.face_mesh
MallaFacial = mpMallaFacial.FaceMesh(max_num_faces=1)


mpDibujo = mp.solutions.drawing_utils
ConfDibu = mpDibujo.DrawingSpec(thickness=1, circle_radius=1)

#variables
parpadeo = False
conteo = 0
conteo_sueno = 0
inicio = 0
tiempo = 0
final = 0
muestra = 0

while True:
    #Lectura de camara
    ret, frame = cap.read()

    #Correccion de color
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    #Procesamiento de resultados
    resultados = MallaFacial.process(rgb)

    cx = []
    cy = []
    lista = []

    #Preguntos si hay resultados
    if resultados.multi_face_landmarks:
        for rostros in resultados.multi_face_landmarks:
            #mpDibujo.draw_landmarks(frame, rostros, mpMallaFacial.FACE_CONNECTIONS, ConfDibu, ConfDibu) #mascara

            #Extraigo los puntos
            for id, puntos in enumerate(rostros.landmark):
                #Ancho y alto
                al, an, c = frame.shape
                #Extraigo X e Y y las convierto
                x, y = int(puntos.x * an), int(puntos.y * al)

                #Almaceno las coordenadas
                cx.append(x)
                cy.append(y)
                lista.append([id,x,y])

                #Pregunto si la lista esta completa
                if len(lista) == 468:
                    #Ojo Izquierdo
                    x1, y1 = lista[386][1:]  #punto de arriba
                    x2, y2 = lista[374][1:]  #punto de abajo
                    #cv2.circle(frame, (x1, y1), 2, (255, 0, 0), cv2.FILLED)  #punto de arriba dibujo
                    #cv2.circle(frame, (x2, y2), 2, (255, 255, 0), cv2.FILLED) #punto de abajo dibujo
                    cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2) #dibujo de linea entre los puntos
                    distancia = math.hypot(x2 - x1, y2 - y1)

                    # Ojo Derecho
                    x3, y3 = lista[159][1:]  # punto de arriba
                    x4, y4 = lista[145][1:]  # punto de abajo
                    cv2.line(frame, (x3, y3), (x4, y4), (0, 255, 0), 2)
                    distancia2 = math.hypot(x4 - x3, y4 - y3)

                    #Mostrando el texto
                    cv2.putText(frame, f'Parpadeo: {int(conteo)}', (100, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                    cv2.putText(frame, f'Micro Sueno: {int(conteo_sueno)}', (100, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
                    cv2.putText(frame, f'Duracion: {int(muestra)}', (100, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

                    if distancia <= 10 and distancia2 <= 10 and parpadeo == False:
                        conteo = conteo + 1
                        inicio = time.time()
                        parpadeo = True
                    elif distancia > 10 and distancia2 > 10 and parpadeo == True:
                        parpadeo = False
                        final = time.time()

                    #Temporizador
                    tiempo = round(final - inicio, 0) #toma el tiempo actual del micro


                    #Contador de micro sueños
                    if tiempo >= 3:
                        conteo_sueno = conteo_sueno + 1


                        def telegram_bot_sendtext(bot_message):
                            bot_token = '1928556380:AAE8W2P5kUz5z68h0Cdw_jIlu165GjBLmfs'
                            bot_chatID = '-714755564'
                            send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

                            response = requests.get(send_text)

                            return response.json()


                        test = telegram_bot_sendtext("Ey despertate pa")
                        print(test)
                        muestra = tiempo  #muestra es para el micro sueño del momento
                        inicio = 0        #limpio las variables para q se tome un nuevo tiempo
                        final = 0





    #muestro resultados
    cv2.imshow("Malla Facial", frame)
    #espero la tecla de esc para cerrar la camara
    t = cv2.waitKey(1)

    #el 27 corresponde al esc
    if t == 27:
        break

#borro lo guardado en la camara
cap.release()
#destruyotodo lo generado
cv2.destroyAllWindows()