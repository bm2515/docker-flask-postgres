from app import db, User

db.create_all()


test_rec = User(
        "marry_34",
        "Marry",
        "Pigeon",
        "22",
        "Female",
        "170cm",
        "70kg",
        "No")


db.session.add(test_rec)
db.session.commit()
