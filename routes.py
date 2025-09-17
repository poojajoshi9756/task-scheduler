from flask import render_template, request, jsonify, redirect, url_for, flash
from app import app, db
from models import Task, TaskStatus
from schedulers import get_scheduler
import logging

@app.route('/')
def index():
    """Main page with task management interface"""
    return render_template('index.html')

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks"""
    try:
        tasks = Task.query.all()
        return jsonify({
            'success': True,
            'tasks': [task.to_dict() for task in tasks]
        })
    except Exception as e:
        logging.error(f"Error fetching tasks: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch tasks'
        }), 500

@app.route('/api/tasks', methods=['POST'])
def create_task():
    """Create a new task"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or not data.get('name'):
            return jsonify({
                'success': False,
                'error': 'Task name is required'
            }), 400
        
        task = Task(
            name=data['name'],
            priority=int(data.get('priority', 1)),
            duration=int(data.get('duration', 1)),
            arrival_time=int(data.get('arrival_time', 0))
        )
        
        db.session.add(task)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'task': task.to_dict(),
            'message': 'Task created successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error creating task: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to create task'
        }), 500

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update an existing task"""
    try:
        task = Task.query.get_or_404(task_id)
        data = request.get_json()
        
        if data.get('name'):
            task.name = data['name']
        if data.get('priority'):
            task.priority = int(data['priority'])
        if data.get('duration'):
            task.duration = int(data['duration'])
        if data.get('arrival_time') is not None:
            task.arrival_time = int(data['arrival_time'])
        if data.get('status'):
            task.status = TaskStatus(data['status'])
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'task': task.to_dict(),
            'message': 'Task updated successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error updating task: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to update task'
        }), 500

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task"""
    try:
        task = Task.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Task deleted successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error deleting task: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to delete task'
        }), 500

@app.route('/api/schedule/<algorithm>')
def get_schedule(algorithm):
    """Get task schedule for a specific algorithm"""
    try:
        # Get only pending tasks for scheduling
        tasks = Task.query.filter_by(status=TaskStatus.PENDING).all()
        
        if not tasks:
            return jsonify({
                'success': True,
                'gantt_data': {
                    'labels': [],
                    'datasets': [],
                    'total_time': 0,
                    'algorithm': algorithm
                },
                'message': 'No pending tasks to schedule'
            })
        
        # Get scheduler parameters from query string
        quantum = int(request.args.get('quantum', 2))
        
        # Create scheduler and generate schedule
        scheduler = get_scheduler(algorithm, tasks, quantum=quantum)
        gantt_data = scheduler.get_gantt_data()
        
        return jsonify({
            'success': True,
            'gantt_data': gantt_data
        })
        
    except Exception as e:
        logging.error(f"Error generating schedule: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Failed to generate schedule: {str(e)}'
        }), 500

@app.route('/api/execute-next/<algorithm>')
def execute_next_task(algorithm):
    """Execute the next task according to the algorithm"""
    try:
        tasks = Task.query.filter_by(status=TaskStatus.PENDING).all()
        
        if not tasks:
            return jsonify({
                'success': False,
                'error': 'No pending tasks to execute'
            })
        
        # Get the next task to execute based on algorithm
        scheduler = get_scheduler(algorithm, tasks)
        schedule = scheduler.generate_schedule()
        
        if not schedule:
            return jsonify({
                'success': False,
                'error': 'No tasks in schedule'
            })
        
        # Get the first task in the schedule
        next_task_info = schedule[0]
        next_task = next_task_info['task']
        
        # Update task status to executing
        next_task.status = TaskStatus.EXECUTING
        next_task.start_time = next_task_info['start_time']
        db.session.commit()
        
        return jsonify({
            'success': True,
            'task': next_task.to_dict(),
            'message': f'Executing task: {next_task.name}'
        })
        
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error executing task: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to execute task'
        }), 500

@app.route('/api/complete-task/<int:task_id>')
def complete_task(task_id):
    """Mark a task as completed"""
    try:
        task = Task.query.get_or_404(task_id)
        task.status = TaskStatus.COMPLETED
        # Set completion time if not already set
        if task.start_time is not None and task.completion_time is None:
            task.completion_time = task.start_time + task.duration
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'task': task.to_dict(),
            'message': f'Task {task.name} completed successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error completing task: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to complete task'
        }), 500

@app.route('/api/reset-tasks')
def reset_tasks():
    """Reset all tasks to pending status"""
    try:
        tasks = Task.query.all()
        for task in tasks:
            task.status = TaskStatus.PENDING
            task.start_time = None
            task.completion_time = None
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'All tasks reset to pending status'
        })
        
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error resetting tasks: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to reset tasks'
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Resource not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500
