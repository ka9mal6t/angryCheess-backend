from email.message import EmailMessage

from pydantic import EmailStr

from app.config import SMTP_USER


def create_reset_pass_template(
        email_to: EmailStr,
        code: str,
):
    email = EmailMessage()

    email['Subject'] = "Reset password"
    email['From'] = SMTP_USER
    email['To'] = email_to

    email.set_content(
        f"""
        <div>
            <h1>Відновлення паролю</h1>
            <h3>Добрий день, Вам було надіслано заяку на зміну пароля, якщо Ви цього не бажаєте цього, просто проігноруйте цей лист.</h3>
            <h1>
                <a href="http://localhost:3000/forgot_pass/{code}" 
                style="display:inline-block;padding:10px 20px;background-color:#007bff;color:#fff;text-decoration:none;border-radius:5px">Змінити пароль</a>
            </h1>
        </div>
        """,
        subtype="html"
    )
    return email
