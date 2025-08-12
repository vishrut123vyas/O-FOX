#!/usr/bin/env python3
"""
Q-FOX Device & Sensor Simulation Demo Task Scenario
==================================================

This demo showcases the multitasking capabilities of Q-FOX with a network of
smart devices and sensors working together in real-time.

Scenario: Smart City IoT Network Management
- Multiple devices sending live data
- Q-FOX agents assigning, processing, and learning from tasks
- Real-time coordination and optimization
"""

import time
import random
import threading
from datetime import datetime, timedelta
from qfox_core import QFoxController
from device_simulator import DeviceType, device_manager

class DemoScenario:
    """Manages the demo scenario with devices, agents, and tasks."""
    
    def __init__(self):
        self.controller = QFoxController()
        self.scenario_active = False
        self.scenario_thread = None
        
    def setup_scenario(self):
        """Initialize the demo scenario with devices, agents, and tasks."""
        print("🚀 Setting up Q-FOX Smart City IoT Demo Scenario...")
        
        # Create demo devices
        print("📡 Creating IoT device network...")
        self.controller.create_demo_devices()
        
        # Create specialized agents for IoT management
        print("🤖 Creating specialized IoT agents...")
        self.create_iot_agents()
        
        # Create IoT-specific tasks
        print("📋 Creating IoT management tasks...")
        self.create_iot_tasks()
        
        # Start device simulation
        print("⚡ Starting device simulation...")
        self.controller.start_device_simulation()
        
        print("✅ Demo scenario setup complete!")
        print(f"   - {len(self.controller.device_manager.devices)} devices active")
        print(f"   - {len(self.controller.agents)} agents ready")
        print(f"   - {len(self.controller.tasks)} tasks queued")
    
    def create_iot_agents(self):
        """Create specialized agents for IoT device management."""
        iot_agents = [
            {
                "name": "IoT Data Analyst",
                "capabilities": ["data_analysis", "pattern_recognition", "temperature", "humidity", "pressure"]
            },
            {
                "name": "Location Tracker",
                "capabilities": ["location", "motion", "data_analysis", "pattern_recognition"]
            },
            {
                "name": "Power Manager",
                "capabilities": ["power", "resource_management", "optimization", "decision_making"]
            },
            {
                "name": "Security Monitor",
                "capabilities": ["camera", "motion", "pattern_recognition", "decision_making"]
            },
            {
                "name": "System Controller",
                "capabilities": ["controller", "actuator", "optimization", "coordination"]
            }
        ]
        
        for agent_data in iot_agents:
            self.controller.add_agent(agent_data["name"], agent_data["capabilities"])
    
    def create_iot_tasks(self):
        """Create IoT-specific tasks that utilize device capabilities."""
        iot_tasks = [
            {
                "name": "Environmental Monitoring",
                "description": "Monitor temperature, humidity, and pressure across the city",
                "required_capabilities": ["temperature", "humidity", "pressure", "data_analysis"],
                "complexity": 6.0,
                "priority": 8.0,
                "estimated_duration": 12.0
            },
            {
                "name": "Traffic Pattern Analysis",
                "description": "Analyze GPS and motion data for traffic optimization",
                "required_capabilities": ["location", "motion", "pattern_recognition"],
                "complexity": 7.0,
                "priority": 9.0,
                "estimated_duration": 15.0
            },
            {
                "name": "Battery Optimization",
                "description": "Optimize power consumption across all IoT devices",
                "required_capabilities": ["power", "optimization", "resource_management"],
                "complexity": 8.0,
                "priority": 7.0,
                "estimated_duration": 18.0
            },
            {
                "name": "Security Surveillance",
                "description": "Monitor security cameras and motion sensors",
                "required_capabilities": ["camera", "motion", "pattern_recognition"],
                "complexity": 7.0,
                "priority": 10.0,
                "estimated_duration": 20.0
            },
            {
                "name": "Climate Control",
                "description": "Control HVAC systems based on environmental data",
                "required_capabilities": ["controller", "actuator", "temperature", "humidity"],
                "complexity": 6.0,
                "priority": 8.0,
                "estimated_duration": 14.0
            }
        ]
        
        for task_data in iot_tasks:
            self.controller.create_task(
                name=task_data["name"],
                description=task_data["description"],
                required_capabilities=task_data["required_capabilities"],
                complexity=task_data["complexity"],
                priority=task_data["priority"],
                estimated_duration=task_data["estimated_duration"]
            )
    
    def start_scenario(self):
        """Start the demo scenario with continuous task generation."""
        if self.scenario_active:
            return
        
        self.scenario_active = True
        self.scenario_thread = threading.Thread(target=self._scenario_loop, daemon=True)
        self.scenario_thread.start()
        
        print("🎯 Demo scenario started! Generating dynamic tasks...")
    
    def stop_scenario(self):
        """Stop the demo scenario."""
        self.scenario_active = False
        if self.scenario_thread:
            self.scenario_thread.join(timeout=2.0)
        print("🛑 Demo scenario stopped.")
    
    def _scenario_loop(self):
        """Main scenario loop that generates dynamic tasks."""
        task_counter = 0
        
        while self.scenario_active:
            try:
                # Generate new tasks periodically
                if task_counter % 10 == 0:  # Every 30 seconds (10 * 3s interval)
                    self._generate_dynamic_task()
                
                # Simulate task execution
                self.controller.simulate_task_execution()
                
                # Assign tasks to agents and devices
                assignments = self.controller.assign_tasks()
                
                # Assign device-specific tasks
                self._assign_device_tasks()
                
                # Update system metrics
                self.controller._update_system_metrics()
                
                task_counter += 1
                time.sleep(3)  # 3-second intervals
                
            except Exception as e:
                print(f"Error in scenario loop: {e}")
                time.sleep(3)
    
    def _generate_dynamic_task(self):
        """Generate a dynamic task based on current system state."""
        task_templates = [
            {
                "name": "Emergency Response",
                "description": "Coordinate emergency response using all available sensors",
                "required_capabilities": ["location", "camera", "motion", "decision_making"],
                "complexity": 9.0,
                "priority": 10.0,
                "estimated_duration": 25.0
            },
            {
                "name": "Energy Conservation",
                "description": "Implement energy conservation measures across the network",
                "required_capabilities": ["power", "optimization", "controller"],
                "complexity": 7.0,
                "priority": 8.0,
                "estimated_duration": 16.0
            },
            {
                "name": "Predictive Maintenance",
                "description": "Predict and schedule maintenance for IoT devices",
                "required_capabilities": ["data_analysis", "pattern_recognition", "prediction"],
                "complexity": 8.0,
                "priority": 7.0,
                "estimated_duration": 22.0
            }
        ]
        
        template = random.choice(task_templates)
        self.controller.create_task(
            name=f"{template['name']} #{random.randint(1000, 9999)}",
            description=template["description"],
            required_capabilities=template["required_capabilities"],
            complexity=template["complexity"],
            priority=template["priority"],
            estimated_duration=template["estimated_duration"]
        )
    
    def _assign_device_tasks(self):
        """Assign tasks to available devices based on their capabilities."""
        available_tasks = [task for task in self.controller.tasks.values() 
                          if task.status.value == "pending"]
        
        for task in available_tasks:
            # Try to assign to devices first
            for capability in task.required_capabilities:
                device_id = self.controller.assign_task_to_best_device(task.id, capability)
                if device_id:
                    print(f"📱 Assigned task '{task.name}' to device {device_id[:8]}...")
                    break
    
    def get_scenario_status(self):
        """Get current status of the demo scenario."""
        devices = self.controller.get_devices_status()
        agents = list(self.controller.agents.values())
        tasks = list(self.controller.tasks.values())
        
        return {
            "devices": {
                "total": len(devices),
                "online": sum(1 for d in devices if d['status'] == 'online'),
                "busy": sum(1 for d in devices if d['status'] == 'busy'),
                "offline": sum(1 for d in devices if d['status'] == 'offline')
            },
            "agents": {
                "total": len(agents),
                "idle": sum(1 for a in agents if a.status.value == 'idle'),
                "busy": sum(1 for a in agents if a.status.value == 'busy')
            },
            "tasks": {
                "total": len(tasks),
                "pending": sum(1 for t in tasks if t.status.value == 'pending'),
                "in_progress": sum(1 for t in tasks if t.status.value == 'in_progress'),
                "completed": sum(1 for t in tasks if t.status.value == 'completed')
            }
        }
    
    def print_status_report(self):
        """Print a detailed status report."""
        status = self.get_scenario_status()
        
        print("\n" + "="*60)
        print("📊 Q-FOX Smart City IoT Demo Status Report")
        print("="*60)
        
        print(f"\n📡 IoT Device Network:")
        print(f"   Total Devices: {status['devices']['total']}")
        print(f"   Online: {status['devices']['online']} (🟢)")
        print(f"   Busy: {status['devices']['busy']} (🟡)")
        print(f"   Offline: {status['devices']['offline']} (🔴)")
        
        print(f"\n🤖 Intelligent Agents:")
        print(f"   Total Agents: {status['agents']['total']}")
        print(f"   Idle: {status['agents']['idle']} (⚪)")
        print(f"   Busy: {status['agents']['busy']} (🟣)")
        
        print(f"\n📋 Task Queue:")
        print(f"   Total Tasks: {status['tasks']['total']}")
        print(f"   Pending: {status['tasks']['pending']} (⏳)")
        print(f"   In Progress: {status['tasks']['in_progress']} (🔄)")
        print(f"   Completed: {status['tasks']['completed']} (✅)")
        
        print("\n" + "="*60)


def run_demo():
    """Run the complete demo scenario."""
    print("🎭 Q-FOX Device & Sensor Simulation Demo")
    print("=" * 50)
    
    # Create and setup scenario
    demo = DemoScenario()
    demo.setup_scenario()
    
    # Start the scenario
    demo.start_scenario()
    
    try:
        # Run for 2 minutes with status updates
        for i in range(40):  # 40 * 3s = 120s = 2 minutes
            time.sleep(3)
            
            if i % 10 == 0:  # Every 30 seconds
                demo.print_status_report()
        
        # Final status report
        demo.print_status_report()
        
    except KeyboardInterrupt:
        print("\n⏹️  Demo interrupted by user")
    finally:
        demo.stop_scenario()
        print("🏁 Demo completed!")


if __name__ == "__main__":
    run_demo() 