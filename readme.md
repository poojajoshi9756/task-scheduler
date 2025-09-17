# Task Scheduling System

## Overview

This is a Flask-based web application that implements various CPU task scheduling algorithms with visual representation through Gantt charts. The system allows users to create tasks with different priorities, durations, and arrival times, then visualize how different scheduling algorithms would execute these tasks.

## System Architecture

### Backend Architecture
- **Framework**: Flask (Python 3.11)
- **Database**: SQLAlchemy ORM with SQLite (default) or PostgreSQL support
- **Web Server**: Gunicorn for production deployment
- **Session Management**: Flask sessions with configurable secret key

### Frontend Architecture
- **UI Framework**: Bootstrap 5 with dark theme
- **Charts**: Chart.js for Gantt chart visualization
- **Icons**: Font Awesome
- **JavaScript**: Vanilla JavaScript with class-based architecture

### Database Schema
- **Task Model**: Core entity with fields for scheduling algorithms
  - `id`: Primary key
  - `name`: Task identifier
  - `priority`: Integer priority (1 = highest)
  - `duration`: Execution time in time units
  - `arrival_time`: When task arrives in system
  - `status`: Enum (PENDING, EXECUTING, COMPLETED)
  - `start_time`: Execution start time
  - `completion_time`: Execution end time
  - `created_at`: Timestamp

## Key Components

### Models (`models.py`)
- **Task**: Main entity representing schedulable tasks
- **TaskStatus**: Enum for task states
- Uses SQLAlchemy with declarative base pattern

### Schedulers (`schedulers.py`)
- **TaskScheduler**: Base class for scheduling algorithms
- Implements multiple scheduling algorithms (incomplete in current code)
- Generates Gantt chart data for visualization
- Calculates scheduling metrics

### Routes (`routes.py`)
- **REST API**: JSON endpoints for task management
- **Web Interface**: Template rendering for main interface
- **Error Handling**: Try-catch blocks with proper HTTP status codes

### Frontend JavaScript
- **TaskSchedulerApp** (`app.js`): Main application controller
- **GanttChart** (`gantt.js`): Chart visualization management
- Event-driven architecture with form handling

## Data Flow

1. **Task Creation**: User submits task form → API validation → Database storage
2. **Schedule Generation**: Algorithm selection → Task retrieval → Schedule calculation
3. **Visualization**: Schedule data → Chart.js rendering → Gantt chart display
4. **Task Management**: CRUD operations through REST API endpoints

## External Dependencies

### Python Packages
- `flask`: Web framework
- `flask-sqlalchemy`: Database ORM
- `gunicorn`: WSGI HTTP server
- `psycopg2-binary`: PostgreSQL adapter
- `email-validator`: Input validation
- `werkzeug`: WSGI utilities

### Frontend Libraries
- Bootstrap 5: UI components and styling
- Chart.js: Data visualization
- Font Awesome: Icon library
- Chart.js date adapter: Time-based charts

## Deployment Strategy

### Development
- Flask development server with hot reload
- SQLite database for local development
- Debug mode enabled

### Production
- Gunicorn WSGI server with auto-scaling
- PostgreSQL database support
- ProxyFix middleware for reverse proxy compatibility
- Environment-based configuration


## User Preferences

Preferred communication style: Simple, everyday language.