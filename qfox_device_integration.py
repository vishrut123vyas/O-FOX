# qfox_device_integration.py

from qfox_core import assign_tasks, agents
from device_simulator import DeviceManager

# Initialize Device Manager
device_manager = DeviceManager()

# Add sample devices
device_manager.add_device("ThermalSensor-A1", ["temperature_reading"])
device_manager.add_device("GeoTracker-B2", ["location_tracking"])
device_manager.add_device("PowerNode-C3", ["power_status"])

# Sample task queue
tasks = [
    {"task_id": 101, "description": "Monitor room temperature", "type": "temperature_reading"},
    {"task_id": 102, "description": "Track shipment location", "type": "location_tracking"},
    {"task_id": 103, "description": "Check battery status", "type": "power_status"},
    {"task_id": 104, "description": "Optimize algorithm", "type": "model_optimization"},
]

# Assign tasks to agents or devices
def smart_assign(tasks):
    for task in tasks:
        assigned = False
        # Try assigning to an agent
        for agent in agents:
            if task['type'] in agent.capabilities and agent.status == 'idle':
                agent.assign_task(task)
                print(f"Assigned to Agent: {agent.name} -> {task['description']}")
                assigned = True
                break
        # If not assigned to agent, try a device
        if not assigned:
            if device_manager.assign_task_to_device(task):
                print(f"Assigned to Device -> {task['description']}")
            else:
                print(f"No match found for task: {task['description']}")

# Simulate assignment
if __name__ == '__main__':
    smart_assign(tasks)
    print("\n[Devices]")
    for device in device_manager.get_devices():
        print(device)
        print("---")
