from app import app, db, User 


# Push the application context to interact with the database
with app.app_context():
    users = User.query.all()
    for user in users:
        print(user.username, user.role)

