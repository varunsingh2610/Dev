from django.shortcuts import render
from django.http import HttpResponse
from Crypto.Cipher import AES
import hashlib

# Create your views here.

def encryption(request):
	return render()


def pad(data):
	length = 16 - (len(data) % 16)
	data += chr(length)*length
	return data

def enCrypt(request):
	workingKey = '4ACF0420A50EAB0310A9081C5B35B43C'
	plainText = 'merchant_id=189681&order_id=481&currency=INR&amount=442&redirect_url=http://frugivore.in/payment-gateway/successfull-payment/e39948c7-7d8b-410b-a928-7b3c37bfee74&cancel_url=http://frugivore.in/repeat-order/e39948c7-7d8b-410b-a928-7b3c37bfee74?release=True&language=EN&integration_type=iframe_normal&billing_name=Frugivore&billing_address=D-1, Panchwati, Adarsh Nagar, Delhi, 110033&billing_city=New Delhi&billing_state=New Delhi&billing_zip=110009&billing_country=India&billing_tel=9911737368&billing_email=raghav.malhotra447@gmail.com&customer_identifier=25&'
	iv = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
	plainText = pad(plainText)
	encDigest = hashlib.md5()
	encDigest.update(workingKey.encode())
	enc_cipher = AES.new(encDigest.digest(), AES.MODE_CBC, iv)
	print(type(encDigest.digest()),type(iv))
	new = str(encDigest.digest())
	encryptedText = enc_cipher.encrypt(plainText).hex()
	context = {
		'enKey' : encryptedText
	}
	return render(request, 'encrypt.html', context)
