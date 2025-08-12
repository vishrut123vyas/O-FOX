#!/usr/bin/env python3
"""
Test script to verify the agent confidence table functionality
"""

from qfox_core import QFoxController
import time

def test_confidence_table():
    """Test the confidence table functionality."""
    print("🧠 Testing Agent Confidence Table")
    print("=" * 40)
    
    # Initialize controller
    controller = QFoxController()
    
    # Create test agents with different capabilities
    print("\n🤖 Creating test agents...")
    agent1_id = controller.add_agent("Data Analyst", ["data_analysis", "visualization", "pattern_recognition"])
    agent2_id = controller.add_agent("ML Engineer", ["machine_learning", "prediction", "classification"])
    agent3_id = controller.add_agent("Optimizer", ["optimization", "resource_management", "decision_making"])
    
    # Create some tasks and simulate completion to update confidence scores
    print("\n📋 Creating and completing tasks...")
    
    # Task 1: Data Analysis (success for Data Analyst)
    task1_id = controller.create_task(
        name="Customer Data Analysis",
        description="Analyze customer behavior patterns",
        required_capabilities=["data_analysis", "pattern_recognition"],
        complexity=6.0,
        priority=8.0,
        estimated_duration=10.0
    )
    controller.process_task_completion(task1_id, True, 8.5)
    
    # Task 2: ML Prediction (success for ML Engineer)
    task2_id = controller.create_task(
        name="Sales Prediction Model",
        description="Build predictive model for sales forecasting",
        required_capabilities=["machine_learning", "prediction"],
        complexity=8.0,
        priority=9.0,
        estimated_duration=15.0
    )
    controller.process_task_completion(task2_id, True, 14.0)
    
    # Task 3: Resource Optimization (failure for Optimizer)
    task3_id = controller.create_task(
        name="Inventory Optimization",
        description="Optimize inventory levels across warehouses",
        required_capabilities=["optimization", "resource_management"],
        complexity=7.0,
        priority=7.0,
        estimated_duration=12.0
    )
    controller.process_task_completion(task3_id, False, 15.0)
    
    # Test the get_agent_status function
    print("\n📊 Testing agent status retrieval...")
    for agent_id in controller.agents.keys():
        status = controller.get_agent_status(agent_id)
        print(f"\n  {status['name']}:")
        print(f"    Confidence scores: {status['confidence_scores']}")
        print(f"    Success history: {status['success_history']}")
    
    # Test the get_all_agents_confidence function
    print("\n📊 Testing bulk confidence retrieval...")
    all_confidence = controller.get_all_agents_confidence()
    for agent_id, confidence_scores in all_confidence.items():
        agent_name = controller.agents[agent_id].name
        print(f"  {agent_name}: {confidence_scores}")
    
    print("\n✅ Confidence table test completed!")
    print("   The dashboard should now display the confidence table with color-coded scores.")

if __name__ == "__main__":
    test_confidence_table() 