#!/usr/bin/env python3
"""
Demonstration of QFox Adaptive Intelligence Evolution
Shows how agent confidence and task assignment preferences change over time.
"""

from qfox_core import QFoxController
import time

def demo_learning_evolution():
    """Demonstrate how adaptive intelligence evolves over multiple iterations."""
    print("🧠 QFox Adaptive Intelligence Evolution Demo")
    print("=" * 60)
    
    # Initialize controller
    controller = QFoxController()
    
    # Create agents with overlapping capabilities
    print("\n🤖 Creating agents with overlapping capabilities...")
    analyst_id = controller.add_agent("Data Analyst", ["data_analysis", "visualization", "pattern_recognition"])
    ml_engineer_id = controller.add_agent("ML Engineer", ["machine_learning", "data_analysis", "prediction"])
    optimizer_id = controller.add_agent("Optimizer", ["optimization", "resource_management", "decision_making"])
    
    # Show initial state
    print("\n📊 Initial confidence scores:")
    for agent_id, agent in controller.agents.items():
        print(f"  {agent.name}: {agent.confidence_scores}")
    
    # Run multiple iterations to show learning evolution
    iterations = 5
    print(f"\n🔄 Running {iterations} learning iterations...")
    
    for iteration in range(iterations):
        print(f"\n--- Iteration {iteration + 1} ---")
        
        # Create a data analysis task (both Data Analyst and ML Engineer can do it)
        task_id = controller.create_task(
            name=f"Data Analysis Task {iteration + 1}",
            description=f"Iteration {iteration + 1} data analysis",
            required_capabilities=["data_analysis"],
            complexity=5.0,
            priority=7.0,
            estimated_duration=8.0
        )
        
        # Assign the task
        assignments = controller.assign_tasks()
        if assignments:
            assignment = assignments[0]
            agent_id = assignment['agent_id']
            agent = controller.agents[agent_id]
            score = assignment['score']
            print(f"  📋 Task assigned to: {agent.name} (score: {score:.3f})")
            
            # Simulate task completion with varying success rates
            # Data Analyst gets better over time, ML Engineer starts strong but plateaus
            if agent.name == "Data Analyst":
                success = iteration >= 2  # Gets better after iteration 2
            elif agent.name == "ML Engineer":
                success = iteration < 3   # Starts strong but declines
            else:
                success = False  # Optimizer shouldn't get data analysis tasks
            
            # Complete the task
            controller.process_task_completion(task_id, success, 7.5)
            
            # Show current confidence scores
            print(f"  📊 Current confidence scores:")
            for aid, a in controller.agents.items():
                if "data_analysis" in a.confidence_scores:
                    conf = a.confidence_scores["data_analysis"]
                    print(f"    {a.name}: {conf:.3f}")
        else:
            print("  ❌ No assignment made")
    
    # Final analysis
    print(f"\n🎯 Final Learning Analysis")
    print("=" * 40)
    
    for agent_id, agent in controller.agents.items():
        print(f"\n🤖 {agent.name}:")
        print(f"  📊 Final confidence scores: {agent.confidence_scores}")
        print(f"  📈 Success history: {agent.success_history}")
        print(f"  🎯 Adaptability score: {agent.adaptability_score:.3f}")
        print(f"  ⭐ Overall score: {agent.get_overall_score():.3f}")
    
    # Show how task assignment preferences changed
    print(f"\n🔄 Task Assignment Evolution Analysis")
    print("=" * 45)
    
    # Create one final task to see assignment preferences
    final_task_id = controller.create_task(
        name="Final Data Analysis Task",
        description="Final test to see assignment preferences",
        required_capabilities=["data_analysis"],
        complexity=5.0,
        priority=8.0,
        estimated_duration=8.0
    )
    
    # Calculate scores for all agents
    final_task = controller.tasks[final_task_id]
    print(f"\n📊 Final task assignment scores:")
    for agent_id, agent in controller.agents.items():
        score = controller.calculate_agent_score(agent, final_task)
        print(f"  {agent.name}: {score:.3f}")
    
    # Assign the final task
    final_assignments = controller.assign_tasks()
    if final_assignments:
        final_assignment = final_assignments[0]
        final_agent = controller.agents[final_assignment['agent_id']]
        print(f"\n🏆 Final task assigned to: {final_agent.name}")
        print(f"   This shows how learning affected task assignment preferences!")
    
    print(f"\n✅ Learning evolution demonstration completed!")
    print(f"   The system has learned from experience and adapted task assignment preferences.")

if __name__ == "__main__":
    demo_learning_evolution() 