import imaplib
import email
import traceback
import os

# Credenciales del correo

login = "pruebaml102021@gmail.com"
password = "pru3ba7*"
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT = 993

#Definición de listas para almacenar fecha(lista1), remitente (lista2) y asunto (lista3).

lista1 = []
lista2 = []
lista3 = []


def clean(text):
    # Se limpia el texto  para crear una carpeta
    return "".join(c if c.isalnum() else "_" for c in text)


def read_email():
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(login, password)
        mail.select('inbox')

        data = mail.search(None, 'ALL')
        mail_ids = data[1]
        id_list = mail_ids[0].split()
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])

        for i in range(latest_email_id, first_email_id, -1):
            data = mail.fetch(str(i), '(RFC822)')
            for response_part in data:
                arr = response_part[0]
                if isinstance(arr, tuple):
                    msg = email.message_from_string(str(arr[1], 'utf-8'))
                    email_subject = msg['subject']
                    email_from = msg['from']
                    email_date = msg['Date']
                    print('From : ' + email_from + '\n')
                    print('Subject : ' + email_subject + '\n')
                    print('Date : ' + email_date + '\n')

                    # Si el mensaje de correo electrónico es de varias partes, entonces ejecute este if
                    if msg.is_multipart():
                        # Hacer la iteración sobre las partes del correo electrónico identificadas
                        for part in msg.walk():
                            # Extraer el contenido del tipo de correo
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            try:
                                # Obtener el cuerpo del correo electrónico
                                body = part.get_payload(decode=True).decode()
                            except:
                                pass
                            if content_type == "text/plain" and "attachment" not in content_disposition:
                                # Imprimir mensajes de correo electronico de texto sin formato y omitir los adjuntos
                                print(body)
                            elif "attachment" in content_disposition:
                                # Descargar archivos adjuntos
                                filename = part.get_filename()
                                if filename:
                                    folder_name = clean(email_subject)
                                    if not os.path.isdir(folder_name):
                                        # Crear una carpeta para este correo electrónico (con nombre del asunto)
                                        os.mkdir(folder_name)
                                    filepath = os.path.join(folder_name, filename)
                                    # Descargar los archivos adjuntos y guardar
                                    open(filepath, "wb").write(part.get_payload(decode=True))
                    else:
                        # Extraer contenido del tipo de correo electrónico
                        content_type = msg.get_content_type()
                        # Obtener el cuerpo del correo
                        body = msg.get_payload(decode=True).decode()
                        if content_type == "text/plain":
                            # Imprimir solo partes de correo electrónico de texto
                            print(body)
                    print("=" * 100)

                    # Identificar los emails que contienen Devops
                    if "DevOps" in body:
                        devops = 1
                        print("Si contiene la palabra DevOps en el body ")
                        lista1.append(email_date)
                        lista2.append(email_from)
                        lista3.append(email_subject)

                    else:
                        print("No contiene la palabra DevOps en el body")
                        devops = 0

                    print(devops)

    except Exception as e:
        traceback.print_exc()
        print(str(e))

read_email()

print("En estas listas estan los correos identificados con la palabra DevOps")
print (lista1, lista2, lista3)



