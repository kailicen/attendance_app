from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from attendance.config import Config
from flask_admin import Admin
from os import path
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
admin = Admin(name='Attendance Admin', template_mode='bootstrap4')


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    admin.init_app(app)
    login_manager.init_app(app)

    from attendance.views.routes import views
    app.register_blueprint(views)

    create_database(app=app)

    return app


def create_database(app):
    if not path.exists('attendance/database.db'):
        db.create_all(app=app)
        with app.app_context():
            create_admin()
            init_member()


def create_admin():
    hashed_password = bcrypt.generate_password_hash(
        'admin').decode('utf-8')
    from attendance.models import User
    admin = User(if_admin=True, if_member=False, name='Admin', email='hobarttoastmasters6247@gmail.com',
                 password=hashed_password)
    db.session.add(admin)
    db.session.commit()


def init_member():
    from attendance.models import User
    names = ["Rebecca Lyons", "Edwin Quilliam", "Mark Zeeman", "Karina Skegg", "Regina Xiao Qi Chan",
             "Kaili Cen", "Ai-Ming Wong", "Rod Henham", "Dhor Ngorapuol", "William James Cohen",
             "Brendan Michael Mitchell", "Simon Moreau", "Daniel Li",
             "Vivian Zhao", "Rajesh Sharma", "Karen Magraith", "Greg YOST", "Anthony GOGGINS",
             "Adrian NOROUZI", "William Leeson", "Bryan Ly", "Sagar", "Bhuwan Sareen",
             "Tony Quang Nguyen", "Acacia Scott Clark", "Stuart Campbell", "Gemma Campbell"]
    emails = ["moonchild7901@hotmail.com", "fern005@live.com.au", "mzeeman1@bigpond.com", "kombiwomble@gmail.com",
              "chanxiaoqi@yahoo.com", "kailicen226@gmail.com", "aimingwong@yahoo.co.uk", "rod.henham@gmail.com",
              "zhor.ngorapuol444@gmail.com", "bill.cohen@entura.com.au", "brendan@mitchellplasticwelding.com",
              "moreau.simon@hotmail.com", "daniel.zorolee@gmail.com", "vvzhao0607@gmail.com", "luck_lucky59@yahoo.com.au",
              "karens.magraith@bigpond.com", "greg.yost@gmail.com", "a@goggins.id.au", "adrian.norouzi@yahoo.com",
              "william.leeson@optusnet.com.au", "namkheang.ly@gmail.com", "ss.sagar5298@gmail.com",
              "drbhuwansareen@gmail.com", "qdc4690@gmail.com", "acacia.s.clark@gmail.com", "stuart.campbell@live.com.au",
              "gemmacampbell94@outlook.com"]
    mobiles = ["0417 307 658", "0400 254 836", "0477 786 975", "0409 236 243", "0452 505 269", "0411 170 189",
               "0439 306 705", "0448 227 604", "0424 902 474", "0488 774 665", "0429 419 303", "0408 275 858", "0401 378 929",
               "0416 360 067", "0481 338 249", "0438 826 719", "0438 379 976", "0415 556 292", "0404 166 005", "0418 426 586",
               "0452 399 187", "0433 882 833", "0405 997 655", "0452 380 168", "0488 188 846", "0456 764 608", "0404 608 825"]
    for i in range(0, 26):
        user = User(if_member=True,
                    name=names[i], email=emails[i], mobile=mobiles[i])
        db.session.add(user)
        db.session.commit()
