#!/usr/bin/env python3
"""
Test script to demonstrate the enhanced adaptive intelligence features
of the QFox Agent system.
"""

from qfox_core import QFoxController, PREDEFINED_CAPABILITIES, TASK_TEMPLATES
import time
import random

def test_adaptive_intelligence():
    """Test the adaptive intelligence features."""
    print("🧠 Testing QFox Adaptive Intelligence System")
    print("=" * 50)
    
    # Initialize controller
    controller = QFoxController()
    
    # Create agents with different capabilities
    print("\n🤖 Creating agents...")
    agent1_id = controller.add_agent("Data Analyst", ["data_analysis", "visualization", "pattern_recognition"])
    agent2_id = controller.add_agent("ML Engineer", ["machine_learning", "prediction", "classification"])
    agent3_id = controller.add_agent("Optimizer", ["optimization", "resource_management", "decision_making"])
    
    # Display initial confidence scores
    print("\n📊 Initial confidence scores:")
    for agent_id, agent in controller.agents.items():
        print(f"  {agent.name}: {agent.confidence_scores}")
    
    # Create and assign tasks
    print("\n📋 Creating and assigning tasks...")
    
    # Task 1: Data Analysis (should favor Data Analyst)
    task1_id = controller.create_task(
        name="Customer Data Analysis",
        description="Analyze customer behavior patterns",
        required_capabilities=["data_analysis", "pattern_recognition"],
        complexity=6.0,
        priority=8.0,
        estimated_duration=10.0
    )
    
    # Task 2: ML Prediction (should favor ML Engineer)
    task2_id = controller.create_task(
        name="Sales Prediction Model",
        description="Build predictive model for sales forecasting",
        required_capabilities=["machine_learning", "prediction"],
        complexity=8.0,
        priority=9.0,
        estimated_duration=15.0
    )
    
    # Task 3: Resource Optimization (should favor Optimizer)
    task3_id = controller.create_task(
        name="Inventory Optimization",
        description="Optimize inventory levels across warehouses",
        required_capabilities=["optimization", "resource_management"],
        complexity=7.0,
        priority=7.0,
        estimated_duration=12.0
    )
    
    # Assign tasks
    assignments = controller.assign_tasks()
    print(f"  Assigned {len(assignments)} tasks")
    
    # Simulate task execution
    print("\n⚙️ Simulating task execution...")
    controller.start_simulation()
    
    # Process task completions with different outcomes
    print("\n📈 Processing task completions...")
    
    # Task 1: Success for Data Analyst
    controller.process_task_completion(task1_id, True, 8.5)
    
    # Task 2: Success for ML Engineer
    controller.process_task_completion(task2_id, True, 14.0)
    
    # Task 3: Failure for Optimizer (will decrease confidence)
    controller.process_task_completion(task3_id, False, 15.0)
    
    # Create another optimization task to see if confidence affects assignment
    print("\n🔄 Creating another optimization task...")
    task4_id = controller.create_task(
        name="Process Optimization",
        description="Optimize manufacturing processes",
        required_capabilities=["optimization", "decision_making"],
        complexity=6.0,
        priority=6.0,
        estimated_duration=10.0
    )
    
    # Assign the new task
    new_assignments = controller.assign_tasks()
    print(f"  Assigned {len(new_assignments)} new tasks")
    
    # Show updated confidence scores
    print("\n📊 Updated confidence scores after learning:")
    for agent_id, agent in controller.agents.items():
        print(f"  {agent.name}:")
        for capability, confidence in agent.confidence_scores.items():
            print(f"    {capability}: {confidence:.3f}")
    
    # Show success history
    print("\n📈 Success history by capability:")
    for agent_id, agent in controller.agents.items():
        print(f"  {agent.name}:")
        for capability, history in agent.success_history.items():
            if history:
                success_rate = sum(history) / len(history)
                print(f"    {capability}: {history} (rate: {success_rate:.2f})")
    
    # Test agent status retrieval for dashboard
    print("\n🖥️ Agent status for dashboard integration:")
    for agent_id in controller.agents.keys():
        status = controller.get_agent_status(agent_id)
        print(f"  {status['name']}:")
        print(f"    Confidence scores: {status['confidence_scores']}")
        print(f"    Adaptability score: {status['adaptability_score']:.3f}")
        print(f"    Overall score: {status['overall_score']:.3f}")
    
    # Show all agents confidence for dashboard
    print("\n📊 All agents confidence for dashboard:")
    all_confidence = controller.get_all_agents_confidence()
    for agent_id, confidence_scores in all_confidence.items():
        agent_name = controller.agents[agent_id].name
        print(f"  {agent_name}: {confidence_scores}")
    
    print("\n✅ Adaptive intelligence test completed!")

if __name__ == "__main__":
    test_adaptive_intelligence() 