import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from config import *

def formList(server_id, lift):
    ref = db.reference(f"/")
    servRef = ref.child(server_id)
    lst = []
    temp = servRef.get()
    for i in temp:
        if lift == "total":
            weight = temp[i][lift]
        else:
            if temp[i][lift] is None:
                weight = "0"
            else:
                weight = temp[i][lift]["latest"]
        lst.append((int(i), int(weight)))
    sorted_list = sorted(lst, key=lambda x: x[1])[::-1]
    return sorted_list

