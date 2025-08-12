import random
import time
from enum import Enum

class DeviceType(Enum):
    CPU = "CPU"
    RAM = "RAM"
    DISK = "Disk"
    SENSOR_HUB = "Sensor Hub"


class BaseDevice:
    def __init__(self, name):
        self.name = name
        self.status = "idle"

    def get_status(self):
        return {
            "device": self.name,
            "status": self.status,
            "timestamp": time.time()
        }

class CPUSensor(BaseDevice):
    def __init__(self):
        super().__init__("CPU Sensor")

    def get_data(self):
        self.status = "active"
        return {
            "temperature": round(random.uniform(35, 80), 2),
            "usage_percent": round(random.uniform(5, 95), 2)
        }

class RAMMonitor(BaseDevice):
    def __init__(self):
        super().__init__("RAM Monitor")

    def get_data(self):
        self.status = "active"
        return {
            "used_gb": round(random.uniform(1, 15), 2),
            "available_gb": round(random.uniform(1, 16), 2)
        }

class DiskScanner(BaseDevice):
    def __init__(self):
        super().__init__("Disk Scanner")

    def get_data(self):
        self.status = "active"
        return {
            "disk_used_percent": round(random.uniform(20, 90), 2),
            "disk_read_speed": round(random.uniform(100, 500), 2)  # in MB/s
        }

class SensorHub(BaseDevice):
    def __init__(self):
        super().__init__("Sensor Hub")

    def get_data(self):
        self.status = "active"
        return {
            "temperature": round(random.uniform(15, 35), 2),
            "humidity": round(random.uniform(30, 70), 2),
            "motion_detected": random.choice([True, False])
        }



# Device Manager to hold all devices
class DeviceManager:
    def __init__(self):
        self.devices = {
            DeviceType.CPU: CPUSensor(),
            DeviceType.RAM: RAMMonitor(),
            DeviceType.DISK: DiskScanner(),
            DeviceType.SENSOR_HUB: SensorHub()
        }
        # Add device IDs and metadata
        self.device_metadata = {}
        self._initialize_device_metadata()

    def _initialize_device_metadata(self):
        """Initialize device metadata with IDs and status information."""
        try:
            for device_type, device in self.devices.items():
                device_id = f"{device_type.value.lower()}_{id(device)}"
                self.device_metadata[device_id] = {
                    'device_id': device_id,
                    'name': device.name,
                    'device_type': device_type.value.lower().replace(' ', '_'),
                    'status': 'online',
                    'battery_level': random.uniform(60, 100),
                    'signal_strength': random.uniform(70, 100),
                    'last_data': {},
                    'assigned_task': None,
                    'location': {'x': random.uniform(0, 100), 'y': random.uniform(0, 100)}
                }
        except Exception as e:
            print(f"Error in _initialize_device_metadata: {e}")

    def get_device(self, device_type):
        try:
            return self.devices.get(device_type)
        except Exception as e:
            print(f"Error in get_device: {e}")
            return None

    def get_all_devices(self):
        try:
            return self.devices
        except Exception as e:
            print(f"Error in get_all_devices: {e}")
            return {}

    def get_all_devices_status(self):
        """Get status of all devices for dashboard display."""
        try:
            status_list = []
            for device_id, metadata in self.device_metadata.items():
                # Get the device object using the original DeviceType enum
                device_type_enum = None
                for dt in DeviceType:
                    if dt.value.lower().replace(' ', '_') == metadata['device_type']:
                        device_type_enum = dt
                        break
                
                if device_type_enum and device_type_enum in self.devices:
                    device = self.devices[device_type_enum]
                    # Update status based on device activity
                    if hasattr(device, 'status'):
                        metadata['status'] = device.status
                    
                    # Generate some simulated data
                    try:
                        data = device.get_data()
                        metadata['last_data'] = data
                    except Exception as e:
                        print(f"Error getting data from device {device_id}: {e}")
                        metadata['last_data'] = {}
                    
                    # Simulate battery and signal changes
                    metadata['battery_level'] = max(0, metadata['battery_level'] - random.uniform(0, 0.1))
                    metadata['signal_strength'] = max(0, metadata['signal_strength'] + random.uniform(-0.5, 0.5))
                    
                    status_list.append(metadata.copy())
            
            return status_list
        except Exception as e:
            print(f"Error in get_all_devices_status: {e}")
            return []

    def get_available_devices(self, capability_type: str = None):
        """Get available devices for task assignment."""
        try:
            available_devices = []
            for device_id, metadata in self.device_metadata.items():
                if metadata['status'] == 'online' and metadata['assigned_task'] is None:
                    if capability_type is None or capability_type.lower() in metadata['device_type'].lower():
                        available_devices.append(metadata)
            return available_devices
        except Exception as e:
            print(f"Error in get_available_devices: {e}")
            return []

    def assign_task_to_device(self, task_id: str, device_id: str) -> bool:
        """Assign a task to a specific device."""
        try:
            if device_id in self.device_metadata:
                self.device_metadata[device_id]['assigned_task'] = task_id
                self.device_metadata[device_id]['status'] = 'busy'
                return True
            return False
        except Exception as e:
            print(f"Error in assign_task_to_device: {e}")
            return False

    def assign_task_to_best_device(self, task_id: str, capability_type: str) -> str:
        """Assign a task to the best available device for the capability."""
        try:
            available_devices = self.get_available_devices(capability_type)
            if available_devices:
                # Simple selection: pick the first available device
                best_device = available_devices[0]
                self.assign_task_to_device(task_id, best_device['device_id'])
                return best_device['device_id']
            return None
        except Exception as e:
            print(f"Error in assign_task_to_best_device: {e}")
            return None

    def complete_task(self, task_id: str) -> bool:
        """Mark a device task as completed."""
        try:
            for device_id, metadata in self.device_metadata.items():
                if metadata['assigned_task'] == task_id:
                    metadata['assigned_task'] = None
                    metadata['status'] = 'online'
                    return True
            return False
        except Exception as e:
            print(f"Error in complete_task: {e}")
            return False

    def get_device_data(self, device_id: str, limit: int = 10) -> list:
        """Get recent data from a specific device."""
        try:
            if device_id in self.device_metadata:
                device_type_str = self.device_metadata[device_id]['device_type']
                
                # Find the matching DeviceType enum
                device_type_enum = None
                for dt in DeviceType:
                    if dt.value.lower().replace(' ', '_') == device_type_str:
                        device_type_enum = dt
                        break
                
                if device_type_enum and device_type_enum in self.devices:
                    device = self.devices[device_type_enum]
                    try:
                        data = device.get_data()
                        return [{'value': str(v), 'unit': '', 'timestamp': time.time()} for v in data.values()]
                    except Exception as e:
                        print(f"Error getting data from device {device_id}: {e}")
                        return []
            return []
        except Exception as e:
            print(f"Error in get_device_data: {e}")
            return []

    def create_demo_devices(self):
        """Initializes demo devices with simulated startup behavior."""
        try:
            for device_type, device in self.devices.items():
                print(f"[DeviceManager] Initializing {device_type.value}...")
                # Optionally, simulate startup data
                try:
                    device.get_status()
                    device.get_data()
                except Exception as e:
                    print(f"[DeviceManager] Error initializing {device_type.value}: {e}")
            print("[DeviceManager] All demo devices initialized.")
        except Exception as e:
            print(f"[DeviceManager] Error in create_demo_devices: {e}")

    def start_all_simulators(self):
        """Starts simulation for all devices if they have a start method."""
        try:
            for device_type, device in self.devices.items():
                if hasattr(device, "start"):
                    try:
                        device.start()
                        print(f"[DeviceManager] Started simulation for {device_type.value}.")
                    except Exception as e:
                        print(f"[DeviceManager] Failed to start {device_type.value}: {e}")
                else:
                    print(f"[DeviceManager] {device_type.value} has no start method.")
        except Exception as e:
            print(f"[DeviceManager] Error in start_all_simulators: {e}")

    def stop_all_simulators(self):
        """Stop all device simulators."""
        try:
            for device_type, device in self.devices.items():
                if hasattr(device, "stop"):
                    try:
                        device.stop()
                        print(f"[DeviceManager] Stopped simulation for {device_type.value}.")
                    except Exception as e:
                        print(f"[DeviceManager] Failed to stop {device_type.value}: {e}")
        except Exception as e:
            print(f"[DeviceManager] Error in stop_all_simulators: {e}")


# Create a global instance
device_manager = DeviceManager()
