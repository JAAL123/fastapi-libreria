from pathlib import Path
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from jinja2 import Environment, FileSystemLoader
from app.core.config import settings

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_FOLDER = BASE_DIR / "templates"

template_env = Environment(loader=FileSystemLoader(str(TEMPLATE_FOLDER)))

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
    # Para validar si el email se va a enviar o no
    SUPPRESS_SEND=settings.SUPPRESS_SEND,
)


async def send_welcome_email(email_to: str, username: str):

    template = template_env.get_template("welcome.html")
    html_content = template.render(username=username, email=email_to)

    message = MessageSchema(
        subject="Bienvenido a FastApi Libreria",
        recipients=[email_to],
        template_body=html_content,
        subtype=MessageType.html,
    )
    fm = FastMail(conf)
    await fm.send_message(message)
    print(f"Correo enviado a {email_to} ")


async def send_loan_confirmation_email(email_to: str, username: str, book_title: str):
    template = template_env.get_template("loan_confirmation.html")
    html_content = template.render(username=username, book_title=book_title)

    message = MessageSchema(
        subject="Prestamo Confirmado",
        recipients=[email_to],
        body=html_content,
        subtype=MessageType.html,
    )

    fm = FastMail(conf)
    await fm.send_message(message)
    print(f"Correo enviado a {email_to} ")
