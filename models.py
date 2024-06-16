from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Users(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    
    name = db.Column(db.String(150), nullable=False)
    sname = db.Column(db.String(150), nullable=False)
    fname = db.Column(db.String(150), nullable=False)
    birthday = db.Column(db.String(150), nullable=False)
    nationality = db.Column(db.String(150), nullable=False)
    registration_region = db.Column(db.String(150), nullable=False)
    sex = db.Column(db.String(150), nullable=False)
    passport = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(150), nullable=False)

    def __init__(self, email, password, name, sname, fname, birthday, nationality, registration_region, sex, passport, role):
        self.email = email
        self.password = password
        self.name = name
        self.sname = sname
        self.fname = fname
        self.birthday = birthday
        self.nationality = nationality
        self.registration_region = registration_region
        self.sex = sex
        self.passport = passport
        self.role = role

class Proposal(db.Model):
    __tablename__ = 'proposal'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(150), nullable=False)
    arrive_date = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    event_format = db.Column(db.String(150), nullable=False)
    event_aim = db.Column(db.String(150), nullable=False)
    media = db.Column(db.String(150), nullable=False)
    status = db.Column(db.String(150), nullable=False)
    oopt = db.Column(db.String(150), nullable=False)

    def __init__(self, user_id, arrive_date, email, event_format, event_aim, media, status, oopt):
        self.user_id = user_id
        self.arrive_date = arrive_date
        self.email = email
        self.event_format = event_format
        self.event_aim = event_aim
        self.media = media
        self.status = status
        self.oopt = oopt

class Incedents(db.Model):
    __tablename__ = 'incedents'

    id = db.Column(db.Integer, primary_key=True)
    photos = db.Column(db.String(550), nullable=False)
    comment = db.Column(db.String(150), nullable=False)
    geo_location = db.Column(db.String(150), nullable=False)
    user_id = db.Column(db.String(150), nullable=False)
    problem_type = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(150), nullable=False)
    status = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)

    def __init__(self, photos, comment, geo_location, user_id, problem_type, phone, status, email):
        self.photos = photos
        self.comment = comment
        self.geo_location = geo_location
        self.user_id = user_id
        self.problem_type = problem_type
        self.phone = phone
        self.status = status
        self.email = email

class TourObject(db.Model):
    __tablename__ = 'tourobject'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(550), nullable=False)
    Cfn = db.Column(db.String(150), nullable=False)
    MC = db.Column(db.String(150), nullable=False)
    Ts = db.Column(db.String(150), nullable=False)
    GS = db.Column(db.String(150), nullable=False)
    t = db.Column(db.String(150), nullable=False)
    routes = db.Column(db.String(150))
    coordinates = db.Column(db.String(150), nullable=False)

    def __init__(self, name, Cfn, MC, Ts, GS, t, routes, coordinates):
        self.name = name
        self.Cfn = Cfn
        self.MC = MC
        self.Ts = Ts
        self.GS = GS
        self.t = t
        self.routes = routes
        self.coordinates = coordinatess

class Routes(db.Model):
    __tablename__ = 'routes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(550), nullable=False)
    DTp = db.Column(db.String(150), nullable=False)
    DGp = db.Column(db.String(150), nullable=False)
    Tdp = db.Column(db.String(150), nullable=False)
    tp = db.Column(db.String(150), nullable=False)
    link_to_tourobject = db.Column(db.String(150), nullable=False)

    def __init__(self, name, DTp, DGp, Tdp, tp, link_to_tourobject):
        self.name = name
        self.DTp = DTp
        self.DGp = DGp
        self.Tdp = Tdp
        self.tp = tp
        self.link_to_tourobject = link_to_tourobject