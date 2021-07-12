import pandas as pd
from datetime import datetime


df = pd.read_csv('transactions20210514.csv')


def header_1():
    return """<ENVELOPE>
 <HEADER>
  <TALLYREQUEST>Import Data</TALLYREQUEST>
 </HEADER>
 <BODY>
  <IMPORTDATA>
   <REQUESTDESC>
    <REPORTNAME>Vouchers</REPORTNAME>
    <STATICVARIABLES>
     <SVCURRENTCOMPANY>HOUSE OF RAMAPURAM</SVCURRENTCOMPANY>
    </STATICVARIABLES>
   </REQUESTDESC>
   <REQUESTDATA>
    <TALLYMESSAGE xmlns:UDF="TallyUDF">
     <VOUCHER VCHTYPE="Receipt" ACTION="Create" OBJVIEW="Accounting Voucher View">
    """


def header_2(date: str):
    return f"""  <DATE>{date}</DATE>
      <NARRATION>Being the amount received against referance no AXISCN0074667298</NARRATION>
      <VOUCHERTYPENAME>Receipt</VOUCHERTYPENAME>
      <PARTYLEDGERNAME>Sidapur.Com</PARTYLEDGERNAME>
      <PERSISTEDVIEW>Accounting Voucher View</PERSISTEDVIEW>
      """


def entry_1(amount):
    return f"""<ALLLEDGERENTRIES.LIST>
       <LEDGERNAME>HDFC Bank</LEDGERNAME>
       <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
       <ISPARTYLEDGER>Yes</ISPARTYLEDGER>
       <AMOUNT>-{amount:.2f}</AMOUNT>
      </ALLLEDGERENTRIES.LIST>
      """


def entry_2(amount, name):
    return f"""<ALLLEDGERENTRIES.LIST>
       <LEDGERNAME>Sidapur.Com</LEDGERNAME>
       <ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE>
       <ISPARTYLEDGER>Yes</ISPARTYLEDGER>
       <AMOUNT>-{amount:.2f}</AMOUNT>
       <BILLALLOCATIONS.LIST>
        <NAME>{name}</NAME>
        <BILLTYPE>Agst Ref</BILLTYPE>
        <AMOUNT>-{amount:.2f}</AMOUNT>
       </BILLALLOCATIONS.LIST>
      </ALLLEDGERENTRIES.LIST>
      """


def entry_3(fee: float):
    return f"""<ALLLEDGERENTRIES.LIST>
       <LEDGERNAME>Razorpay Software Pvt. Ltd</LEDGERNAME>
       <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
       <ISPARTYLEDGER>Yes</ISPARTYLEDGER>
       <AMOUNT>-{fee:.2f}</AMOUNT>
      </ALLLEDGERENTRIES.LIST>
      """


def entry_4(sum: float):
    return f"""<ALLLEDGERENTRIES.LIST>
       <LEDGERNAME>Sidapur.Com</LEDGERNAME>
       <ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE>
       <ISPARTYLEDGER>Yes</ISPARTYLEDGER>
       <AMOUNT>{sum:.2f}</AMOUNT>
       """


def entry_5_repeat(row: pd.Series):
    return f"""<BILLALLOCATIONS.LIST>
        <NAME>{row['description']}</NAME>
        <BILLTYPE>Agst Ref</BILLTYPE>
        <AMOUNT>{row['amount']:.2f}</AMOUNT>
       </BILLALLOCATIONS.LIST>
       """


def final_part():
    return '''</ALLLEDGERENTRIES.LIST>
     </VOUCHER>
    </TALLYMESSAGE>
   </REQUESTDATA>
  </IMPORTDATA>
 </BODY>
</ENVELOPE>
'''

if __name__ == '__main__':

    # Rendering template
    final = header_1() + header_2(datetime.today().strftime(f"%Y%m%d"))
    final += entry_1(df[df['type'] == 'settlement']['amount'].values[0])
    final += entry_2(df[df['type'] == 'refund']['amount'].values[0],
                    df[df['type'] == 'refund']['description'].values[0])
    final += entry_3(df['fee'].sum())
    df_copy = df[df['type'] == 'payment']
    final += entry_4(df_copy['amount'].sum())
    final += ''.join(df_copy.apply(entry_5_repeat, axis=1))
    final += final_part()

    with open('result.xml', 'w') as f:
        f.write(final)
        print('Created XML file!')
