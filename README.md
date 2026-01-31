# HRMS Lite - Human Resource Management System

A lightweight Human Resource Management System built with React frontend and Django backend with MongoDB database.

## Features

### Employee Management
- Add new employees with unique Employee ID, Full Name, Email, and Department
- View list of all employees
- Delete employees
- Server-side validation for all fields
- Duplicate employee ID handling

### Attendance Management
- Mark daily attendance for employees (Present/Absent)
- View attendance records with filtering options
- Filter by employee and date
- Prevent duplicate attendance entries for same employee on same date

### Dashboard
- Overview statistics (Total Employees, Attendance Records, Today's Present/Absent count)
- Quick action buttons for common tasks

## Tech Stack

### Frontend
- **React 19.2.4** - UI framework
- **React Router DOM** - Client-side routing
- **Axios** - HTTP client for API calls
- **CSS3** - Custom styling with responsive design

### Backend
- **Django 4.2.7** - Web framework
- **Django REST Framework** - API development
- **MongoDB** - Database (via MongoEngine)
- **django-cors-headers** - CORS handling

## Project Structure

```
hrms-lite/
├── backend/
│   ├── hrms/                 # Django project settings
│   ├── employees/            # Employee app
│   ├── attendance/           # Attendance app
│   ├── requirements.txt      # Python dependencies
│   ├── setup_db.py          # MongoDB setup script
│   └── manage.py            # Django management script
├── frontend/
│   ├── src/
│   │   ├── components/      # Reusable React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API service layer
│   │   └── App.js          # Main App component
│   └── package.json        # Node.js dependencies
├── requirements.txt        # Root Python dependencies (for Railway)
├── railway.toml           # Railway configuration
├── Procfile              # Process definition
└── README.md
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- MongoDB (local or cloud instance)

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
```

3. Activate virtual environment:
```bash
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Setup MongoDB database (automated):

**Option 1: Using setup script (Recommended)**
```bash
python setup_db.py
```

**Option 2: Using Django management command**
```bash
# Setup database with sample data
python manage.py setup_mongodb --sample-data

# Setup database without sample data
python manage.py setup_mongodb
```

6. Start the Django server:
```bash
python manage.py runserver
```

**Note**: The setup scripts will:
- ✅ Check if MongoDB is installed and running
- ✅ Create the database and collections automatically
- ✅ Set up proper indexes for optimal performance
- ✅ Optionally create sample data for testing

The backend API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the React development server:
```bash
npm start
```

The frontend will be available at `http://localhost:3000`

## API Endpoints

### Employees
- `GET /api/employees/` - Get all employees
- `POST /api/employees/` - Create new employee
- `GET /api/employees/{id}/` - Get specific employee
- `DELETE /api/employees/{id}/` - Delete employee

### Attendance
- `GET /api/attendance/` - Get all attendance records (supports filtering)
- `POST /api/attendance/` - Mark attendance
- `GET /api/attendance/summary/{employee_id}/` - Get attendance summary for employee

## Usage

1. **Adding Employees**: Navigate to the Employees page and click "Add Employee" to create new employee records.

2. **Marking Attendance**: Go to the Attendance page and click "Mark Attendance" to record daily attendance.

3. **Viewing Data**: Use the Dashboard for overview statistics, or browse specific pages for detailed views.

4. **Filtering**: Use the filter options on the Attendance page to view records by employee or date.

## Validation & Error Handling

### Frontend Validation
- Required field validation
- Email format validation
- Real-time error display

### Backend Validation
- Unique employee ID constraint
- Email format validation
- Required field validation
- Duplicate attendance prevention

### Error Handling
- Proper HTTP status codes
- Meaningful error messages
- Graceful error display in UI

## Assumptions & Limitations

1. **Single Admin User**: No authentication system implemented as per requirements
2. **Basic CRUD Operations**: Focus on core functionality without advanced features
3. **Date-based Attendance**: One attendance record per employee per day
4. **No Employee Updates**: Employees can only be added or deleted, not modified
5. **Local Development**: Configuration optimized for local development

## Future Enhancements

- Employee profile updates
- Attendance reporting and analytics
- Export functionality
- User authentication and authorization
- Advanced filtering and search
- Bulk operations

## Development Notes

- The application uses MongoDB with djongo for Django-MongoDB integration
- CORS is configured to allow frontend-backend communication
- Responsive design works on desktop and mobile devices
- Error states and loading states are handled throughout the application
