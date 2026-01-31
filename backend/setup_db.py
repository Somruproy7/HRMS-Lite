#!/usr/bin/env python
"""
MongoDB Database Setup Script for HRMS Lite
This script automatically creates the database and collections if MongoDB is installed.
"""

import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# Add the backend directory to Python path
backend_dir = Path(__file__).resolve().parent
sys.path.append(str(backend_dir))

# Load environment variables
load_dotenv()

def check_mongodb_installed():
    """Check if MongoDB is installed and running"""
    try:
        # Try to run mongosh --version (MongoDB Shell)
        result = subprocess.run(['mongosh', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ MongoDB Shell (mongosh) found")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    try:
        # Try to run mongo --version (Legacy MongoDB Shell)
        result = subprocess.run(['mongo', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ MongoDB Legacy Shell (mongo) found")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print("❌ MongoDB not found in system PATH")
    return False

def check_mongodb_running():
    """Check if MongoDB service is running"""
    try:
        import pymongo
        from pymongo import MongoClient
        
        # Get MongoDB URI from environment
        mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/hrms_lite')
        
        # Extract connection details
        if '/hrms_lite' in mongodb_uri:
            base_uri = mongodb_uri.replace('/hrms_lite', '')
        else:
            base_uri = mongodb_uri
            
        client = MongoClient(base_uri, serverSelectionTimeoutMS=5000)
        
        # Test connection
        client.admin.command('ping')
        print("✅ MongoDB service is running")
        return True, client, mongodb_uri
        
    except Exception as e:
        print(f"❌ MongoDB service not running or not accessible: {e}")
        return False, None, None

def create_database_and_collections(client, mongodb_uri):
    """Create database and collections with indexes"""
    try:
        # Extract database name from URI
        db_name = 'hrms_lite'
        if '/' in mongodb_uri:
            db_name = mongodb_uri.split('/')[-1]
        
        db = client[db_name]
        
        print(f"📁 Creating database: {db_name}")
        
        # Create employees collection with indexes
        employees_collection = db['employees']
        
        # Create unique index on employee_id
        employees_collection.create_index("employee_id", unique=True)
        employees_collection.create_index("email")
        print("✅ Created 'employees' collection with indexes")
        
        # Create attendance collection with indexes
        attendance_collection = db['attendance']
        
        # Create compound index for employee + date (for uniqueness)
        attendance_collection.create_index([("employee", 1), ("date", 1)], unique=True)
        attendance_collection.create_index("date")
        attendance_collection.create_index("status")
        print("✅ Created 'attendance' collection with indexes")
        
        # Insert sample data (optional)
        create_sample_data = input("\n🤔 Would you like to create sample data? (y/n): ").lower().strip()
        
        if create_sample_data == 'y':
            insert_sample_data(db)
        
        print(f"\n🎉 Database '{db_name}' setup completed successfully!")
        print(f"📊 Database URL: {mongodb_uri}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return False

def insert_sample_data(db):
    """Insert sample employees and attendance data"""
    try:
        from datetime import datetime, date, timedelta
        
        # Sample employees
        sample_employees = [
            {
                "employee_id": "EMP001",
                "full_name": "John Doe",
                "email": "john.doe@company.com",
                "department": "Engineering",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "employee_id": "EMP002", 
                "full_name": "Jane Smith",
                "email": "jane.smith@company.com",
                "department": "HR",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "employee_id": "EMP003",
                "full_name": "Mike Johnson", 
                "email": "mike.johnson@company.com",
                "department": "Marketing",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
        ]
        
        # Insert employees
        employees_result = db.employees.insert_many(sample_employees)
        print(f"✅ Inserted {len(employees_result.inserted_ids)} sample employees")
        
        # Sample attendance data for the last 5 days
        sample_attendance = []
        today = date.today()
        
        for i in range(5):
            attendance_date = today - timedelta(days=i)
            for emp in sample_employees:
                # Randomly assign Present/Absent (80% Present)
                import random
                status = "Present" if random.random() > 0.2 else "Absent"
                
                sample_attendance.append({
                    "employee": employees_result.inserted_ids[sample_employees.index(emp)],
                    "date": attendance_date,
                    "status": status,
                    "created_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                })
        
        # Insert attendance
        attendance_result = db.attendance.insert_many(sample_attendance)
        print(f"✅ Inserted {len(attendance_result.inserted_ids)} sample attendance records")
        
    except Exception as e:
        print(f"⚠️ Error inserting sample data: {e}")

def main():
    print("🚀 HRMS Lite - MongoDB Database Setup")
    print("=" * 40)
    
    # Check if MongoDB is installed
    if not check_mongodb_installed():
        print("\n📥 Please install MongoDB first:")
        print("   Windows: https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/")
        print("   macOS: brew install mongodb-community")
        print("   Linux: https://docs.mongodb.com/manual/administration/install-on-linux/")
        return False
    
    # Check if MongoDB is running
    is_running, client, mongodb_uri = check_mongodb_running()
    if not is_running:
        print("\n🔧 Please start MongoDB service:")
        print("   Windows: net start MongoDB")
        print("   macOS/Linux: brew services start mongodb-community")
        print("   Or: mongod --dbpath /path/to/data/directory")
        return False
    
    # Create database and collections
    success = create_database_and_collections(client, mongodb_uri)
    
    if success:
        print("\n✅ Setup completed! You can now run:")
        print("   python manage.py runserver")
        print("\n🌐 Your HRMS Lite backend will be available at:")
        print("   http://localhost:8000/api/")
    
    # Close connection
    if client:
        client.close()
    
    return success

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ Setup cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please check your MongoDB installation and try again.")