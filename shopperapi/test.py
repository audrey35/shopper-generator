from bson import ObjectId

from shoppermodel import ShopperDatabase

if __name__ == '__main__':
    db = ShopperDatabase()

    db.connect_to_client()

    parameter_id = "5f23a9311a054568dd434b53"
    query_dict = {"_id": ObjectId(parameter_id)}
    output = db.query(query_dict=query_dict, collection_name="parameters")
    for i in output:
        print(type(i))

