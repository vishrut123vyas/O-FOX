import random
import time
import uuid
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
import json
from datetime import datetime, timedelta
from device_simulator import device_manager, DeviceType


class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class AgentStatus(Enum):
    IDLE = "idle"
    BUSY = "busy"
    LEARNING = "learning"
    OPTIMIZING = "optimizing"


@dataclass
class Task:
    """Represents a task with requirements and metadata."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    required_capabilities: List[str] = field(default_factory=list)
    complexity: float = 1.0  # 1.0 to 10.0
    priority: float = 1.0  # 1.0 to 10.0
    estimated_duration: float = 1.0  # minutes
    status: TaskStatus = TaskStatus.PENDING
    assigned_agent: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    actual_duration: Optional[float] = None
    success_score: Optional[float] = None  # 0.0 to 1.0
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'required_capabilities': self.required_capabilities,
            'complexity': self.complexity,
            'priority': self.priority,
            'estimated_duration': self.estimated_duration,
            'status': self.status.value,
            'assigned_agent': self.assigned_agent,
            'created_at': self.created_at.isoformat(),
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'actual_duration': self.actual_duration,
            'success_score': self.success_score
        }


@dataclass
class Agent:
    """Represents an intelligent agent with capabilities and learning system."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    capabilities: List[str] = field(default_factory=list)
    confidence_scores: Dict[str, float] = field(default_factory=dict)  # capability -> confidence (0.0 to 1.0)
    success_history: Dict[str, List[int]] = field(default_factory=dict)  # capability -> list of outcomes (1 or 0)
    performance_history: List[Dict] = field(default_factory=list)
    status: AgentStatus = AgentStatus.IDLE
    current_task: Optional[str] = None
    total_tasks_completed: int = 0
    total_tasks_failed: int = 0
    average_success_rate: float = 0.0
    learning_rate: float = 0.1
    adaptability_score: float = 0.5
    created_at: datetime = field(default_factory=datetime.now)
    last_activity: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        # Initialize confidence scores and success history for all capabilities
        for capability in self.capabilities:
            if capability not in self.confidence_scores:
                self.confidence_scores[capability] = 0.5  # Default confidence = 0.5
            if capability not in self.success_history:
                self.success_history[capability] = []  # Initialize empty success history
    
    def get_capability_confidence(self, capability: str) -> float:
        """Get confidence score for a specific capability."""
        return self.confidence_scores.get(capability, 0.5)  # Default to 0.5 for new capabilities
    
    def get_success_rate(self, capability: str) -> float:
        """Calculate success rate for a specific capability based on recent history."""
        history = self.success_history.get(capability, [])
        if not history:
            return 0.5  # Default success rate
        return sum(history) / len(history)
    
    def update_confidence(self, capability: str, outcome: int):
        """
        Update confidence based on task outcome using the specified learning rule.
        outcome: 1 for success, 0 for failure
        """
        if capability not in self.capabilities:
            return
        
        current_confidence = self.confidence_scores[capability]
        
        # Apply the learning rule: confidence += learning_rate * (outcome - confidence)
        new_confidence = current_confidence + self.learning_rate * (outcome - current_confidence)
        
        # Ensure confidence stays within bounds
        new_confidence = max(0.0, min(1.0, new_confidence))
        
        # Update confidence score
        self.confidence_scores[capability] = new_confidence
        
        # Update success history (maintain only last 10 outcomes)
        if capability not in self.success_history:
            self.success_history[capability] = []
        
        self.success_history[capability].append(outcome)
        
        # Keep only the last 10 outcomes
        if len(self.success_history[capability]) > 10:
            self.success_history[capability] = self.success_history[capability][-10:]
        
        # Update adaptability score based on average confidence
        if self.confidence_scores:
            self.adaptability_score = sum(self.confidence_scores.values()) / len(self.confidence_scores)
    
    def record_performance(self, task_id: str, success: bool, duration: float, complexity: float, capabilities_used: List[str]):
        """Record task performance for learning."""
        performance_record = {
            'task_id': task_id,
            'success': success,
            'duration': duration,
            'complexity': complexity,
            'capabilities': capabilities_used,
            'timestamp': datetime.now().isoformat()
        }
        
        self.performance_history.append(performance_record)
        
        if success:
            self.total_tasks_completed += 1
        else:
            self.total_tasks_failed += 1
        
        # Update average success rate
        total_tasks = self.total_tasks_completed + self.total_tasks_failed
        if total_tasks > 0:
            self.average_success_rate = self.total_tasks_completed / total_tasks
        
        self.last_activity = datetime.now()
    
    def get_overall_score(self) -> float:
        """Calculate overall agent score based on performance and confidence."""
        if not self.capabilities:
            return 0.0
        
        avg_confidence = sum(self.confidence_scores.values()) / len(self.confidence_scores)
        return (self.average_success_rate * 0.6) + (avg_confidence * 0.4)
    
    def get_adaptivity_profile(self) -> Dict:
        """Get comprehensive adaptivity profile for the agent."""
        # Calculate expertise (capabilities with >90% success rate)
        expertise = []
        for capability in self.capabilities:
            success_rate = self.get_success_rate(capability)
            if success_rate > 0.9:
                expertise.append(capability)
        
        # Build history by capability
        history = {}
        for capability in self.capabilities:
            history[capability] = {
                "success": sum(self.success_history.get(capability, [])),
                "fail": len(self.success_history.get(capability, [])) - sum(self.success_history.get(capability, [])),
                "total": len(self.success_history.get(capability, [])),
                "success_rate": self.get_success_rate(capability)
            }
        
        return {
            "capabilities": self.confidence_scores.copy(),
            "success_history": self.success_history.copy(),
            "history": history,
            "expertise": expertise,
            "total_tasks": len(self.performance_history),
            "adaptability_score": self.adaptability_score,
            "learning_rate": self.learning_rate
        }
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'name': self.name,
            'capabilities': self.capabilities,
            'confidence_scores': self.confidence_scores,
            'success_history': self.success_history,
            'status': self.status.value,
            'current_task': self.current_task,
            'total_tasks_completed': self.total_tasks_completed,
            'total_tasks_failed': self.total_tasks_failed,
            'average_success_rate': self.average_success_rate,
            'learning_rate': self.learning_rate,
            'adaptability_score': self.adaptability_score,
            'overall_score': self.get_overall_score(),
            'created_at': self.created_at.isoformat(),
            'last_activity': self.last_activity.isoformat()
        }


class QFoxController:
    """Main controller for intelligent task assignment and system coordination."""
    
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.tasks: Dict[str, Task] = {}
        self.assignment_history: List[Dict] = []
        self.system_metrics: Dict = {
            'total_tasks_created': 0,
            'total_tasks_completed': 0,
            'total_tasks_failed': 0,
            'average_completion_time': 0.0,
            'system_efficiency': 0.0,
            'agent_utilization': 0.0
        }
        self.simulation_active = False
        self.simulation_start_time = None
        self.training_mode = False
        
        # Initialize device manager
        self.device_manager = device_manager
        
    def add_agent(self, name: str, capabilities: List[str]) -> str:
        """Add a new agent to the system."""
        agent = Agent(name=name, capabilities=capabilities)
        self.agents[agent.id] = agent
        return agent.id
    
    def remove_agent(self, agent_id: str) -> bool:
        """Remove an agent from the system."""
        if agent_id in self.agents:
            # Reassign any current task
            agent = self.agents[agent_id]
            if agent.current_task:
                task = self.tasks.get(agent.current_task)
                if task:
                    task.status = TaskStatus.PENDING
                    task.assigned_agent = None
            
            del self.agents[agent_id]
            return True
        return False
    
    def create_task(self, name: str, description: str, required_capabilities: List[str], 
                   complexity: float = 1.0, priority: float = 1.0, 
                   estimated_duration: float = 1.0) -> str:
        """Create a new task."""
        task = Task(
            name=name,
            description=description,
            required_capabilities=required_capabilities,
            complexity=complexity,
            priority=priority,
            estimated_duration=estimated_duration
        )
        self.tasks[task.id] = task
        self.system_metrics['total_tasks_created'] += 1
        return task.id
    
    def remove_task(self, task_id: str) -> bool:
        """Remove a task from the system."""
        if task_id in self.tasks:
            task = self.tasks[task_id]
            if task.assigned_agent:
                agent = self.agents.get(task.assigned_agent)
                if agent:
                    agent.current_task = None
                    agent.status = AgentStatus.IDLE
            
            del self.tasks[task_id]
            return True
        return False
    
    def calculate_agent_score(self, agent: Agent, task: Task) -> float:
        """Calculate weighted score for agent-task assignment using adaptive intelligence."""
        if not agent.capabilities or not task.required_capabilities:
            return 0.0
        
        # 1. Capability Match: 40%
        matching_capabilities = set(agent.capabilities) & set(task.required_capabilities)
        capability_match = len(matching_capabilities) / len(task.required_capabilities)
        
        # 2. Confidence Score: 35%
        confidence_sum = 0.0
        confidence_count = 0
        for capability in task.required_capabilities:
            if capability in agent.capabilities:
                confidence_sum += agent.get_capability_confidence(capability)
                confidence_count += 1
        
        avg_confidence = confidence_sum / confidence_count if confidence_count > 0 else 0.0
        
        # 3. Success Rate: 15%
        success_rate_sum = 0.0
        success_rate_count = 0
        for capability in task.required_capabilities:
            if capability in agent.capabilities:
                success_rate_sum += agent.get_success_rate(capability)
                success_rate_count += 1
        
        avg_success_rate = success_rate_sum / success_rate_count if success_rate_count > 0 else 0.0
        
        # 4. Current Load/Availability: 10%
        load_score = 1.0 if agent.status == AgentStatus.IDLE else 0.3
        
        # Weighted combination as specified
        final_score = (
            capability_match * 0.40 +      # Capability Match: 40%
            avg_confidence * 0.35 +        # Confidence Score: 35%
            avg_success_rate * 0.15 +      # Success Rate: 15%
            load_score * 0.10              # Current Load/Availability: 10%
        )
        
        return final_score
    
    def assign_tasks(self) -> List[Dict]:
        """Intelligently assign pending tasks to available agents."""
        assignments = []
        pending_tasks = [task for task in self.tasks.values() if task.status == TaskStatus.PENDING]
        available_agents = [agent for agent in self.agents.values() if agent.status == AgentStatus.IDLE]
        
        if not pending_tasks or not available_agents:
            return assignments
        
        # Sort tasks by priority (highest first)
        pending_tasks.sort(key=lambda t: t.priority, reverse=True)
        
        for task in pending_tasks:
            best_agent = None
            best_score = 0.0
            
            for agent in available_agents:
                score = self.calculate_agent_score(agent, task)
                if score > best_score:
                    best_score = score
                    best_agent = agent
            
            if best_agent and best_score > 0.1:  # Minimum threshold
                # Assign task
                task.assigned_agent = best_agent.id
                task.status = TaskStatus.IN_PROGRESS
                task.started_at = datetime.now()
                
                best_agent.current_task = task.id
                best_agent.status = AgentStatus.BUSY
                
                assignment_record = {
                    'task_id': task.id,
                    'agent_id': best_agent.id,
                    'score': best_score,
                    'timestamp': datetime.now().isoformat()
                }
                assignments.append(assignment_record)
                self.assignment_history.append(assignment_record)
                
                # Remove assigned agent from available list
                available_agents.remove(best_agent)
        
        return assignments
    
    def process_task_completion(self, task_id: str, success: bool, actual_duration: float):
        """Process task completion and update learning with confidence logging."""
        task = self.tasks.get(task_id)
        if not task or not task.assigned_agent:
            return
        
        agent = self.agents.get(task.assigned_agent)
        if not agent:
            return
        
        # Log confidence before update for each capability
        confidence_before = {}
        for capability in task.required_capabilities:
            if capability in agent.capabilities:
                confidence_before[capability] = agent.get_capability_confidence(capability)
        
        # Update task
        task.status = TaskStatus.COMPLETED if success else TaskStatus.FAILED
        task.completed_at = datetime.now()
        task.actual_duration = actual_duration
        task.success_score = 1.0 if success else 0.0
        
        # Update agent learning
        for capability in task.required_capabilities:
            agent.update_confidence(capability, 1 if success else 0)
        
        # Log confidence after update
        confidence_after = {}
        for capability in task.required_capabilities:
            if capability in agent.capabilities:
                confidence_after[capability] = agent.get_capability_confidence(capability)
        
        # Log confidence changes
        print(f"🤖 Agent '{agent.name}' completed task '{task.name}' ({'SUCCESS' if success else 'FAILED'})")
        for capability in task.required_capabilities:
            if capability in confidence_before and capability in confidence_after:
                before = confidence_before[capability]
                after = confidence_after[capability]
                change = after - before
                change_symbol = "📈" if change > 0 else "📉" if change < 0 else "➡️"
                print(f"   📊 {capability}: {before:.3f} → {after:.3f} ({change_symbol} {change:+.3f})")
        
        # Record performance
        agent.record_performance(task_id, success, actual_duration, task.complexity, task.required_capabilities)
        
        # Reset agent status
        agent.current_task = None
        agent.status = AgentStatus.IDLE
        
        # Update system metrics
        if success:
            self.system_metrics['total_tasks_completed'] += 1
        else:
            self.system_metrics['total_tasks_failed'] += 1
        
        self._update_system_metrics()
    
    def _update_system_metrics(self):
        """Update overall system performance metrics."""
        total_completed = self.system_metrics['total_tasks_completed']
        total_failed = self.system_metrics['total_tasks_failed']
        total_tasks = total_completed + total_failed
        
        if total_tasks > 0:
            self.system_metrics['system_efficiency'] = total_completed / total_tasks
        
        # Calculate agent utilization
        busy_agents = sum(1 for agent in self.agents.values() if agent.status != AgentStatus.IDLE)
        total_agents = len(self.agents)
        if total_agents > 0:
            self.system_metrics['agent_utilization'] = busy_agents / total_agents
    
    def get_system_state(self) -> Dict:
        """Get complete system state for dashboard."""
        return {
            'agents': {aid: agent.to_dict() for aid, agent in self.agents.items()},
            'tasks': {tid: task.to_dict() for tid, task in self.tasks.items()},
            'system_metrics': self.system_metrics,
            'simulation_active': self.simulation_active,
            'simulation_start_time': self.simulation_start_time.isoformat() if self.simulation_start_time else None,
            'training_mode': self.training_mode
        }
    
    def get_agent_status(self, agent_id: str) -> Optional[Dict]:
        """Get detailed agent status including confidence scores for dashboard integration."""
        agent = self.agents.get(agent_id)
        if not agent:
            return None
        
        return {
            'id': agent.id,
            'name': agent.name,
            'status': agent.status.value,
            'current_task': agent.current_task,
            'capabilities': agent.capabilities,
            'confidence_scores': agent.confidence_scores,  # capability -> float
            'success_history': agent.success_history,      # capability -> list of outcomes
            'total_tasks_completed': agent.total_tasks_completed,
            'total_tasks_failed': agent.total_tasks_failed,
            'average_success_rate': agent.average_success_rate,
            'learning_rate': agent.learning_rate,
            'adaptability_score': agent.adaptability_score,
            'overall_score': agent.get_overall_score(),
            'last_activity': agent.last_activity.isoformat()
        }
    
    def get_all_agents_confidence(self) -> Dict[str, Dict[str, float]]:
        """Get confidence scores for all agents, organized by agent -> capability -> confidence."""
        return {
            agent_id: agent.confidence_scores.copy() 
            for agent_id, agent in self.agents.items()
        }
    
    def start_simulation(self):
        """Start the simulation."""
        self.simulation_active = True
        self.simulation_start_time = datetime.now()
    
    def stop_simulation(self):
        """Stop the simulation."""
        self.simulation_active = False
    
    def toggle_training_mode(self):
        """Toggle training mode for faster learning."""
        self.training_mode = not self.training_mode
        # Adjust learning rates for all agents
        for agent in self.agents.values():
            if self.training_mode:
                agent.learning_rate = 0.3  # Faster learning in training mode
            else:
                agent.learning_rate = 0.1  # Normal learning rate
    
    def simulate_task_execution(self):
        """Simulate task execution for active tasks."""
        if not self.simulation_active:
            return
        
        current_time = datetime.now()
        active_tasks = [task for task in self.tasks.values() if task.status == TaskStatus.IN_PROGRESS]
        
        for task in active_tasks:
            if not task.started_at:
                continue
            
            elapsed_time = (current_time - task.started_at).total_seconds() / 60  # minutes
            
            # Simulate completion based on estimated duration
            if elapsed_time >= task.estimated_duration:
                # Determine success based on agent confidence and task complexity
                agent = self.agents.get(task.assigned_agent)
                if agent:
                    avg_confidence = sum(
                        agent.get_capability_confidence(cap) 
                        for cap in task.required_capabilities 
                        if cap in agent.capabilities
                    ) / len(task.required_capabilities)
                    
                    # Success probability based on confidence and complexity
                    success_prob = avg_confidence * (1.0 - task.complexity * 0.1)
                    success = random.random() < success_prob
                    
                    self.process_task_completion(task.id, success, elapsed_time)
    
    # Device Management Methods
    def add_device(self, name: str, device_type: DeviceType, location: Dict[str, float] = None) -> str:
        """Add a new device to the system."""
        return self.device_manager.add_device(name, device_type, location)
    
    def remove_device(self, device_id: str) -> bool:
        """Remove a device from the system."""
        return self.device_manager.remove_device(device_id)
    
    def get_devices_status(self) -> List[Dict]:
        """Get status of all devices."""
        return self.device_manager.get_all_devices_status()
    
    def get_available_devices(self, capability_type: str = None) -> List[Dict]:
        """Get available devices for task assignment."""
        devices = self.device_manager.get_available_devices(capability_type)
        return [device.to_dict() for device in devices]
    
    def assign_task_to_device(self, task_id: str, device_id: str) -> bool:
        """Assign a task to a specific device."""
        return self.device_manager.assign_task_to_device(task_id, device_id)
    
    def assign_task_to_best_device(self, task_id: str, capability_type: str) -> Optional[str]:
        """Assign a task to the best available device for the capability."""
        return self.device_manager.assign_task_to_best_device(task_id, capability_type)
    
    def complete_device_task(self, task_id: str) -> bool:
        """Mark a device task as completed."""
        return self.device_manager.complete_task(task_id)
    
    def get_device_data(self, device_id: str, limit: int = 10) -> List[Dict]:
        """Get recent data from a specific device."""
        data = self.device_manager.get_device_data(device_id, limit)
        return [data_point.__dict__ for data_point in data]
    
    def start_device_simulation(self):
        """Start all device simulators."""
        self.device_manager.start_all_simulators()
    
    def stop_device_simulation(self):
        """Stop all device simulators."""
        self.device_manager.stop_all_simulators()
    
    def create_demo_devices(self):
        """Create demo devices for testing."""
        self.device_manager.create_demo_devices()


# Predefined capabilities and task templates
PREDEFINED_CAPABILITIES = [
    "data_analysis", "machine_learning", "optimization", "visualization",
    "pattern_recognition", "decision_making", "resource_management",
    "communication", "coordination", "problem_solving", "creativity",
    "adaptation", "prediction", "classification", "regression"
]

TASK_TEMPLATES = [
    {
        "name": "Data Pattern Analysis",
        "description": "Analyze complex data patterns and identify correlations",
        "required_capabilities": ["data_analysis", "pattern_recognition"],
        "complexity": 7.0,
        "priority": 8.0,
        "estimated_duration": 15.0
    },
    {
        "name": "Predictive Modeling",
        "description": "Build predictive models using historical data",
        "required_capabilities": ["machine_learning", "prediction"],
        "complexity": 8.0,
        "priority": 9.0,
        "estimated_duration": 20.0
    },
    {
        "name": "Resource Optimization",
        "description": "Optimize resource allocation across multiple parameters",
        "required_capabilities": ["optimization", "resource_management"],
        "complexity": 6.0,
        "priority": 7.0,
        "estimated_duration": 12.0
    },
    {
        "name": "Visual Analytics",
        "description": "Create interactive visualizations for complex datasets",
        "required_capabilities": ["visualization", "data_analysis"],
        "complexity": 5.0,
        "priority": 6.0,
        "estimated_duration": 10.0
    },
    {
        "name": "Adaptive Decision System",
        "description": "Implement adaptive decision-making algorithms",
        "required_capabilities": ["decision_making", "adaptation"],
        "complexity": 9.0,
        "priority": 10.0,
        "estimated_duration": 25.0
    }
] 