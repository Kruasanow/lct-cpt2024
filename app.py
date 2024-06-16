from flask import Flask, request, jsonify, make_response, render_template, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import hashlib
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
from models import db, Users, Proposal, Incedents, TourObject, Routes
from f import is_valid_email, is_valid_username, is_valid_password, is_valid_passport, is_valid_fsname, is_valid_birthday, is_valid_status, is_valid_sex, is_valid_regreg, is_valid_role, is_valid_problem_status , get_info_about_user, convert_str_to_list, hash_password
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from dotenv import load_dotenv


#------КОНФИГИ---------------------------------------------------#

app = Flask(__name__)

load_dotenv()
DBUSER = os.getenv("dbuser")
DBUSERPASSWORD = os.getenv("dbpassword")
DBHOST = os.getenv("dbhost")
DBPORT = os.getenv("dbport")
DB = os.getenv("db")
SECRETKEY = os.getenv("secret_key")
FOLDER = os.getenv("upload_folder")

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DBUSER}:{DBUSERPASSWORD}@{DBHOST}:{DBPORT}/{DB}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = SECRETKEY

db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
api = Api(app)
CORS(app)

UPLOAD_FOLDER = FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
FLUTTER_WEB_APP = 'templates'

#----------------------------------------------------------------#


#------ГЕНЕРАТОРЫ СТРАНИЦ----------------------------------------#
@app.route('/api')
def api_show():
    return render_template('api.html')

@app.route('/')
def render_page():
    return render_template('index.html')

@app.route('/web/')
def render_page_web():
    return render_template('index.html')

@app.route('/web/<path:name>')
def return_flutter_doc(name):

    datalist = str(name).split('/')
    DIR_NAME = FLUTTER_WEB_APP

    if len(datalist) > 1:
        for i in range(0, len(datalist) - 1):
            DIR_NAME += '/' + datalist[i]

    return send_from_directory(DIR_NAME, datalist[-1])

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))
#----------------------------------------------------------------#

#------МОЗГИ АПИ-------------------------------------------------#

class RegisterAPI(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        sname = data.get('sname')
        name = data.get('name')
        fname = data.get('fname')
        birthday = data.get('birthday')
        nationality = data.get('nationality')
        registration_region = data.get('registration_region')
        sex = data.get('sex')
        passport = data.get('passport')

        if not is_valid_sex(sex):
            return make_response(jsonify({
                'message': 'Invalid sex. Одна буква: f-женщина, m-мужчина, o-другое'}), 400)

        if not is_valid_fsname(name):
            return make_response(jsonify({
                'message': 'Invalid name. Кириллица и латиница. Не более 20 символов по длине имени.'}), 400)

        if not is_valid_fsname(sname):
            return make_response(jsonify({
                'message': 'Invalid surname. Кириллица и латиница. Не более 20 символов по длине фамилии.'}), 400)

        if not is_valid_fsname(fname):
            return make_response(jsonify({
                'message': 'Invalid fathername. Кириллица и латиница. Не более 20 символов по длине отчества..'}), 400)
        
        if not is_valid_birthday(birthday):
            return make_response(jsonify({'message': 'Invalid birthday. Формат 01.02.1990.'}), 400)

        if not is_valid_username(nationality):
            return make_response(jsonify({'message': 'Invalid nationality. Не более 25 символов по длине названия гражданства.'}), 400)

        if not is_valid_regreg(registration_region):
            return make_response(jsonify({'message': 'Invalid reg. region. Латиница и кириллица в верхнем и нижнем регистре, символы ". , : -", пробелы и цифры. Не более 60 символов'}), 400)

        if not is_valid_passport(passport):
            return make_response(jsonify({'message': 'Invalid passport. не более 11 цифр по длине.'}), 400)

        if not is_valid_email(email):
            return make_response(jsonify({'message': 'Invalid email. Пример - example@bk.ru.'}), 400)

        if not is_valid_password(password):
            return make_response(jsonify({'message': 'Invalid password. Не короче 8 символов, Цифры, Верхний и нижний регистры, спец. символы'}), 400)

        if Users.query.filter_by(email=email).first():
            return make_response(jsonify({'message': 'Уже зарегестрирован.'}), 409)

        hashed_password = hash_password(password)
        user = Users(email=email, password=hashed_password, name=name, 
                    sname=sname, fname=fname, birthday=birthday, nationality=nationality,
                    registration_region=registration_region, sex=sex, passport=passport, role='1')
        db.session.add(user)
        db.session.commit()
        return make_response(jsonify({'message': 'Пользователь успешно зарегестрирован'}), 201)

class LoginAPI(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not is_valid_email(email):
            return make_response(jsonify({'message': 'Неверный формат почты.'}), 400)

        user = Users.query.filter_by(email=email).first()
        if user and user.password == hash_password(password):   
            login_user(user)
            
            return make_response(jsonify({"message": "Успешный логин", 
                                          "id":user.id, 
                                          "name":user.name,
                                          "birthday":user.birthday,
                                          "nationality":user.nationality,
                                          "registration_region":user.registration_region,
                                          "sex":user.sex,
                                          "passport":user.passport,
                                          "sname":user.sname,
                                          "fname":user.fname,
                                          "role":user.role}), 200)
        else:
            return make_response(jsonify({'message': 'Неверные учетные данные'}), 401)

class LoginAdminAPI(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not is_valid_email(email):
            return make_response(jsonify({'message': 'Неверный формат почты.'}), 400)

        user = Users.query.filter_by(email=email).first()
        if user and user.password == password:
            if user.role == '2' or user.role == '3':  
                login_user(user)
                
                return make_response(jsonify({"message": "Успешный логин", 
                                            "id":user.id, 
                                            "name":user.name,
                                            "birthday":user.birthday,
                                            "nationality":user.nationality,
                                            "registration_region":user.registration_region,
                                            "sex":user.sex,
                                            "passport":user.passport,
                                            "sname":user.sname,
                                            "fname":user.fname,
                                            "role":user.role}), 200)
            else:
                return make_response(jsonify({"message":"Invalid ROLE. Текущий пользователь не является администратором или модератором"}), 402)
        else:
            return make_response(jsonify({'message': 'Неверные учетные данные'}), 401)

class SendFormAPI(Resource):
    # @login_required
    def post(self):
        data = request.get_json()
        arrive_date = data.get('arrive_date')
        email = data.get('email')
        event_format = data.get('event_format')
        event_aim = data.get('event_aim')
        media = data.get('media')
        status = data.get('status')
        oopt = data.get('oopt')
        user_id = data.get('user_id')

        if not is_valid_birthday(arrive_date):
            return make_response(jsonify({"message":"Invalid arrive_date. Неверный формат даты прибытия, пример - 10.11.2024"}))
        
        if not is_valid_email(email):
            return make_response(jsonify({'message':'Invalid email. Неверный формат email, пример - example@mail.ru'}))

        if not is_valid_status(status):
            return make_response(jsonify({'message','Invalid status. Статус должен быть цифрой от 0 до 9. Глебас, надо по статусам обговорить '}))

        proposal = Proposal(user_id=user_id, arrive_date=arrive_date, email=email, event_format=event_format, 
                            event_aim=event_aim, media=media, status=status, oopt=oopt)
        db.session.add(proposal)
        db.session.commit()
        return make_response(jsonify({'message':'Заявка обработана в бд'}))

class IncedentReport(Resource):
    def post(self):
        if 'photos' not in request.files:
            return make_response(jsonify({'message': 'Не удалось загрузить фотографии: поле "photos" отсутствует'}), 400)
        photos = request.files.getlist('photos')
        comment = request.form.get('comment')
        geo_location = request.form.get('geo_location')
        user = request.form.get('user_id')
        problem_type = request.form.get('problem_type')
        phone = request.form.get('phone')
        email = request.form.get('email')
        status = request.form.get('status')
        
        if not comment or not geo_location or not user or not problem_type or not phone or not email or not status:
            return make_response(jsonify({'message': 'Все поля обязательны', 
                                          'comment': comment,
                                          'geo_location': geo_location,
                                          'user_id': user,
                                          'problem_type': problem_type,
                                          'phone': phone,
                                          'status': status,
                                          'email': email}), 400)

        if not is_valid_problem_status(status):
            return make_response(jsonify({'message':'Статус должен быть - "На рассмотрении", "Выясняется", "В процессе", "Решена"'}),407)

        if photos:
            photo_filenames = []
            for photo in photos:
                if photo.filename == '':
                    continue
                filename = secure_filename(photo.filename)
                curr_folder = app.config['UPLOAD_FOLDER']+email+"/"+problem_type+f"{datetime.now().strftime('_%d-%m-%Y_%H:%M:%S')}"
                
                os.makedirs(str(curr_folder), exist_ok=True)
                photo_path = os.path.join((curr_folder), filename)
                photo.save(photo_path)
                photo_filenames.append(photo_path)

            incedent = Incedents(photos=photo_filenames, comment=comment, geo_location=geo_location, 
                        user_id=user, problem_type=problem_type, phone=phone, status=status, email=email)
            db.session.add(incedent)
            db.session.commit()

            return make_response(jsonify({"message":'Все гуд',
                                          "photos": photo_filenames,
                                          'comment': comment,
                                          'geo_location': geo_location,
                                          'user_id': user,
                                          'problem_type': problem_type,
                                          'phone': phone,
                                          'status': status,
                                          'email': email}), 202)
        return make_response(jsonify({"message":"фоток нет пачемута"}),409)

class GetAdminModer(Resource):
    # @login_required
    def get(self):
        users_with_specific_roles = Users.query.all()
        admin_moder = []
        for user in users_with_specific_roles:
            if user.role == '2' or user.role == '3':
                admin_moder.append(
                    {user.id : {
                    "email": user.email,
                    "password": user.password,
                    "name": user.name,
                    "sname": user.sname,
                    "fname": user.fname,
                    "birthday": user.birthday,
                    "nationality": user.nationality,
                    "registration_region": user.registration_region,
                    "sex": user.sex,
                    "passport": user.passport,
                    "role": user.role
                    }
                    })
            else:
                continue

        return make_response(jsonify({"message": "Администраторы и модераторы", "modersadmins": admin_moder}))

class ChangeRole(Resource):
    def put(self):
        try:
            data = request.get_json()
            user_id = data.get('id')
            new_role = data.get('newrole')
            user = Users.query.get(user_id)
            user.role = new_role
            db.session.commit()
            return make_response(jsonify({"message": f"пользователь с id={user.id} роль изменена на {user.role}"}))
        except Exception as e:
            return make_response(jsonify({"message": f"{e}"}))

class LogoutAPI(Resource):
    @login_required
    def post(self):
        logout_user()
        return make_response(jsonify({'message': 'Успешный выход из учетной записи'}), 200)

class ProtectedAPI(Resource):
    @login_required
    def get(self):
        return make_response(jsonify({'message': f'Hello, {current_user.username}!'}), 200)

class GetOOPTAPI(Resource):
    # @login_required
    def get(self):
        from f import parse_excel_to_json
        return make_response(jsonify(parse_excel_to_json()))

class GetAllIncedents(Resource):
    def get(self):
        incedents = Incedents.query.all()
        inc = {}
        for incedent in incedents:
            user_info = get_info_about_user(incedent.user_id)
            inc[incedent.id] = {
                "comment":incedent.comment,
                "geo_location":incedent.geo_location,
                "user_id":user_info,
                "problem_type":incedent.problem_type,
                "phone":incedent.phone,
                "status":incedent.status,
                "email":incedent.email,
                "photos":incedent.photos
            }
        return make_response(jsonify({'message': "Все гуд", "incedents":inc}))

class GetAllSendedForm(Resource):
    def get(self):
        proposals = Proposal.query.all()
        prop = {}
        for proposal in proposals:
            prop[proposal.id] = {
                "arrive_date" : proposal.arrive_date,
                "email": proposal.email,
                "event_format" : proposal.event_format,
                "event_aim" : proposal.event_aim,
                "media" : proposal.media,
                "status" : proposal.status,
                "oopt" : proposal.oopt,
                "user_id" : proposal.user_id
            }
        return make_response(jsonify({"All Proposals": prop}))

class UpdataProposalStatus(Resource):
    def put(self):
        data = request.get_json()

        curr_id = data.get('id')
        newstatus = data.get('newstatus')
        proposal = Proposal.query.get(curr_id)
        proposal.status = newstatus
        db.session.commit()
        return make_response(jsonify({'message': f'заявка с айди {curr_id} изменила статус на {newstatus}'}))

class GetCurrentUserProposal(Resource):
    def get(self):
        data = request.get_json()
        user_id = data["user_id"]
        current_user = Users.query.filter_by(id=int(user_id)).first()
        proposals = Proposal.query.filter_by(user_id=user_id).all()
        print(proposals)
        res_dict = []
        for proposal in proposals: 
            res_dict.append( {
                "proposal_arrive_date": proposal.arrive_date,
                "proposal_email": proposal.email,
                "proposal_event_format": proposal.event_format,
                "proposal_evemt_aim": proposal.event_aim,
                "proposal_media": proposal.media,
                "proposal_status": proposal.status,
                "proposal_oopt": proposal.oopt,
                "proposal_user_id": {
                    "id": current_user.id,
                    "email":current_user.email, 
                    "password":current_user.password, 
                    "name":current_user.name,
                    "sname":current_user.sname, 
                    "fname":current_user.fname, 
                    "birthday":current_user.birthday, 
                    "nationality":current_user.nationality, 
                    "registration_region":current_user.registration_region, 
                    "sex":current_user.sex, 
                    "passport":current_user.passport, 
                    "role":current_user.role 
                }
            }
            )
        return make_response(jsonify({'message':res_dict}))

class UpdateIncedent(Resource):
    def put(self):
        report_id = request.form.get('report_id')
        photos = request.files.getlist('photos')
        comment = request.form.get('comment')
        geo_location = request.form.get('geo_location')
        user_id = request.form.get('user_id')
        problem_type = request.form.get('problem_type')
        phone = request.form.get('phone')
        email = request.form.get('email')
        status = request.form.get('status')

        res_arr = []
        incedents = Incedents.query.filter_by(id=int(report_id)).first()
        if photos != "":
            if photos == "deleteall": 
                incedents.photos = "No_photo"
                # db.session.commit()
                #крад к фолдерам

            if photos:
                photo_filenames = []
                for photo in photos:
                    if photo.filename == '':
                        continue
                    filename = secure_filename(photo.filename)
                    curr_folder = app.config['UPLOAD_FOLDER']+email+"/"+problem_type+f"{datetime.now().strftime('_%d-%m-%Y_%H:%M:%S')}"
                    
                    os.makedirs(str(curr_folder), exist_ok=True)
                    photo_path = os.path.join((curr_folder), filename)
                    photo.save(photo_path)
                    photo_filenames.append(photo_path)
                incedents.photos = photo_filenames
                res_arr.append(photo_filenames)
        if comment != "": 
            incedents.comment = comment
            res_arr.append(comment)
        if geo_location != "": 
            incedents.geo_location = geo_location
            res_arr.append(geo_location)
        if user_id != "": 
            incedents.user_id = user_id
            res_arr.append(user_id)
        if problem_type != "": 
            incedents.problem_type = problem_type
            res_arr.append(problem_type)
        if phone != "": 
            incedents.phone = phone
            res_arr.append(phone)
        if email != "": 
            incedents.email = email
            res_arr.append(email)
        if status != "": 
            incedents.status = status
            res_arr.append(status)
        db.session.commit()
        return make_response(jsonify({'message':res_arr}))

class MaxCountPeople(Resource):
    def get(self):
        from coeff import TurObjWithoutTimeLim, OneDayTouristRouteWithoutTimeLim
        from route_max_count_people import max_count_people

        tourobjects = TourObject.query.all()
        leha = {}
        for obj in tourobjects:
            first = len(Proposal.query.filter_by(oopt=obj.name).all()) # 1 elem

            routes = Routes.query.filter_by(link_to_tourobject=obj.name).all()
            arr = []
            for route in routes:
                arr.append(OneDayTouristRouteWithoutTimeLim(DTp=float(route.DTp),DGp=float(route.DGp),
                                                            Tdp=float(route.Tdp),tp=int(route.tp)))

            third = TurObjWithoutTimeLim(name=obj.name, 
                                Cfn=convert_str_to_list(obj.Cfn),
                                MC=float(obj.MC), 
                                Ts=float(obj.Ts), 
                                GS=int(obj.GS), 
                                t=int(obj.t), 
                                routes=arr)

            mcp = max_count_people(30, third)
            leha[obj.name] = mcp
        return make_response(jsonify({'mcp':leha}))

class Recomendalka(Resource):
    def get(self):
        from ml_kir import predict_count_people
        data = request.get_json()
        y = data['year']
        m = data['month']
        d = data['day']
        # 1 элемент - посчитать кол-во заявок в БД на каждый парк за день (какой-то)
        # получить от глеба какой день
        # 2 элемент - результат отработки predict_count_people
        # 3 mcp - для одного туристического объекта(парка)
        from coeff import TurObjWithoutTimeLim, OneDayTouristRouteWithoutTimeLim
        from route_max_count_people import max_count_people
        
        # запрос в БД на туристческий объект из таблицы tourobject и route
        tourobjects = TourObject.query.all()
        leha = {}
        for obj in tourobjects:
            first = len(Proposal.query.filter_by(oopt=obj.name).all())
            
            coord = obj.coordinates.split('_')

            second = predict_count_people(datetime(y,m,d),coord[0],coord[1])

            routes = Routes.query.filter_by(link_to_tourobject=obj.name).all()
            arr = []
            for route in routes:
                arr.append(OneDayTouristRouteWithoutTimeLim(DTp=float(route.DTp),DGp=float(route.DGp),
                                                            Tdp=float(route.Tdp),tp=int(route.tp)))

            third = max_count_people(30, TurObjWithoutTimeLim(
                                name=obj.name, 
                                Cfn=convert_str_to_list(obj.Cfn),
                                MC=float(obj.MC), 
                                Ts=float(obj.Ts), 
                                GS=int(obj.GS), 
                                t=int(obj.t), 
                                routes=arr))
            leha[obj.name] = [first,second,third]


        from route_rekomendalka import calculate_ranked_coefficients
        res = calculate_ranked_coefficients(leha)
        return make_response(jsonify({'recommended':res}))

class WeatherForDay(Resource):
    def get(self):
        data = request.get_json()
        y = data['year']
        m = data['month']
        d = data['day']
        lat = data['latitude']
        lang = data['longitude']

        from route_weather_for_day import get_weather_for_selected_day
        res = get_weather_for_selected_day(datetime(y,m,d),lat,lang)
        return make_response(jsonify({'weather':res}))
#----------------------------------------------------------------#

api.add_resource(RegisterAPI, '/api/register')                          # +
api.add_resource(LoginAPI, '/api/login')                                # +
api.add_resource(LogoutAPI, '/api/logout')                              # ~
api.add_resource(ProtectedAPI, '/api/protected')                        # ~
api.add_resource(GetOOPTAPI, '/api/getoopt')                            # +
api.add_resource(SendFormAPI, '/api/sendform')                          # +
api.add_resource(IncedentReport, '/api/incedentreport')                 # +
api.add_resource(LoginAdminAPI, '/api/loginadmin')                      # +
api.add_resource(GetAdminModer, '/api/getadminmoder')                   # +
api.add_resource(ChangeRole, '/api/changerole')                         # +
api.add_resource(GetAllIncedents, '/api/getallincedents')               # +
api.add_resource(GetAllSendedForm, '/api/getallproposals')              # +
api.add_resource(UpdataProposalStatus, '/api/updateproposalstatus')     # +
api.add_resource(GetCurrentUserProposal, '/api/getcurrentuserproposal') # +
api.add_resource(UpdateIncedent, '/api/updateincedent')                 # +
api.add_resource(MaxCountPeople, '/api/maxcountpeople')                 # +
api.add_resource(Recomendalka, '/api/recommended')                      # +
api.add_resource(WeatherForDay, '/api/weatherforday')                   # +

#------END------------------------------------------------------#
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)
