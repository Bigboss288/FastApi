from fastapi import FastAPI
from pymongo.mongo_client import MongoClient
from pydantic import BaseModel
from bson import ObjectId

app = FastAPI()

uri = "mongodb+srv://ayan:Bigboss_288@cluster0.geyruxz.mongodb.net/?retryWrites=true&w=majority"


try:
    #client.admin.command('ping')
    client = MongoClient(uri)
    mydb = client["test"]
    productcol = mydb["productInfo"]
    print("db connection successful")
except Exception as e:
    print(e)



class Product(BaseModel):
    name:str
    price:float
    quantity:int

@app.get('/welcome')
def welcome():
    return {"message" : "Welcome user"}

@app.get("/allproduct")
def getAllProduct():
     array = []
     for item in productcol.find():
        item['_id'] = str(item['_id'])  # Convert ObjectId to string
        array.append(item)

     return array
    
    
@app.get("/product/{id}")
def getProduct(id:str):
    try:
        product_id_obj = ObjectId(id)
        product = productcol.find_one({"_id": product_id_obj})
        if product:
            product['_id'] = str(product['_id'])
            return product
        else:
            return {"message": "Product not found."}
    except Exception as e:
        return {"error": str(e)}


@app.post("/product")
def saveProduct(product:Product):
    productJson = {
        "name" : product.name,
        "price" : product.price,
        "quantity" : product.quantity
    }
    productcol.insert_one(productJson)
    return "Product saved"


@app.delete("/product/{id}")
def deleteProduct(id:str):
    try:
       product_id_obj = ObjectId(id)
       prod = productcol.find_one({"_id" : product_id_obj})
       if prod:
            productcol.delete_one({"_id" : product_id_obj})
            return f"product with id: {id} deleted"
       else:
           return f"Product with id:{id} does not exist"
    except Exception as e:
        return {"error" : str(e)}


@app.put("/product/update/{id}")
def updateProduct(id:str, product:Product):
    try:
        product_id_obj = ObjectId(id)
        updated_product = {
             "name" : product.name,
             "price" : product.price,
             "quantity" : product.quantity
            }
        prod = productcol.find_one({"_id" : product_id_obj})

        if prod:
            result = productcol.update_one({"_id": product_id_obj}, {"$set": updated_product})
            if result.modified_count == 1:
                return "Product details Updated"
            else:
                return "Product details up to date"
            
        else:
            return "Product not found"
    except Exception as e:
        return {"Error" : str(e)}
   
    
   