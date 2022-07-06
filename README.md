# flask_lesson_02 (SQLite3, CRUD)

# Task 1. Создать таблицу phones с полями contactName, phone
# Task 2. Реализовать CRUD операции для таблицы phones (/phones/create/, /phones/read/, /phones/update/, /phones/delete/)

# realization:
    The paths are available in this app:
    
    / or  /phones/help/
    --home page
    
    /phones/create/?name=value&phone=value<
    --page for creating a new contact
    --there is a check of the validity of the phone number
        the number of characters must be 10
        all of characters must be a digit
        checking valid mobile operator codes
    --there is a check of the validity of the contact name <br>
        the contact name must be not less than 3 characters</li>
        the contact name must be not less than 20 characters</li><br>   
    
    /phones/delete/?phone=value
    --page for deleting a contact by phone
    
    /phones/update/?phone=value&new_name=value&new_phone=value
    --page for changing values (new_name or/and new_phone) in contact (by phone)<br>
    --there is a check of the validity of the phone number <br>
        the number of characters must be 10
        all of characters must be a digit
        checking valid mobile operator codes
    --there is a check of the validity of the contact name 
        the contact name must be not less than 3 characters
        the contact name must be not less than 20 characters
     
    /phones/read/
    --page for get all contacts
    
    --this page can accept parameters (id=int, name=str, phone=tsr) to filter data<br>
    /phones/read/?id=value
    --get contacts by id (exact match)
    
    /phones/read/?name=value
    --get contacts by name (any fragment)
    
    /phones/read/?phone=value
    --get contacts by phone (any fragment)
    
    /phones/read/?name=value&phone=value
    --get contacts by name (any phone fragment) and phone (any phone fragment)
