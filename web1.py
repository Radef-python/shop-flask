import pandas as pd
from flask import Flask,render_template,request,redirect,jsonify
import os
import sqlite3
radef=Flask(__name__)
def create_db():
    conn = sqlite3.connect("products.db")
    
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
@radef.route("/admin",methods=["GET","POST"])
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
            
        conn=sqlite3.connect("products.db")
        cursor=conn.cursor()
        

        conn.execute("INSERT INTO products(name,price,discount,image,details_images) VALUES (?, ?, ?, ?, ?)",(name,pr,dd,filename,details_images))
        conn.commit()
        conn.close()
        print(name)
        print(pr)
        print(dd)
        print(imag)
        

    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    conn.close()

    return render_template("admin.html",products=products)



    
        
@radef.route("/delete/<int:id>", methods=["POST"])
def delete_product(id):

    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM products WHERE id = ?", (id,))
    

    conn.commit()
    conn.close()
    return redirect("/admin")


@radef.route("/")
def products():

    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

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