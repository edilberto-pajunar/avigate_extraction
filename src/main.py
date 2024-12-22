from firestore_config import initialize_firestore
from firestore_data import get_TRU_documents
from message import process_token_with_pandas

def main():
        # Initialize Firestore
        initialize_firestore()
        
        # Fetch and print first two documents
        tru_datas = get_TRU_documents()
        print(tru_datas[28])
        
        for tru_data in tru_datas[26:]:
                print(f"TRU Access Tokens: {tru_data}")
                process_token_with_pandas(tru_data)

                
        # with ThreadPoolExecutor(max_workers=5) as executor:
        #         # Fetch all conversations concurrently
        #         futures = executor.map(prscess_token_with_pandas, tru_datas)

if __name__ == "__main__":
    main()
    