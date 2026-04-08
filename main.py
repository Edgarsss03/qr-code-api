import base64
import qrcode
from io import BytesIO

import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel


class QrCodeItemIn(BaseModel):
    link: str


class QrCodeItemOut(BaseModel):
    link: str | None = None
    QrCodeBase64String: str | None = None


app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/")
async def root():
    return {"message": "Hello World"}


@app.post("/getqrcode/", response_model=QrCodeItemOut)
async def generate_qrcode(req: QrCodeItemIn):

    resp = QrCodeItemOut()
    resp.link = req.link

    img = qrcode.make(req.link)

    buffered = BytesIO()
    img.save(buffered, format="PNG")

    qr_img_bytes = base64.b64encode(buffered.getvalue()).decode()

    resp.QrCodeBase64String = qr_img_bytes

    return resp


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)