import re

def is_valid_role(role):
    regex = r'^[123]{1}$'
    return re.match(regex, role)

def is_valid_email(email):
    regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.match(regex, email)

def is_valid_password(password):
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[!@#\$%\^&\*]", password):
        return False
    return True

def is_valid_regreg(reg):
    regex = r'^[a-zA-Zа-яА-Я0-9.,:\-\s]{1,120}$'
    return re.match(regex, reg)

def is_valid_status(status):
    regex = r'^[0-9]{1}$'
    return re.match(regex, status)

def is_valid_username(username):
    regex = r'^[A-Za-zА-Яа-я0-9]{1,25}$'
    return re.match(regex, username)

def is_valid_passport(passport):
    regex = r'^[0-9]{1,10}$'
    return re.match(regex, passport)

def is_valid_fsname(fsname):
    regex = r'^[а-яА-Яa-zA-Z]{1,20}$'
    return re.match(regex, fsname)

def is_valid_birthday(bday):
    regex = r'^[0-9]{1,2}.[0-9]{1,2}.[0-9]{1,4}$'
    return re.match(regex, bday)

def is_valid_sex(sex):
    regex = r'^[mfo]{1}$'
    return re.match(regex, sex)

def is_valid_problem_status(status):
    if status not in ["На рассмотрении", "Выясняется", "В процессе", "Решена"]:
        return False
    return True

def get_info_about_user(user_id):
    from models import Users
    users = Users.query.all()
    for user in users:
        if str(user.id) == str(user_id):
            return {"email":user.email, "password":user.password, "name":user.name, 
                    "sname":user.sname, "fname":user.fname, "birthday":user.birthday, 
                    "nationality":user.nationality, "registration_region":user.registration_region, 
                    "sex":user.sex, "passport":user.passport, "role":user.role }  
    return False       

def hash_password(password):
    import hashlib
    h = hashlib.new('sha256')
    h.update(password.encode())
    return h.hexdigest()

def convert_str_to_list(stroka):
    import ast
    list_data = list(ast.literal_eval(stroka))
    return list_data

# def parse_excel_to_json():
#     import pandas as pd
#     import json
#     import re
#     try:
#         file_path = 'oopt/OOPT.xlsx'
#         xls = pd.ExcelFile(file_path)
#     except ImportError as e:
#         return f"Ошибка импорта: {e}"

#     all_sheets_data = {}

#     for sheet_name in xls.sheet_names:
#         df = pd.read_excel(xls, sheet_name=sheet_name, header=None)
        
#         sheet_data = {}
        
#         for i in range(22):
#             key = str(df.iloc[i, 0]).strip().replace("\n", " ").replace("\"", "")
#             value = str(df.iloc[i, 1]).strip().replace("\n", " ").replace("\"", "")
#             sheet_data[key] = value
        
#         points = {}
#         for i in range(22, len(df)):
#             point_num = str(df.iloc[i, 0]).strip()
#             if pd.isna(point_num):
#                 break
#             longitude = str(df.iloc[i, 1]).strip().replace("\"", "")
#             latitude = str(df.iloc[i, 2]).strip().replace("\"", "")
#             points[point_num] = {"longitude": longitude, "latitude": latitude}
        
#         sheet_data["points"] = points
        
#         events = {}
#         i = 22
#         while i < len(df):
#             if pd.isna(df.iloc[i, 4]):
#                 i += 1
#                 continue
#             event_key = str(df.iloc[i, 4]).strip().replace("\n", " ").replace("\"", "")
#             event_data = {}
#             i += 1
#             while i < len(df) and not pd.isna(df.iloc[i, 4]):
#                 key = str(df.iloc[i, 4]).strip().replace("\n", " ").replace("\"", "")
#                 value = str(df.iloc[i, 5]).strip().replace("\n", " ").replace("\"", "")
#                 if not pd.isna(df.iloc[i, 6]):
#                     value += " " + str(df.iloc[i, 6]).strip().replace("\n", " ").replace("\"", "")
#                 if re.match(r'\d+°\d+\'\d+', value):
#                     coordinates = value.split(' ')
#                     if len(coordinates) == 2:
#                         value = coordinates
#                 event_data[key] = value
#                 i += 1
#             events[event_key] = event_data

#         sheet_data["events"] = events
        
#         all_sheets_data[sheet_name] = sheet_data
    
#     return all_sheets_data
def parse_excel_to_json():
    import pandas as pd
    import json
    import re
    try:
        file_path = 'oopt/OOPT_new6.xlsx'
        xls = pd.ExcelFile(file_path)
    except ImportError as e:
        return f"Ошибка импорта: {e}"

    all_sheets_data = {}

    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name, header=None)
        
        sheet_data = {}

        for i in range(22):
            key = str(df.iloc[i, 0]).strip().replace("\n", " ").replace("\"", "")
            value = str(df.iloc[i, 1]).strip().replace("\n", " ").replace("\"", "")
            sheet_data[key] = value
        
        points = {}
        for i in range(22, len(df)):
            point_num = str(df.iloc[i, 0]).strip()
            if pd.isna(point_num):
                break
            longitude = str(df.iloc[i, 1]).strip().replace("\"", "")
            latitude = str(df.iloc[i, 2]).strip().replace("\"", "")
            points[point_num] = {"longitude": longitude, "latitude": latitude}
        
        sheet_data["points"] = points
        
        events = {}
        i = 22
        while i < len(df):
            if pd.isna(df.iloc[i, 4]):
                i += 1
                continue
            event_key = str(df.iloc[i, 4]).strip().replace("\n", " ").replace("\"", "")
            event_data = {}
            point_names_and_coords = []
            i += 1
            while i < len(df) and not pd.isna(df.iloc[i, 4]):
                key = str(df.iloc[i, 4]).strip().replace("\n", " ").replace("\"", "")
                value = str(df.iloc[i, 5]).strip().replace("\n", " ").replace("\"", "")
                if not pd.isna(df.iloc[i, 6]):
                    value += " " + str(df.iloc[i, 6]).strip().replace("\n", " ").replace("\"", "")
                if re.match(r'\d+°\d+\'\d+', value):
                    coordinates = value.split(' ')
                    if len(coordinates) == 2:
                        point_names_and_coords.append({key: coordinates})
                        value = coordinates
                event_data[key] = value
                i += 1
            if point_names_and_coords:
                event_data["Точки по порядку"] = point_names_and_coords
            events[event_key] = event_data

        sheet_data["events"] = events
        
        all_sheets_data[sheet_name] = sheet_data
    
    return all_sheets_data