from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import mysql.connector

app = FastAPI()

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "root@123",
    "database": "vatic",
}


conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

templates = Jinja2Templates(directory="templates")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    #Login Authentication
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    user = cursor.fetchone()

    if user:
        return {"message": " login Successful"}
        
    else:
        return templates.TemplateResponse("create_user.html", {"request": request})


@app.post("/create_user")
def create_user(
    full_name: str = Form(...),
    email: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
):
    try:
        query = f"INSERT INTO users (full_name, email, username, password) VALUES ('{full_name}', '{email}', '{username}', '{password}')"
        cursor.execute(query)
        conn.commit()
        print("User created successfully.")
        print("Database status after insertion:")
        cursor.execute("SELECT * FROM users")
        result = cursor.fetchall()
        for row in result:
            print(row)
        return {"message": "User created successfully"}
    except mysql.connector.Error as err:
        print(f"Error creating user: {err}")
        return {"message": f"Error creating user: {err}"}



@app.on_event("shutdown")
def shutdown_event():
    print("FastAPI application shutting down.")
    if conn.is_connected():
        conn.close()
        print("MySQL connection closed.")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
