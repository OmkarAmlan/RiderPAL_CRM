from flask import Flask, request
import sqlite3

app = Flask(__name__)

@app.route('/feedback_dump/', methods=['POST'])
def feedback_put():
    payload_dict = request.get_json()
    if not payload_dict:
        return {"error": "Invalid JSON payload"}, 400
    
    order_id = payload_dict.get('order_id')
    feedback = payload_dict.get('feedback')
    rating = payload_dict.get('rating')

    # Open a new connection inside the function
    con = sqlite3.connect("delivery.db", check_same_thread=False)
    cur = con.cursor()
    
    # Ensure table exists
    cur.execute('''
                CREATE TABLE IF NOT EXISTS feedback (
                    order_id TEXT PRIMARY KEY,
                    feedback TEXT,
                    rating INTEGER
                )
                ''')
    
    try:
        cur.execute('''
                    INSERT INTO feedback (order_id, feedback, rating) VALUES (?, ?, ?)
                    ''', (order_id, feedback, rating))
        con.commit()
    except sqlite3.IntegrityError:
        return {"error": "Duplicate order_id. Data not inserted."}, 409  # Handle duplicate primary keys
    
    con.close()  # Close the connection

    return {"message": "Feedback successfully added!"}, 201

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7000)
