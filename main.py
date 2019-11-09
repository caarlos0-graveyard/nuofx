import json
import os
import xml.etree.cElementTree as ET
from datetime import datetime, timedelta
from xml.dom import minidom

from pynubank import Nubank

nu = Nubank()
now = datetime.now().strftime('%Y%m%d')
d60 = datetime.now() - timedelta(days=60)
date_format = '%Y%m%d'
cpf = os.getenv('NU_CPF', '')
pwd = os.getenv('NU_PWD', '')
test_file = os.getenv('NU_TEST_FILE', '')
statements = []
balance = 0.00

# used to test from a json file with the statements
if test_file == "":
    if cpf == "" or pwd == "":
        print("missing cpf and/or password")
        raise SystemExit()

    uuid, qr_code = nu.get_qr_code()
    qr_code.print_ascii(invert=True)
    input('scan and press enter...')
    nu.authenticate_with_qr_code(
        os.environ['NU_CPF'],
        os.environ['NU_PWD'],
        uuid
    )

    balance = nu.get_account_balance()
    statements = nu.get_account_statements()
else:
    with open(test_file) as json_file:
        statements = json.load(json_file)
        balance = 1233.11

print(f'creating 60-day OFX file of account with balance {balance}...')

# here begins the uglyness
# I'm extremely regretful right now
ofx = ET.Element("OFX")

signonmsgsrsv1 = ET.SubElement(ofx, "SIGNONMSGSRSV1")
sonrs = ET.SubElement(signonmsgsrsv1, "SONRS")
sonrsStatus = ET.SubElement(sonrs, "STATUS")
ET.SubElement(sonrsStatus, "CODE").text = "0"
ET.SubElement(sonrsStatus, "SEVERITY").text = "INFO"
ET.SubElement(sonrs, "DTSERVER").text = now
ET.SubElement(sonrs, "LANGUAGE").text = "POR"
sonrsFI = ET.SubElement(sonrs, "FI")
sonrsFIOrg = ET.SubElement(sonrsFI, "ORG").text = "NuBank"
sonrsFID = ET.SubElement(sonrsFI, "FID").text = "260"

bankmsgsrsv1 = ET.SubElement(ofx, "BANKMSGSRSV1")
stmttrnrs = ET.SubElement(bankmsgsrsv1, "STMTTRNRS")
ET.SubElement(stmttrnrs, "TRNUID").text = "1001"
stmtstatus = ET.SubElement(stmttrnrs, "STATUS")
ET.SubElement(stmtstatus, "CODE").text = "0"
ET.SubElement(stmtstatus, "SEVERITY").text = "INFO"

stmtrs = ET.SubElement(stmttrnrs, "STMTRS")
ET.SubElement(stmtrs, "CURDEF").text = "BRL"

bankacctfrom = ET.SubElement(stmtrs, "BANKACCTFROM")
ET.SubElement(bankacctfrom, "BANKID").text = "260"
ET.SubElement(bankacctfrom, "BRANCHID").text = "0001"
ET.SubElement(bankacctfrom, "ACCTID").text = "1234"
ET.SubElement(bankacctfrom, "ACCTTYPE").text = "CHECKING"

banktranlist = ET.SubElement(stmtrs, "BANKTRANLIST")
ET.SubElement(banktranlist, "DTSTART").text = d60.strftime(date_format)
ET.SubElement(banktranlist, "DTEND").text = now

for statement in statements:
    stmdate = datetime.strptime(statement["postDate"], '%Y-%m-%d')

    # ifnore if older than 60d
    if (datetime.now() - stmdate).days > 60:
        continue

    memo = f'{statement["title"]}: {statement["detail"]}'
    typename = statement["__typename"]

    stm = ET.SubElement(banktranlist, "STMTTRN")

    # TODO: maybe improve TRNTYPEs here
    if typename == 'TransferOutEvent' or typename == 'BarcodePaymentEvent' or typename == 'DebitPurchaseEvent':
        ET.SubElement(stm, "TRNTYPE").text = "DEBIT"
        ET.SubElement(stm, "TRNAMT").text = f'-{statement["amount"]}'
    else:
        ET.SubElement(stm, "TRNTYPE").text = "CREDIT"
        ET.SubElement(stm, "TRNAMT").text = f'{statement["amount"]}'

    ET.SubElement(stm, "DTPOSTED").text = stmdate.strftime(date_format)
    ET.SubElement(stm, "FITID").text = statement["id"]
    ET.SubElement(stm, "CHECKNUM").text = "260"
    ET.SubElement(stm, "REFNUM").text = "260"
    ET.SubElement(stm, "MEMO").text = memo

ledgerbal = ET.SubElement(stmtrs, "LEDGERBAL")
ET.SubElement(ledgerbal, "BALAMT").text = f'{balance}'
ET.SubElement(ledgerbal, "DTASOF").text = now

xmlstr = minidom.parseString(ET.tostring(ofx)).toprettyxml(indent="\t")
with open("/tmp/extrato.ofx", "w") as f:
    f.write(xmlstr)
