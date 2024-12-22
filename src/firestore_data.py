from firebase_admin import firestore
import os


# return list of access_tokens <List<string>>
def get_TRU_documents():
    db = firestore.client()
    tru_id = os.getenv("TRU_ID")

    # Filter TRU stores
    docs = db.collection("Tenant").where("parent_id", "==", tru_id).stream()
    tru_datas = []

    for doc in docs:
        doc_data = doc.to_dict()
        tru_datas.append({
            "access_token": doc_data["access_token"],
            "business_name": doc_data["business_name"]
        })
    return tru_datas
