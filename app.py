from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure SQLite Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///saathi.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Fixed typo in config
db = SQLAlchemy(app)

# Define the Vendor Table Model matching your registration form
class Vendor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    contact_no = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(15), nullable=False)
    address = db.Column(db.Text, nullable=False)
    id_type = db.Column(db.String(50), nullable=False)
    id_proof = db.Column(db.String(100), nullable=False)
    profession = db.Column(db.String(50), nullable=False)
    experience = db.Column(db.String(50), nullable=False)
    pincode = db.Column(db.String(10), nullable=False)

# Automatically create the database file (saathi.db) when the script starts
with app.app_context():
    db.create_all()

# --- ROUTES TO SERVE HTML PAGES ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/customer.html')
def customer_page():
    return render_template('customer.html')

@app.route('/vendorregistration.html')
def vendor_page():
    return render_template('vendorregistration.html')

# --- BACKEND API LOGIC ---

@app.route('/api/register-vendor', methods=['POST'])
def register_vendor():
    try:
        # Extract data submitted from the HTML form
        new_vendor = Vendor(
            full_name=request.form.get('fullName'),
            contact_no=request.form.get('contactNo'),
            email=request.form.get('email'),
            gender=request.form.get('gender'),
            address=request.form.get('address'),
            id_type=request.form.get('idType'),
            id_proof=request.form.get('idProof'),
            profession=request.form.get('profession'),
            experience=request.form.get('experience'),
            pincode=request.form.get('pincode')
        )
        
        # Save records to the database
        db.session.add(new_vendor)
        db.session.commit()
        
        # CHANGED: Now rendering the success.html template instead of returning a string
        return render_template('success.html')
        
    except Exception as e:
        return f"An error occurred during submission: {str(e)}", 400

@app.route('/api/search-vendors', methods=['POST'])
def search_vendors():
    # Receive search criteria securely via JSON
    search_data = request.json
    pincode = search_data.get('pincode')
    profession = search_data.get('profession')
    
    # Query database for matches case-insensitively
    query_results = Vendor.query.filter(
        Vendor.pincode == pincode,
        Vendor.profession.ilike(profession)
    ).all()
    
    # Format the query results to send back to the frontend
    results_list = []
    for vendor in query_results:
        results_list.append({
            "name": vendor.full_name,
            "contact": vendor.contact_no,
            "profession": vendor.profession,
            "experience": f"{vendor.experience} Years"
        })
        
    return jsonify({"status": "success", "vendors": results_list})

if __name__ == '__main__':
    #app.run(debug=True)