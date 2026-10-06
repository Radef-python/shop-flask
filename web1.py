import pandas as pd
from flask import Flask,render_template,request,redirect,jsonify
import os
import sqlite3
import libs_client
radef=Flask(__name__)
touso_url=os.environ.get("TURSO_URL","libsql://shop-db-radef-python.aws-eu-west-1.turso.io")
touso_token=os.environ.get("TURSO_AUTH_TOKEN","eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJhIjoicnciLCJpYXQiOjE3OTEyOTE4NTQsImlkIjoiMDFhMTExNGUtMzAwMS03NGI0LTkxNzQtNWJhZDcwNDg2NGYwIiwia2lkIjoiaGlyeTY2RmRnaXhOWkZHemNNc1NCS0dyX29aVEl5WHVYbTRlbVZfb1lJWSIsInJpZCI6ImU3N2ZmMzgxLTk5OTYtNDAwYS1iMTE5LWFkOGI3YjU4ZWM0NiJ9.pFek0KAP2bl7cn1YADU8SNdkneaj7mkEeYngYtbCSMnY5dHmQg01z4umC2yGgMLXJ8wr_GcPCblzyCPFGe3pDQ")
def create_db():
    conn = libs_client.connect(url=touso_url,auth_token=touso_token)
    
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price REAL,
            discount REAL,
            image TEXT,
            details_images TEXT
        )
    """)
    cursor.execute("PRAGMA table_info(products)")
    
   
    conn.commit()
    conn.close()
@radef.route("/admin.11",methods=["GET","POST"])
def home():
    
    
    # df=pd.read_excel(os.path.join(os.path.dirname(__file__),"oo.xlsx"))
    # data=df.to_dict(orient="records")
    if request.method=="POST":
        name=request.form["name"]
        pr=request.form["price"]
        dd=request.form["discount"]
        imag=request.files["image"]
        filename=imag.filename

        imag.save("static/photos/" + filename)
        detail_files = request.files.getlist("details_images")

        detail_filenames = []

        for file in detail_files:
            if file and file.filename:
                filename = file.filename
                file.save("static/photos/" + filename)
                detail_filenames.append(filename)

        details_images = ",".join(detail_filenames)
            
        conn=libs_client.connect(url=touso_url,auth_token=touso_token)
        # cursor=conn.cursor()
        

        conn.execute("INSERT INTO products(name,price,discount,image,details_images) VALUES (?, ?, ?, ?, ?)",(name,pr,dd,filename,details_images))
        # conn.commit()
        conn.close()
        print(name)
        print(pr)
        print(dd)
        print(imag)
        

    # conn = sqlite3.connect("products.db")
    conn=libs_client.connect(url=touso_url,auth_token=touso_token)

    # cursor = conn.cursor()

    result=conn.execute("SELECT * FROM products")
    products = result.rows

    conn.close()

    return render_template("admin.html",products=products)



    
        
@radef.route("/delete/<int:id>", methods=["POST"])
def delete_product(id):

    # conn = sqlite3.connect("products.db")
    conn=libs_client.connect(url=touso_url,auth_token=touso_token)

    # cursor = conn.cursor()

    conn.execute("DELETE FROM products WHERE id = ?", (id,))
    

    # conn.commit()
    conn.close()
    return redirect("/admin.11")


@radef.route("/")
def products():

    # conn = sqlite3.connect("products.db")
    conn=libs_client.connect(url=touso_url,auth_token=touso_token)

    # cursor = conn.cursor()

    result=conn.execute("SELECT * FROM products")
    products = result.rows

    conn.close()

    return render_template("web1.html", products=products)
@radef.route("/product/<int:id>")
def product_details(id):

    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products WHERE id = ?", (id,))

    product = cursor.fetchone()
   
    details_images=product[5].split(",") if product[5] else[]

    conn.close()

    return render_template("details.html", product=product,details_images=details_images)




  
create_db()

if __name__=="__main__":
    radef.run(debug=True)
