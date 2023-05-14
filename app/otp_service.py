import requests

def send_otp(otp,mobile):
    tem_id = '644553bbd6fc05261863dec2'
    msg = f'your otp is {otp}'
    auth_key = '395201A9XCF3GuWh6442431fP1'
    otp = int(otp)
    sender_id='tilak'

    url = "https://control.msg91.com/api/v5/otp?mobile=&message=&otp=&sender_id="

    payload = {
        "mobile": mobile,
        "message": msg,
        'sender_id':sender_id,
        "otp": otp
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authkey": '395201A9XCF3GuWh6442431fP1'
    }
    
    response = requests.post(url, json=payload, headers=headers)
    print(response.text)