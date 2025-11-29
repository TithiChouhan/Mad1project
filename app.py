from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask (__name__)
app.secret_key = "123" 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)




###------------------Models----------------###


from datetime import datetime
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    specialization_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), unique=True, nullable=False) 
    role = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    department = db.relationship("Department", back_populates = "doctors")
    appointments= db.relationship("Appointment", back_populates="user")
    

class Department(db.Model):
    __tablename__ = 'departments'
    id =db.Column(db.Integer, primary_key=True) 
    name =db.Column(db.String(100), unique=True, nullable=False)
    description =db.Column(db.Text, nullable=True)
    doctors =db.relationship("User", back_populates = "department")

class Appointment(db.Model):
    __tablename__ = 'appointment'
    id = db.Column(db.Integer,primary_key=True )
    date = db.Column(db.String(20))
    time = db.Column(db.String(20))
    status = db.Column(db.String(20), default='Confirmed')
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    treatment_id = db.Column(db.Integer,db.ForeignKey("treatment.id"), unique=True)
    user = db.relationship("User" ,back_populates = "appointments")


class Treatment(db.Model):
    __tablename__ = "treatment"
    id = db.Column(db.Integer, primary_key=True)
    treat_name = db.Column(db.String(100))
    description = db.Column(db.Text)
    



if __name__ == '__main__':
    with app.app_context():

        db.create_all()
        existing_admin = User.query.filter_by(username="admin").first()

        if not existing_admin:
            admin_db = User(
                username="admin",
                password="admin",
                email="11d@gmail.com",
                role="admin"
            )
            db.session.add(admin_db)
            db.session.commit()
    app.run(debug= True)