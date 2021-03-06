from threading import Thread
from flask_mail import Message
from app import mail, app
from flask import render_template, current_app


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    """
    A helper function to send emails using Thread calls
    :param subject:
    :param sender:
    :param recipients:
    :param text_body:
    :param html_body:
    :return:
    """
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(
        target=send_async_email, args=(current_app._get_current_object(), msg)
    ).start()
    # mail.send(msg)


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email(
        "[DataGator] Reset Your Password",
        sender=app.config["ADMINS"][0],
        recipients=[user.email],
        text_body=render_template("email/reset_password.txt", user=user, token=token),
        html_body=render_template("email/reset_password.html", user=user, token=token),
    )
