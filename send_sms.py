import nexmo
 
API_KEY = '76d1b324'
API_SECRET = 'd4ace30618c703cd'

def send_sms(from_phone, to_phone, message): 
    client = nexmo.Client(key=API_KEY, secret=API_SECRET)
    response = client.send_message(
	{'from': from_phone, 'to': to_phone, 'text': message})
    response = response['messages'][0]
    if response['status'] == '0':
    	print 'Sent message', response['message-id']
        print 'Remaining balance is', response['remaining-balance']
	return True
    else:
        print 'Error:', response['error-text']
	return False

