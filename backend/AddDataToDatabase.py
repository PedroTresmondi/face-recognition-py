from firebase_config import db

ref = db.reference('Person')

data = {
    "142595": {
        "name": "Pedro Tresmondi",
        "email": "pedro_tresmondi@hotmail.com"
    },
    "852741": {
        "name": "Emily Blunt",
        "email": "emily_blunt@hotmail.com"
    },
    "963852": {
        "name": "Elon Musk",
        "email": "elon_musk@hotmail.com"
    }
}

for key, value in data.items():
    ref.child(key).set(value)
