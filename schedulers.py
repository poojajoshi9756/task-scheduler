from models import Task, TaskStatus
from typing import List, Dict, Any
import heapq
from collections import deque

class TaskScheduler:
    """Base class for task scheduling algorithms"""
    
    def __init__(self, tasks: List[Task]):
        self.tasks = tasks
        self.schedule = []
        self.current_time = 0
    
    def generate_schedule(self) -> List[Dict[str, Any]]:
        """Generate the execution schedule for tasks"""
        raise NotImplementedError("Subclasses must implement generate_schedule")
    
    def get_gantt_data(self) -> Dict[str, Any]:
        """Generate data for Gantt chart visualization"""
        schedule = self.generate_schedule()
        
        datasets = []
        labels = []
        
        for i, task_info in enumerate(schedule):
            task = task_info['task']
            start_time = task_info['start_time']
            duration = task_info['duration']
            
            labels.append(task.name)
            
            # Create dataset for this task
            datasets.append({
                'label': task.name,
                'data': [{
                    'x': [start_time, start_time + duration],
                    'y': i,
                    'task_id': task.id,
                    'priority': task.priority,
                    'duration': duration
                }],
                'backgroundColor': self._get_priority_color(task.priority),
                'borderColor': self._get_priority_color(task.priority, True),
                'borderWidth': 2
            })
        
        return {
            'labels': labels,
            'datasets': datasets,
            'total_time': self.current_time,
            'algorithm': self.__class__.__name__
        }
    
    def _get_priority_color(self, priority: int, border: bool = False) -> str:
        """Get color based on priority level"""
        colors = {
            1: '#dc3545' if not border else '#b02a37',  # High priority - Red
            2: '#fd7e14' if not border else '#d63384',  # Medium-High - Orange
            3: '#ffc107' if not border else '#d39e00',  # Medium - Yellow
            4: '#20c997' if not border else '#1aa179',  # Medium-Low - Teal
            5: '#6f42c1' if not border else '#59359a'   # Low priority - Purple
        }
        return colors.get(priority, '#6c757d' if not border else '#545b62')

class PriorityScheduler(TaskScheduler):
    """Priority-based scheduling algorithm"""
    
    def generate_schedule(self) -> List[Dict[str, Any]]:
        # Sort tasks by priority (1 = highest priority)
        sorted_tasks = sorted(self.tasks, key=lambda x: (x.priority, x.created_at))
        
        schedule = []
        current_time = 0
        
        for task in sorted_tasks:
            schedule.append({
                'task': task,
                'start_time': current_time,
                'duration': task.duration,
                'completion_time': current_time + task.duration
            })
            current_time += task.duration
        
        self.current_time = current_time
        return schedule

class FCFSScheduler(TaskScheduler):
    """First Come First Serve scheduling algorithm"""
    
    def generate_schedule(self) -> List[Dict[str, Any]]:
        # Sort tasks by arrival time, then by creation time
        sorted_tasks = sorted(self.tasks, key=lambda x: (x.arrival_time, x.created_at))
        
        schedule = []
        current_time = 0
        
        for task in sorted_tasks:
            # If task arrives later than current time, wait
            if task.arrival_time > current_time:
                current_time = task.arrival_time
            
            schedule.append({
                'task': task,
                'start_time': current_time,
                'duration': task.duration,
                'completion_time': current_time + task.duration
            })
            current_time += task.duration
        
        self.current_time = current_time
        return schedule

class SJFScheduler(TaskScheduler):
    """Shortest Job First scheduling algorithm"""
    
    def generate_schedule(self) -> List[Dict[str, Any]]:
        # Sort tasks by duration (shortest first), then by creation time
        sorted_tasks = sorted(self.tasks, key=lambda x: (x.duration, x.created_at))
        
        schedule = []
        current_time = 0
        
        for task in sorted_tasks:
            schedule.append({
                'task': task,
                'start_time': current_time,
                'duration': task.duration,
                'completion_time': current_time + task.duration
            })
            current_time += task.duration
        
        self.current_time = current_time
        return schedule

class RoundRobinScheduler(TaskScheduler):
    """Round Robin scheduling algorithm"""
    
    def __init__(self, tasks: List[Task], quantum: int = 2):
        super().__init__(tasks)
        self.quantum = quantum
    
    def generate_schedule(self) -> List[Dict[str, Any]]:
        # Create a queue of tasks with remaining time
        task_queue = deque()
        remaining_time = {}
        
        # Initialize remaining time for each task
        for task in self.tasks:
            remaining_time[task.id] = task.duration
            task_queue.append(task)
        
        schedule = []
        current_time = 0
        
        while task_queue:
            task = task_queue.popleft()
            
            # Execute for quantum time or remaining time, whichever is smaller
            execution_time = min(self.quantum, remaining_time[task.id])
            
            schedule.append({
                'task': task,
                'start_time': current_time,
                'duration': execution_time,
                'completion_time': current_time + execution_time,
                'remaining_time': remaining_time[task.id] - execution_time
            })
            
            current_time += execution_time
            remaining_time[task.id] -= execution_time
            
            # If task is not completed, add it back to the queue
            if remaining_time[task.id] > 0:
                task_queue.append(task)
        
        self.current_time = current_time
        return schedule

def get_scheduler(algorithm: str, tasks: List[Task], **kwargs) -> TaskScheduler:
    """Factory function to get appropriate scheduler"""
    schedulers = {
        'priority': PriorityScheduler,
        'fcfs': FCFSScheduler,
        'sjf': SJFScheduler,
        'round_robin': RoundRobinScheduler
    }
    
    scheduler_class = schedulers.get(algorithm, PriorityScheduler)
    
    # Only pass quantum parameter to RoundRobinScheduler
    if algorithm == 'round_robin' and 'quantum' in kwargs:
        return scheduler_class(tasks, quantum=kwargs['quantum'])
    else:
        return scheduler_class(tasks)
