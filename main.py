import base64
import qrcode
from io import BytesIO

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse


app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>QR Code Generator</title>
        </head>
        <body style="font-family: Arial; text-align: center; margin-top: 50px;">
            <h2>QR Code Generator</h2>

            <form action="/generate" method="post">
                <input type="text" name="link" placeholder="Enter link" style="width:300px; padding:8px;" required>
                <br><br>
                <button type="submit" style="padding:10px 20px;">Generate</button>
            </form>
        </body>
    </html>
    """


@app.post("/generate", response_class=HTMLResponse)
def generate(link: str = Form(...)):

    img = qrcode.make(link)

    buffered = BytesIO()
    img.save(buffered, format="PNG")

    qr_base64 = base64.b64encode(buffered.getvalue()).decode()

    return f"""
    <html>
        <head>
            <title>QR Result</title>
        </head>
        <body style="font-family: Arial; text-align: center; margin-top: 50px;">
            <h2>QR Code for:</h2>
            <p>{link}</p>

            <img src="data:image/png;base64,{qr_base64}" width="250"/>

            <br><br>
            <a href="/">Back</a>
        </body>
    </html>
    """
