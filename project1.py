from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Establish the connection
conn = mysql.connector.connect(
    host="172.31.25.230",       # Replace with your MySQL server host
    user="app_user",            # Replace with your MySQL username
    password="2004",        # Replace with your MySQL password
    database="aws"  # Replace with the name of your database
)

@app.route('/')
def home():
    return "Welcome to the Airline Data API!"

@app.get("/airline_data")
def get_airline_data():
    airport_code = request.args.get('Airport_Code')  # Fetch airport code from query parameter
    
    cursor = conn.cursor()

    # SQL query to fetch relevant columns based on the dataset
    query = """
        SELECT *
        FROM air
        WHERE Airport_Code = '%s';
    """
    
    cursor.execute(query, [airport_code])  # Execute the query with the provided airport code

    # Fetch all rows from the executed query
    results = cursor.fetchall()

    # Convert the result to a list of dictionaries for JSON response
    results2 = [dict(zip(cursor.column_names, result)) for result in results]

    cursor.close()

    return jsonify(results2)

@app.route('/airline_data', methods=['POST'])
def add_airline_data():
    if request.is_json:
        data = request.get_json()

        cursor = conn.cursor()
        query = """
            INSERT INTO air (Airport_Code, Airport_Name, Time_Label, Time_Year, Time_Month)
            VALUES (%s, %s, %s, %s, %s)
        """
        
        values = (
            data['Airport_Code'], data['Airport_Name'], data['Time_Label'], 
            data['Time_Year'], data['Time_Month']
        )

        cursor.execute(query, values)
        conn.commit()
        cursor.close()

        return jsonify(data), 201

    return {"error": "Request must be JSON"}, 415

if __name__ == '__main__':
    app.run(debug=True)
