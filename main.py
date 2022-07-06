from flask import Flask, request
from phones import Contact

app = Flask(__name__)

links = '''<br><br>
    <a href="/phones/help/">Help page</a>
    <a href="/phones/read/">All contacts</a>
    '''

@app.route('/')
@app.route('/phones/help/')
def index():
    page_text = '''
    The paths are available in this app: <br><br>
    
    <strong>/</strong>  or  <strong>/phones/help/</strong> <br>
    --this page <br><br>
    
    <strong>/phones/create/?name=value&phone=value</strong> <br>
    --page for creating a new contact <br>
    --there is a check of the validity of the phone number <br>
        <li>the number of characters must be 10
        <li>all of characters must be a digit</li>
        <li>checking valid mobile operator codes</li>
    --there is a check of the validity of the contact name <br>
        <li>the contact name must be not less than 3 characters</li>
        <li>the contact name must be not less than 20 characters</li><br>   
    
    <strong>/phones/delete/?phone=value</strong> <br>
    --page for deleting a contact by phone<br><br>
    
    <strong>/phones/update/?phone=value&new_name=value&new_phone=value</strong> <br>
    --page for changing values (new_name or/and new_phone) in contact (by phone)<br>
    --there is a check of the validity of the phone number <br>
        <li>the number of characters must be 10
        <li>all of characters must be a digit</li>
        <li>checking valid mobile operator codes</li>
    --there is a check of the validity of the contact name <br>
        <li>the contact name must be not less than 3 characters</li>
        <li>the contact name must be not less than 20 characters</li><br> 
     
    <strong>/phones/read/</strong> <br>
    --page for get all contacts<br><br>
    
    --this page can accept parameters (id=int, name=str, phone=tsr) to filter data<br>
    <strong>/phones/read/?id=value</strong> <br>
    --get contacts by id (exact match)<br><br>
    
    <strong>/phones/read/?name=value</strong> <br>
    --get contacts by name (any name fragment)<br><br>
    
    <strong>/phones/read/?phone=value</strong> <br>
    --get contacts by phone (any phone fragment)<br><br>
    
    <strong>/phones/read/?name=value&phone=value</strong> <br>
    --get contacts by name (any phone fragment) and phone (any phone fragment)<br><br>

    '''
    return page_text


@app.route('/phones/create/')
def phones_create():
    name = request.args['name']
    phone = request.args['phone']

    if not Contact().validate_name(name).get('is_valid'):
        return Contact().validate_name(name)["msg"]
    else:
        if not Contact().validate_phone(phone).get('is_valid'):
            return Contact().validate_phone(phone)["msg"]
        else:
            if Contact().phone_is_exists(phone):
                return f'Phone: {phone} already exists in the database! Try to change the number!'
            else:
                contact = Contact()
                contact.create(name, phone)
                return f'New contact ContactName: {name}, Phone: {phone} created! {links}'


@app.route('/phones/read/')
def phones_read():
    phone = request.args.get('phone') or ''
    name = request.args.get('name') or ''
    _id = request.args.get('id') or '0'

    if _id.isdigit():
        _id = int(_id)
    else:
        return f'Invalid parameter id {_id}. Integer is expected.'

    contacts_list = Contact().read(_id, name, phone)
    result = ''
    if len(contacts_list) == 0:
        if phone == '' and name == '' and _id == 0:
            return 'Sorry, database is empty.'
        else:
            return 'Sorry, no contacts found. Try changing your search parameters.'
    else:
        for item in contacts_list:
            result += f'''<p>id: <strong>{str(item[0])}</strong> \
                      , ContactName: <strong>{str(item[1])}</strong> \
                      , Phone: <strong>{str(item[2])}</strong> \
                       <a href="/phones/delete/?phone={str(item[2])}">delete</a></p>'''

    return f'Contacts: ({len(contacts_list)}) <br>' + result


@app.route('/phones/delete/')
def phones_delete():
    phone = request.args['phone']
    if not Contact().phone_is_exists(phone):
        return f'Phone: {phone} is not in the database! Try to change the number for delete!'
    else:
        contact = Contact()
        contact.delete(phone)
        return f'Phone: {phone} deleted! {links}'


@app.route('/phones/update/')
def phones_update():
    phone = request.args.get('phone', 'none', type=str)
    new_name = request.args.get('new_name', 'none', type=str)
    new_phone = request.args.get('new_phone', 'none', type=str)

    if phone == 'none':
        return f'Parameter phone is empty! It is required!'
    else:
        if not Contact().phone_is_exists(phone):
            return f'Phone: {phone} is not in the database! Try to change parameter phone for update!'
        else:
            if new_name != 'none':
                if not Contact().validate_name(new_name).get('is_valid'):
                    return Contact().validate_name(new_name)["msg"]
            elif new_phone != 'none':
                if not Contact().validate_phone(new_phone).get('is_valid'):
                    return Contact().validate_phone(new_phone)["msg"]
            else:
                return f'Pass at least one parameter (new_name or/and new_phone) to change!'

            contact = Contact()
            contact.update(phone, new_name, new_phone)
            return f'Contact with phone {phone} updated successfully!! {links}'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
