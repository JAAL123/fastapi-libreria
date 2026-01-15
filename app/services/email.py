from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from app.core.config import settings

conf = ConnectionConfig(
    # Conf de credenciales
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    # conf de certificados
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    #
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)


async def send_welcome_email(email_to: str, username: str):
    # Enviar correo de bienvenida
    html = f""" 
    <h1>¡Bienvenido a la Biblioteca {username}!</h1>
    <p> Gracias por registrarte. Puedes empezar a pedir libros </p>
    """
    message = MessageSchema(
        subject="Bienvenido a la Biblioteca",
        recipients=[email_to],
        body=html,
        subtype=MessageType.html,
    )

    fm = FastMail(conf)
    await fm.send_message(message)
    print(f"Correo enviado a {email_to} ")


async def send_loan_confirmation_email(email_to: str, username: str, book_title: str):
    # Enviar correo de confirmacion de prestamo
    html = f"""
    <h1> Prestamo Confirmado </h1>
    <p> Hola ${username}, has tomado prestado el libro {book_title} </p>
    <p> Por favor no olvides retornarlo a tiempo </p>
    """

    message = MessageSchema(
        subject="Prestamo Confirmado",
        recipients=[email_to],
        body=html,
        subtype=MessageType.html,
    )

    fm = FastMail(conf)
    await fm.send_message(message)
    print(f"Correo enviado a {email_to} ")
