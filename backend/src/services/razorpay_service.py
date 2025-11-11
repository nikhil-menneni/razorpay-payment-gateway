import razorpay, os, hmac,hashlib
from fastapi.concurrency import run_in_threadpool
import aiohttp
import aiosmtplib
from email.message import EmailMessage
from pathlib import Path
import os

# Get the base directory where your backend/src folder is
BASE_DIR = Path(__file__).resolve().parent.parent  # points to backend/src/..
INVOICE_DIR = BASE_DIR / "invoices"
INVOICE_DIR.mkdir(exist_ok=True)  # ensures folder exists


razorpay_client = razorpay.Client(auth=(os.getenv("RAZORPAY_KEY_ID"), os.getenv("RAZORPAY_KEY_SECRET")))
RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")

async def create_order(amount:int,currency:str="INR"):
    def blocking_create():
        return razorpay_client.order.create({
            "amount": amount * 100,  # Amount in paise  
            "currency": currency,
             "receipt": "receipt_001"
        })
    order = await run_in_threadpool(blocking_create)
    return order


def verify_payment_signature(razorpay_order_id:str, razorpay_payment_id:str, razorpay_signature:str)->bool:
    expected=hmac.new(
        os.getenv("RAZORPAY_KEY_SECRET").encode(),
        f"{razorpay_order_id}|{razorpay_payment_id}".encode(),
        hashlib.sha256
    ).hexdigest()

    print("here",expected == razorpay_signature)

    return expected == razorpay_signature 

async def download_invoice_pdf(invoice_id:str)->bytes:
    pdf_url = f"https://api.razorpay.com/v1/invoices/{invoice_id}/pdf"

    async with aiohttp.ClientSession() as session:
        async with session.get(
            pdf_url,
            auth=aiohttp.BasicAuth(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET)
        ) as response:
            if response.status == 200:
                pdf_bytes = await response.read()
                return pdf_bytes
            else:
                raise Exception(f"Failed to download PDF. Status code: {response.status}")
            

async def get_invoice_id(payment_id:str) -> str | None:
    url = f"https://api.razorpay.com/v1/invoices?payment_id={payment_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url,auth=aiohttp.BasicAuth(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET)) as response:
            if response.status == 200:
                data = await response.json()
                print("Fetched invoice data:", data)
                if data.get("count", 0) > 0:
                    return data["items"][0]["id"]
            else:
                print("⚠️ Failed to fetch invoices. Status:", response.status)
                print("Response:", await response.text())
                return None
        
async def download_and_save_invoice_pdf(payment_id:str):
    invoice_id=await get_invoice_id(payment_id)
    if invoice_id:
        print("✅ Entered download block")
        pdf_bytes = await download_invoice_pdf(invoice_id)
        print("PDF bytes length:", len(pdf_bytes))
        file_path = INVOICE_DIR / f"{invoice_id}.pdf"
        file_path.write_bytes(pdf_bytes) 
        print(f"✅ Invoice saved at: {file_path.resolve()}")
    else:
        print("⚠️ No invoice found for this payment; skipping PDF save.")


# async def send_invoice_email(to_email:str, pdf_bytes:bytes,invoice_id:str):
#     message = EmailMessage()
#     message["From"] = "nikhilmenneni999@gmail.com"
#     message["To"] = to_email
#     message["Subject"] = f"Invoice {invoice_id} - Your Payment Receipt"
#     message.add_attachment(pdf_bytes, maintype="application", subtype="pdf", filename=f"{invoice_id}.pdf")

#     await aiosmtplib.send(
#         message,
#         hostname="smtp.gmail.com",
#         port=587,
#         start_tls=True,
#         username=os.getenv("EMAIL_USER"),
#         password=os.getenv("EMAIL_PASS"),
#     )