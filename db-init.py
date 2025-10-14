from app import db, User

db.create_all()

# Optionally, add a test user
user = User(username='admin')
user.set_password('#4TurkeyTom')
db.session.add(user)
db.session.commit()