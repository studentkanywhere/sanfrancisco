from app import db, User
from werkzeug.security import generate_password_hash

NEW_PASSWORD = 'abcd' 

users = User.query.all()
for user in users:
    user.password = generate_password_hash(NEW_PASSWORD)
    print(f"Updated password for user: {user.username}")

db.session.commit()
print("All user passwords have been updated and hashed.")