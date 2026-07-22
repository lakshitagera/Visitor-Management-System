import qrcode
import base64
import io

def get_qr_base64(data):
    print("data-->",data)
    qr = qrcode.make(str(data))
    buf = io.BytesIO()
    qr.save(buf)
    return base64.b64encode(buf.getvalue()).decode()
