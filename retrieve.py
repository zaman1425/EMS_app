from flask import Flask, render_template,request,abort,redirect,url_for
import psycopg2
from psycopg2.extras import DictCursor

app = Flask(__name__)

db_params = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432"
}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search_employee')
def search_emp():
    return render_template('search_emp.html')

@app.route('/success')
def success_page():
    return render_template('success.html')

    
@app.route('/add_emp')
def add_emp():
    return render_template('add_emp.html')


@app.route('/mod_emp',methods=['GET'])
def mod_emp():
    return render_template('mod.html')


@app.route('/srch',methods=['GET'])
def srch():
    emp_no=request.args.get('eno')
    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                sql =" SELECT wrk_no, wrk_name, wrk_age, wrk_job, wrk_salary, wrk_adr FROM workers WHERE wrk_no = %s"
                cursor.execute(sql, (emp_no,))
                employee = cursor.fetchone()

    except psycopg2.OperationalError as e:
        print(f"Database connection error: {e}")
        abort(500)
        
    if employee is None:
        abort(404)
    return render_template('update_employee.html', employee=employee)
    

@app.route('/update_employee',methods=['POST'])
def update_emp():
    emp_update = {
        'eno': request.form.get('update_eno'),
        'ename': request.form.get('ename'),
        'eage': request.form.get('eage'),
        'ejob': request.form.get('ejob'),
        'esalary': request.form.get('esalary'),
        'eadr': request.form.get('eadr')
    }
    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cursor: 
                sql = """UPDATE workers 
                         SET wrk_name = %s, wrk_age = %s, wrk_job = %s, wrk_salary = %s, wrk_adr = %s 
                         WHERE wrk_no = %s"""
                cursor.execute(sql, (
                    emp_update['ename'],
                    emp_update['eage'],
                    emp_update['ejob'],
                    emp_update['esalary'],
                    emp_update['eadr'],
                    emp_update['eno']
                ))
            conn.commit()
            return redirect(url_for('updated')) 
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        return "Database error occurred.", 500
    
@app.route('/updated',methods=['GET'])
def updated():
    return render_template('updated.html')
    

@app.route("/submit_employee", methods=['POST'])
def submit_employee():
    emp_new = {
        'eno': request.form.get('eno'),
        'ename': request.form.get('ename'),
        'eage': request.form.get('eage'),
        'ejob': request.form.get('ejob'),
        'esalary': request.form.get('esalary'),
        'eadr': request.form.get('eadr')
    }
    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cursor: 
                sql = "insert into workers(wrk_no,wrk_name,wrk_age,wrk_job,wrk_salary,wrk_adr) values(%s,%s,%s,%s,%s,%s)"
                cursor.execute(sql, (
                    emp_new['eno'],
                    emp_new['ename'],
                    emp_new['eage'],
                    emp_new['ejob'],
                    emp_new['esalary'],
                    emp_new['eadr']
                ))
            conn.commit()
            return redirect(url_for('success_page'))
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Database error: {e}")
        return "Database error occurred.", 500
    

@app.route("/search_emp", methods=["GET"])
def get_employee():
    emp_no=request.args.get('eno')
    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                sql =" SELECT wrk_no, wrk_name, wrk_age, wrk_job, wrk_salary, wrk_adr FROM workers WHERE wrk_no = %s"
                cursor.execute(sql, (emp_no,))
                employee = cursor.fetchone()

    except psycopg2.OperationalError as e:
        print(f"Database connection error: {e}")
        abort(500)
        
    if employee is None:
        abort(404)
    return render_template('view_emp.html', employe=employee)

@app.route("/exit-page")
def exit_pages():
    return render_template("exit.html")

    

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
