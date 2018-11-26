# Checks if any insert statement is there :
def check_insert(data):
    for s in data:
        if 'insert' in s and 'into' in s:
            return False
    return True 

# Checks if any drop statement is there :
def check_drop(data):
    for s in data:
        if 'select' in s and 'from' in s:
            return False
    return True 

# Checks if any update statement is there :
def check_update(data):
    for s in data:
        if 'update' in s and 'set' in s:
            return False
    return True 

# Checks if any alter statement is there :
def check_alter(data):
    for s in data:
        if 'select' in s and 'from' in s:
            return False
    return True 

# Checks if any insert statement is there :
def break_data(data):
    l = [ x.lower() for x in data.split(';')]
    li = [ i.split() for i in l ]
    print(li)
    return li

# Checks if any select statement is there :
def check_select(data):
    for s in data:
        if 'select' in s and 'from' in s:
            return False
    return True 

# Checks if any delete statement is there :
def check_delete(data):
    for s in data:
        if 'delete' in s and 'from' in s:
            return False
    return True

# Checks if any grant statement is there :
def check_grant(data):
    for s in data:
        if 'grant' in s:
            return False
    return True

# Main function to check the validity of the data:
def isValid(data):
    lines = break_data(data)
    print('/////////////////////',lines)
    errors = False

    if check_alter(lines) is False:
        print(1)
        errors = True
    if check_delete(lines) is False:
        print(2)
        errors = True
    if check_drop(lines) is False:
        print(3)
        errors = True
    if check_insert(lines) is False:
        print(4)
        errors = True
    if check_update(lines) is False:
        print(5)
        errors = True
    if check_grant(lines) is False:
        print(6)
        errors = True
    
    return errors
    