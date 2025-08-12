#!/usr/bin/env python3
"""
Test script to verify confidence learning is working correctly
"""

from qfox_core import QFoxController

def test_confidence_learning():
    """Test that confidence scores are updated correctly after task completion."""
    print("🧠 Testing Confidence Learning System")
    print("=" * 45)
    
    # Initialize controller
    controller = QFoxController()
    
    # Create a test agent
    print("\n🤖 Creating test agent...")
    agent_id = controller.add_agent("Test Agent", ["data_analysis", "machine_learning"])
    agent = controller.agents[agent_id]
    
    # Show initial confidence
    print(f"\n📊 Initial confidence scores:")
    print(f"  data_analysis: {agent.get_capability_confidence('data_analysis'):.3f}")
    print(f"  machine_learning: {agent.get_capability_confidence('machine_learning'):.3f}")
    
    # Create and assign a task successfully
    print("\n📋 Creating and assigning task (SUCCESS)...")
    task_id = controller.create_task(
        name="Test Data Analysis",
        description="Test task for data analysis",
        required_capabilities=["data_analysis"],
        complexity=5.0,
        priority=5.0,
        estimated_duration=5.0
    )
    
    # Assign the task
    assignments = controller.assign_tasks()
    print(f"  Task assigned: {len(assignments) > 0}")
    
    # Complete the task successfully
    controller.process_task_completion(task_id, True, 4.5)
    
    # Show updated confidence
    print(f"\n📊 Confidence after SUCCESS:")
    print(f"  data_analysis: {agent.get_capability_confidence('data_analysis'):.3f}")
    print(f"  machine_learning: {agent.get_capability_confidence('machine_learning'):.3f}")
    
    # Create and assign another task (failure)
    print("\n📋 Creating and assigning task (FAILURE)...")
    task2_id = controller.create_task(
        name="Test ML Task",
        description="Test task for machine learning",
        required_capabilities=["machine_learning"],
        complexity=5.0,
        priority=5.0,
        estimated_duration=5.0
    )
    
    # Assign the task
    assignments = controller.assign_tasks()
    print(f"  Task assigned: {len(assignments) > 0}")
    
    # Complete the task with failure
    controller.process_task_completion(task2_id, False, 6.0)
    
    # Show final confidence
    print(f"\n📊 Final confidence after FAILURE:")
    print(f"  data_analysis: {agent.get_capability_confidence('data_analysis'):.3f}")
    print(f"  machine_learning: {agent.get_capability_confidence('machine_learning'):.3f}")
    
    # Show success history
    print(f"\n📈 Success history:")
    print(f"  data_analysis: {agent.success_history.get('data_analysis', [])}")
    print(f"  machine_learning: {agent.success_history.get('machine_learning', [])}")
    
    print("\n✅ Confidence learning test completed!")

if __name__ == "__main__":
    test_confidence_learning() 