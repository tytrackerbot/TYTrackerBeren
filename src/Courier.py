from TYItem import TYItem
import os
import smtplib
import imghdr
from email.message import EmailMessage
import jsonpickle

mail_address = os.environ.get('MAIL_USERNAME')
mail_password = os.environ.get('MAIL_PASSWORD')
receiver_address = os.environ.get('RECEIVER_USERNAME')

# Set Mail Credentials
msg = EmailMessage()
msg['Subject'] = 'TY DISCOUNT !!!'
msg['From'] = mail_address
msg['To'] = receiver_address

# Obtain TYItems using jsonpickle
data_path = os.path.dirname(os.path.abspath(
    __file__)) + os.path.sep + os.path.join('..', 'data')
with open(os.path.join(data_path, 'tracked_items.json'), 'r') as file:
    content = file.read()
    items = jsonpickle.decode(content)


def getMinNeglectNone(price_list):
    return min([price for price in price_list if price is not None])


suitable_items = [item for item in items
                  if not item.informed and getMinNeglectNone([item.old_price,
                                                              item.default_price,
                                                              item.cartbox_price]) <= item.threshold]

if 0 < len(suitable_items):
    # Generate mail message
    string = '\n'.join([str(item) for item in suitable_items])
    html_msg = string.replace('\n', '<br>')
    msg.add_alternative(f'''\
    <!DOCTYPE html>
    <html>
        <body>
            <h2>Items:</h2>
                <p>{html_msg}</p>
        </body>
    </html>
    ''', subtype='html')

    # Send mail
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(mail_address, mail_password)
        smtp.send_message(msg)

    # Mark items informed
    for item in suitable_items:
        item.setInformed(state=True)

    with open(os.path.join(data_path, 'tracked_items.json'), 'w') as file:
        frozen = jsonpickle.encode(items)
        file.write(frozen)
        file.truncate()
