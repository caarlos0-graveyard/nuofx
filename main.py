from pynubank import Nubank

nu = Nubank()
uuid, qr_code = nu.get_qr_code()

qr_code.print_ascii(invert=True)
input('Após escanear o QRCode, pressione enter...')

nu.authenticate_with_qr_code(os.environ['NU_CPF'], os.environ['NU_PWD'], uuid)

f = open("extrato.csv","w+")
f.write("account;desc;date;amount")
for statement in nu.get_account_statements():
	# hacky af but i dont care
	typename = statement["__typename"]
	if typename == 'TransferOutEvent' or typename == 'BarcodePaymentEvent' or typename == 'DebitPurchaseEvent':
		sign = '-'
	else:
		sign = '+'

	f.write(f'NuConta;{statement["title"]} - {statement["detail"]};{statement["postDate"]};{sign}{statement["amount"]}')
f.close()
