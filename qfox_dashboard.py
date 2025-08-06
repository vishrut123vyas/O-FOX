import dash
from dash import dcc, html, Input, Output, State, dash_table
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import threading
import time

from qfox_core import QFoxController, PREDEFINED_CAPABILITIES, TASK_TEMPLATES

# Initialize controller and demo agents
controller = QFoxController()

def create_demo_agents():
    demo_agents = [
        {"name": "Quantum Analyst", "capabilities": ["data_analysis", "pattern_recognition", "visualization"]},
        {"name": "ML Optimizer", "capabilities": ["machine_learning", "optimization", "prediction"]},
        {"name": "Adaptive Coordinator", "capabilities": ["decision_making", "adaptation", "coordination"]},
        {"name": "Resource Manager", "capabilities": ["resource_management", "optimization", "problem_solving"]}
    ]
    for agent_data in demo_agents:
        controller.add_agent(agent_data["name"], agent_data["capabilities"])

create_demo_agents()

# Add some demo tasks to make confidence scores more interesting
def create_demo_tasks():
    demo_tasks = [
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
        }
    ]
    
    for task_data in demo_tasks:
        controller.create_task(
            name=task_data["name"],
            description=task_data["description"],
            required_capabilities=task_data["required_capabilities"],
            complexity=task_data["complexity"],
            priority=task_data["priority"],
            estimated_duration=task_data["estimated_duration"]
        )

create_demo_tasks()

# Initialize Dash app
app = dash.Dash(__name__, 
                external_stylesheets=['https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap'],
                suppress_callback_exceptions=True)
server = app.server

app.title = "Q-FOX - Quantum-inspired Framework for Optimized eXecution"

# Global simulation variables
simulation_thread = None
stop_simulation = False

# Performance data for live stats
agent_names = ['Quantum Analyst', 'ML Optimizer', 'Adaptive Coordinator', 'Resource Manager']
performance_data = {
    agent: {'tasks_completed': [], 'confidence': []} for agent in agent_names
}

# Confidence trends history storage
confidence_history = {}  # agent_name -> capability -> list of confidence values

def run_simulation():
    global stop_simulation
    while not stop_simulation:
        if controller.simulation_active:
            controller.simulate_task_execution()
            controller.assign_tasks()
        time.sleep(2)

def start_simulation_thread():
    global simulation_thread, stop_simulation
    stop_simulation = False
    simulation_thread = threading.Thread(target=run_simulation, daemon=True)
    simulation_thread.start()

def stop_simulation_thread():
    global stop_simulation
    stop_simulation = True
    if simulation_thread:
        simulation_thread.join(timeout=1)

# App layout
app.layout = html.Div([
    # Background
    html.Div(id="particles-bg"),
    
    # Main container
    html.Div([
        # Header
        html.Div([
            html.H1("Q-FOX", className="main-title"),
            html.P("Quantum-inspired Framework for Optimized eXecution", className="subtitle"),
            html.Div([
                html.Span("SIMULATION STATUS: ", className="status-label"),
                html.Span(id="simulation-status", className="status-indicator")
            ], className="status-container"),
            html.Div(id="status-display", className="status-display")
        ], className="header"),
        
        # Navigation dots
        html.Div([
            html.Div(className="nav-dot active", id="nav-dot-1"),
            html.Div(className="nav-dot", id="nav-dot-2"),
            html.Div(className="nav-dot", id="nav-dot-3"),
            html.Div(className="nav-dot", id="nav-dot-4"),
            html.Div(className="nav-dot", id="nav-dot-5")
        ], className="navigation-dots"),
        
        # Slides container
        html.Div([
            # Slide 1: Welcome
            html.Div([
                html.Div([
                    html.H2("Welcome to Q-FOX", className="slide-title"),
                    html.P("Experience the future of intelligent agent coordination.", className="slide-description"),
                    
                    html.Div([
                        html.Div([
                            html.H3("System Overview", className="card-title"),
                            html.Div([
                                html.Div([
                                    html.Span(id="total-agents", className="metric-value"),
                                    html.Span("Active Agents", className="metric-label")
                                ], className="metric-item"),
                                html.Div([
                                    html.Span(id="total-tasks", className="metric-value"),
                                    html.Span("Total Tasks", className="metric-label")
                                ], className="metric-item"),
                                html.Div([
                                    html.Span(id="system-efficiency", className="metric-value"),
                                    html.Span("Efficiency", className="metric-label")
                                ], className="metric-item")
                            ], className="metrics-grid")
                        ], className="glass-card"),
                        
                                                 html.Div([
                             html.H3("Quick Actions", className="card-title"),
                             html.Div([
                                 html.Button("Start Simulation", id="start-sim-btn", className="glow-button primary"),
                                 html.Button("Stop Simulation", id="stop-sim-btn", className="glow-button secondary"),
                                 html.Button("Add Demo Tasks", id="add-demo-tasks-btn", className="glow-button accent"),
                                 html.Div([
                                     html.Label("Training Mode", className="toggle-label"),
                                     dcc.Checklist(
                                         id="training-mode-toggle",
                                         options=[{"label": "", "value": "enabled"}],
                                         value=[],
                                         className="toggle-switch"
                                     )
                                 ], className="toggle-container")
                             ], className="button-group")
                         ], className="glass-card")
                    ], className="welcome-cards")
                ], className="slide-content")
            ], className="slide active", id="slide-1"),
            
            # Slide 2: Agent Overview
            html.Div([
                html.Div([
                    html.H2("Agent Intelligence Matrix", className="slide-title"),
                    
                    html.Div([
                        html.Div([
                            html.H3("Agent Management", className="card-title"),
                            html.Div([
                                dcc.Input(id="agent-name-input", placeholder="Agent Name", className="input-field"),
                                dcc.Dropdown(
                                    id="agent-capabilities-dropdown",
                                    options=[{"label": cap.replace("_", " ").title(), "value": cap} for cap in PREDEFINED_CAPABILITIES],
                                    multi=True,
                                    placeholder="Select Capabilities",
                                    className="dropdown-field"
                                ),
                                html.Button("Add Agent", id="add-agent-btn", className="glow-button primary")
                            ], className="form-group")
                        ], className="glass-card"),
                        
                                                 html.Div([
                             html.H3("Agent Performance", className="card-title"),
                             dcc.Graph(id="agent-performance-chart", className="chart-container")
                         ], className="glass-card"),
                         
                         html.Div([
                             html.H3("Agent Confidence Levels", className="card-title"),
                             html.Div(id="agent-confidence-container", className="confidence-container")
                         ], className="glass-card"),
                         
                         html.Div([
                             html.H3("Agent Confidence Table", className="card-title"),
                                                           dash_table.DataTable(
                                  id="agent-confidence-table",
                                  columns=[],
                                  data=[],
                                  style_cell={
                                      "textAlign": "center",
                                      "fontFamily": "Segoe UI, sans-serif",
                                      "fontSize": "14px",
                                      "padding": "8px",
                                      "color": "#ffffff",
                                      "backgroundColor": "rgba(0,0,0,0.2)",
                                      "backdropFilter": "blur(8px)"
                                  },
                                  style_header={
                                      "backgroundColor": "#141e30",
                                      "color": "#ffffff",
                                      "fontWeight": "bold",
                                      "fontSize": "16px"
                                  },
                                  style_table={
                                      "maxHeight": "60vh",
                                      "overflowY": "auto",
                                      "margin": "20px auto",
                                      "width": "95%",
                                      "borderRadius": "12px",
                                      "boxShadow": "0 4px 12px rgba(0,0,0,0.2)",
                                      "backgroundColor": "transparent"
                                  },
                                  style_data_conditional=[
                                      {
                                          "if": {"row_index": "odd"},
                                          "backgroundColor": "rgba(255,255,255,0.05)"
                                      },
                                      {
                                          "if": {"row_index": "even"},
                                          "backgroundColor": "rgba(255,255,255,0.02)"
                                      },
                                      {
                                          "if": {"column_id": "success_rate"},
                                          "color": "#00ffab",
                                          "fontWeight": "bold"
                                      },
                                      {
                                          "if": {"state": "active"},
                                          "backgroundColor": "rgba(0, 255, 255, 0.15)",
                                          "color": "#000000"
                                      }
                                  ],
                                  page_size=10,
                                  sort_action='native',
                                  filter_action='native',
                                  sort_mode='multi'
                              )
                         ], className="glass-card wide"),
                         
                         html.Div([
                             html.H3("Success/Failure Analysis", className="card-title"),
                             dcc.Graph(id="agent-success-failure-chart", className="chart-container")
                         ], className="glass-card wide")
                    ], className="agent-section")
                ], className="slide-content")
            ], className="slide", id="slide-2"),
            
            # Slide 3: Task Assignment
            html.Div([
                html.Div([
                    html.H2("Dynamic Task Assignment", className="slide-title"),
                    
                    html.Div([
                        html.Div([
                            html.H3("Task Creation", className="card-title"),
                            html.Div([
                                dcc.Input(id="task-name-input", placeholder="Task Name", className="input-field"),
                                dcc.Textarea(id="task-description-input", placeholder="Task Description", className="textarea-field"),
                                dcc.Dropdown(
                                    id="task-capabilities-dropdown",
                                    options=[{"label": cap.replace("_", " ").title(), "value": cap} for cap in PREDEFINED_CAPABILITIES],
                                    multi=True,
                                    placeholder="Required Capabilities",
                                    className="dropdown-field"
                                ),
                                html.Div([
                                    html.Label("Complexity:"),
                                    dcc.Slider(id="task-complexity-slider", min=1, max=10, step=1, value=5)
                                ], className="slider-group"),
                                html.Div([
                                    html.Label("Priority:"),
                                    dcc.Slider(id="task-priority-slider", min=1, max=10, step=1, value=5)
                                ], className="slider-group"),
                                html.Div([
                                    html.Label("Duration (minutes):"),
                                    dcc.Slider(id="task-duration-slider", min=1, max=60, step=1, value=10)
                                ], className="slider-group"),
                                html.Button("Create Task", id="create-task-btn", className="glow-button primary")
                            ], className="form-group")
                        ], className="glass-card"),
                        
                                                 html.Div([
                             html.H3("Active Tasks", className="card-title"),
                             html.Div(id="active-tasks-container", className="tasks-grid")
                         ], className="glass-card"),
                         
                         html.Div([
                             html.H3("Agent Expertise", className="card-title"),
                             html.Div(id="agent-expertise-container", className="expertise-container")
                         ], className="glass-card")
                    ], className="task-section")
                ], className="slide-content")
            ], className="slide", id="slide-3"),
            
            # Slide 4: Performance Analytics
            html.Div([
                html.Div([
                    html.H2("Performance Analytics", className="slide-title"),
                    
                    html.Div([
                        html.Div([
                            html.H3("System Metrics", className="card-title"),
                            html.Div([
                                html.Div([
                                    html.Span(id="completion-rate", className="metric-value"),
                                    html.Span("Completion Rate", className="metric-label")
                                ], className="metric-item"),
                                html.Div([
                                    html.Span(id="avg-completion-time", className="metric-value"),
                                    html.Span("Avg. Completion Time", className="metric-label")
                                ], className="metric-item"),
                                html.Div([
                                    html.Span(id="agent-utilization", className="metric-value"),
                                    html.Span("Agent Utilization", className="metric-label")
                                ], className="metric-item")
                            ], className="metrics-grid")
                        ], className="glass-card"),
                        
                        html.Div([
                            html.H3("Performance Trends", className="card-title"),
                            dcc.Graph(id="performance-trends-chart", className="chart-container")
                        ], className="glass-card wide"),
                        
                        html.Div([
                            html.H3("Live Agent Performance", className="card-title"),
                            dcc.Graph(id="performance-data", className="chart-container")
                        ], className="glass-card wide")
                    ], className="analytics-section")
                ], className="slide-content")
            ], className="slide", id="slide-4"),
            
            # Slide 5: Intelligence Matrix
            html.Div([
                html.Div([
                    html.H2("Real-Time Intelligence Matrix", className="slide-title"),
                    
                    html.Div([
                        html.Div([
                            html.H3("Agent Confidence Matrix", className="card-title"),
                            dcc.Graph(id="confidence-matrix-chart", className="chart-container")
                        ], className="glass-card"),
                        
                        html.Div([
                            html.H3("Confidence Trends Over Time", className="card-title"),
                            dcc.Graph(id="confidence-trend-graph", className="chart-container")
                        ], className="glass-card"),
                        
                        html.Div([
                            html.H3("System Intelligence", className="card-title"),
                            html.Div(id="intelligence-metrics", className="intelligence-grid")
                        ], className="glass-card")
                    ], className="intelligence-section")
                ], className="slide-content")
            ], className="slide", id="slide-5")
        ], className="slides-container")
    ], className="main-container"),
    
    # Hidden divs and interval
    dcc.Store(id="current-slide", data=1),
    dcc.Interval(id="update-interval", interval=3000, n_intervals=0)  # 3 second updates
], className="app-container")

# Callbacks
@app.callback(
    [Output("simulation-status", "children"),
     Output("simulation-status", "className"),
     Output("status-display", "children")],
    [Input("update-interval", "n_intervals")]
)
def update_simulation_status(n):
    if controller.simulation_active:
        status_text = f"System running since {controller.simulation_start_time.strftime('%H:%M:%S') if controller.simulation_start_time else 'N/A'}"
        return "ACTIVE", "status-indicator active", status_text
    else:
        return "INACTIVE", "status-indicator inactive", "System ready for simulation"

@app.callback(
    [Output("total-agents", "children"),
     Output("total-tasks", "children"),
     Output("system-efficiency", "children")],
    [Input("update-interval", "n_intervals")]
)
def update_system_overview(n):
    total_agents = len(controller.agents)
    total_tasks = len(controller.tasks)
    efficiency = f"{controller.system_metrics['system_efficiency']:.1%}"
    return total_agents, total_tasks, efficiency

@app.callback(
    Output("agent-performance-chart", "figure"),
    [Input("update-interval", "n_intervals")]
)
def update_agent_performance_chart(n):
    try:
        if not controller.agents:
            return go.Figure()
        
        agents_data = []
        for agent in controller.agents.values():
            try:
                agents_data.append({
                    'name': agent.name,
                    'success_rate': getattr(agent, 'average_success_rate', 0.0),
                    'overall_score': agent.get_overall_score() if hasattr(agent, 'get_overall_score') else 0.0,
                    'adaptability': getattr(agent, 'adaptability_score', 0.0),
                    'tasks_completed': getattr(agent, 'total_tasks_completed', 0)
                })
            except Exception as e:
                print(f"Error processing agent {agent.name}: {e}")
                continue
        
        if not agents_data:
            return go.Figure()
        
        df = pd.DataFrame(agents_data)
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Success Rate', 'Overall Score', 'Adaptability', 'Tasks Completed'),
            specs=[[{"type": "bar"}, {"type": "bar"}],
                   [{"type": "bar"}, {"type": "bar"}]]
        )
        
        fig.add_trace(
            go.Bar(x=df['name'], y=df['success_rate'], name='Success Rate', marker_color='#00d4ff'),
            row=1, col=1
        )
        fig.add_trace(
            go.Bar(x=df['name'], y=df['overall_score'], name='Overall Score', marker_color='#ff6b6b'),
            row=1, col=2
        )
        fig.add_trace(
            go.Bar(x=df['name'], y=df['adaptability'], name='Adaptability', marker_color='#4ecdc4'),
            row=2, col=1
        )
        fig.add_trace(
            go.Bar(x=df['name'], y=df['tasks_completed'], name='Tasks Completed', marker_color='#45b7d1'),
            row=2, col=2
        )
        
        fig.update_layout(
            height=400,
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        return fig
        
    except Exception as e:
        print(f"Error in agent performance chart callback: {e}")
        return go.Figure()

@app.callback(
    Output("active-tasks-container", "children"),
    [Input("update-interval", "n_intervals")]
)
def update_active_tasks(n):
    try:
        tasks = []
        for task in controller.tasks.values():
            try:
                status_color = {
                    'pending': '#ffa726',
                    'in_progress': '#42a5f5',
                    'completed': '#66bb6a',
                    'failed': '#ef5350'
                }.get(task.status.value, '#757575')
                
                assigned_agent = "Unassigned"
                if task.assigned_agent:
                    agent = controller.agents.get(task.assigned_agent)
                    if agent:
                        assigned_agent = agent.name
                
                # Find matching agents for this task
                matching_agents = []
                for agent in controller.agents.values():
                    if any(cap in agent.capabilities for cap in task.required_capabilities):
                        match_score = len(set(agent.capabilities) & set(task.required_capabilities)) / len(task.required_capabilities)
                        matching_agents.append({
                            'name': agent.name,
                            'score': match_score,
                            'is_expert': any(cap in agent.get_adaptivity_profile()["expertise"] for cap in task.required_capabilities)
                        })
                
                # Sort by match score and expertise
                matching_agents.sort(key=lambda x: (x['is_expert'], x['score']), reverse=True)
                
                capability_tags = [
                    html.Span(
                        cap.replace("_", " ").title(),
                        className="capability-tag",
                        style={"background": "#00d4ff" if any(agent['name'] == assigned_agent and agent['is_expert'] for agent in matching_agents) else "#ffa726"}
                    ) for cap in task.required_capabilities
                ]
                
                matching_agents_display = []
                for agent in matching_agents[:3]:  # Show top 3 matches
                    agent_class = "matching-agent expert" if agent['is_expert'] else "matching-agent"
                    matching_agents_display.append(
                        html.Span(
                            f"{agent['name']} ({agent['score']:.0%})",
                            className=agent_class
                        )
                    )
                
                task_card = html.Div([
                    html.H4(task.name, className="task-name"),
                    html.P(task.description, className="task-description"),
                    html.Div(capability_tags, className="capability-tags"),
                    html.Div([
                        html.Span(f"Status: {task.status.value.replace('_', ' ').title()}", 
                                 className="task-status", style={"color": status_color}),
                        html.Span(f"Agent: {assigned_agent}", className="task-agent"),
                        html.Span(f"Priority: {task.priority}", className="task-priority")
                    ], className="task-meta"),
                    html.Div([
                        html.Span("Matching Agents: ", className="matching-label"),
                        html.Div(matching_agents_display, className="matching-agents")
                    ], className="matching-section")
                ], className="task-card")
                
                tasks.append(task_card)
            except Exception as e:
                print(f"Error processing task {task.name}: {e}")
                continue
        
        return tasks
        
    except Exception as e:
        print(f"Error in active tasks callback: {e}")
        return []

@app.callback(
    Output("performance-trends-chart", "figure"),
    [Input("update-interval", "n_intervals")]
)
def update_performance_trends(n):
    timestamps = pd.date_range(start=datetime.now() - timedelta(hours=2), 
                              end=datetime.now(), freq='5min')
    
    efficiency_data = [0.7 + 0.2 * np.sin(i/10) + 0.1 * np.random.random() for i in range(len(timestamps))]
    utilization_data = [0.6 + 0.3 * np.cos(i/8) + 0.1 * np.random.random() for i in range(len(timestamps))]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=timestamps,
        y=efficiency_data,
        mode='lines+markers',
        name='System Efficiency',
        line=dict(color='#00d4ff', width=3),
        marker=dict(size=6)
    ))
    
    fig.add_trace(go.Scatter(
        x=timestamps,
        y=utilization_data,
        mode='lines+markers',
        name='Agent Utilization',
        line=dict(color='#ff6b6b', width=3),
        marker=dict(size=6)
    ))
    
    fig.update_layout(
        height=300,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        legend=dict(font=dict(color='white')),
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
    )
    
    return fig

@app.callback(
    Output("confidence-matrix-chart", "figure"),
    [Input("update-interval", "n_intervals")]
)
def update_confidence_matrix(n):
    try:
        if not controller.agents:
            return go.Figure()
        
        # Get all unique capabilities from agents
        all_capabilities = set()
        for agent in controller.agents.values():
            if hasattr(agent, 'capabilities') and agent.capabilities:
                all_capabilities.update(agent.capabilities)
        
        # If no capabilities, return empty figure
        if not all_capabilities:
            return go.Figure()
        
        capabilities_list = sorted(list(all_capabilities))
        agent_names = [agent.name for agent in controller.agents.values()]
        
        # Build confidence matrix
        confidence_matrix = []
        for agent in controller.agents.values():
            row = []
            for capability in capabilities_list:
                try:
                    confidence = agent.get_capability_confidence(capability)
                    row.append(confidence)
                except:
                    row.append(0.0)  # Default confidence if error
            confidence_matrix.append(row)
        
        # Ensure we have valid data
        if not confidence_matrix or not capabilities_list or not agent_names:
            return go.Figure()
        
        fig = go.Figure(data=go.Heatmap(
            z=confidence_matrix,
            x=[cap.replace('_', ' ').title() for cap in capabilities_list],
            y=agent_names,
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Confidence")
        ))
        
        fig.update_layout(
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        return fig
        
    except Exception as e:
        print(f"Error in confidence matrix callback: {e}")
        return go.Figure()

@app.callback(
    Output("intelligence-metrics", "children"),
    [Input("update-interval", "n_intervals")]
)
def update_intelligence_metrics(n):
    try:
        if not controller.agents:
            return []
        
        # Calculate average confidence
        confidence_values = []
        for agent in controller.agents.values():
            if hasattr(agent, 'confidence_scores') and agent.confidence_scores:
                try:
                    avg_agent_confidence = np.mean(list(agent.confidence_scores.values()))
                    confidence_values.append(avg_agent_confidence)
                except:
                    confidence_values.append(0.0)
        
        avg_confidence = np.mean(confidence_values) if confidence_values else 0.0
        
        # Calculate average adaptability
        adaptability_values = []
        for agent in controller.agents.values():
            if hasattr(agent, 'adaptability_score'):
                adaptability_values.append(agent.adaptability_score)
        
        avg_adaptability = np.mean(adaptability_values) if adaptability_values else 0.0
        
        # Calculate total learning events
        total_learning_events = 0
        for agent in controller.agents.values():
            if hasattr(agent, 'performance_history'):
                total_learning_events += len(agent.performance_history)
        
        # Calculate system intelligence
        system_intelligence = (avg_confidence * 0.4 + avg_adaptability * 0.4 + 
                              min(1.0, total_learning_events / 100) * 0.2)
        
        metrics = [
            html.Div([
                html.Span(f"{avg_confidence:.1%}", className="intelligence-value"),
                html.Span("Average Confidence", className="intelligence-label")
            ], className="intelligence-item"),
            html.Div([
                html.Span(f"{avg_adaptability:.1%}", className="intelligence-value"),
                html.Span("Average Adaptability", className="intelligence-label")
            ], className="intelligence-item"),
            html.Div([
                html.Span(f"{total_learning_events}", className="intelligence-value"),
                html.Span("Learning Events", className="intelligence-label")
            ], className="intelligence-item"),
            html.Div([
                html.Span(f"{system_intelligence:.1%}", className="intelligence-value"),
                html.Span("System Intelligence", className="intelligence-label")
            ], className="intelligence-item")
        ]
        
        return metrics
        
    except Exception as e:
        print(f"Error in intelligence metrics callback: {e}")
        return []

@app.callback(
    Output("agent-confidence-container", "children"),
    [Input("update-interval", "n_intervals")]
)
def update_agent_confidence_levels(n):
    try:
        if not controller.agents:
            return []
        
        confidence_cards = []
        for agent in controller.agents.values():
            profile = agent.get_adaptivity_profile()
            
            capability_bars = []
            for capability, confidence in profile["capabilities"].items():
                bar_color = "#00d4ff" if confidence > 0.8 else "#ff6b6b" if confidence < 0.4 else "#ffa726"
                capability_bars.append(
                    html.Div([
                        html.Span(capability.replace("_", " ").title(), className="capability-name"),
                        html.Div([
                            html.Div(
                                style={
                                    "width": f"{confidence * 100}%",
                                    "height": "8px",
                                    "background": bar_color,
                                    "borderRadius": "4px",
                                    "transition": "width 0.3s ease"
                                }
                            )
                        ], className="progress-bar-container"),
                        html.Span(f"{confidence:.1%}", className="confidence-value")
                    ], className="capability-bar")
                )
            
            confidence_cards.append(
                html.Div([
                    html.H4(agent.name, className="agent-name"),
                    html.Div(capability_bars, className="capabilities-list")
                ], className="agent-confidence-card")
            )
        
        return confidence_cards
        
    except Exception as e:
        print(f"Error in agent confidence callback: {e}")
        return []

@app.callback(
    [Output("agent-confidence-table", "columns"),
     Output("agent-confidence-table", "data")],
    [Input("update-interval", "n_intervals")]
)
def update_agent_confidence_table(n):
    try:
        if not controller.agents:
            return [], []
        
        # Create columns with the new structure
        columns = [
            {"name": "Agent ID", "id": "agent_id"},
            {"name": "Name", "id": "name"},
            {"name": "Status", "id": "status"},
            {"name": "Tasks Completed", "id": "tasks_completed"},
            {"name": "Success Rate (%)", "id": "success_rate"},
            {"name": "Confidence Scores", "id": "confidence"}
        ]
        
        # Create data rows
        data = []
        for agent in controller.agents.values():
            # Calculate success rate
            total_tasks = agent.total_tasks_completed + agent.total_tasks_failed
            success_rate = (agent.total_tasks_completed / total_tasks * 100) if total_tasks > 0 else 0.0
            
            # Get average confidence score
            avg_confidence = 0.0
            if hasattr(agent, 'confidence_scores') and agent.confidence_scores:
                avg_confidence = sum(agent.confidence_scores.values()) / len(agent.confidence_scores)
            
            # Determine status
            status = "Active" if agent.total_tasks_completed > 0 else "Idle"
            
            row = {
                "agent_id": agent.id[:8] + "...",  # Truncate for display
                "name": agent.name,
                "status": status,
                "tasks_completed": agent.total_tasks_completed,
                "success_rate": round(success_rate, 1),
                "confidence": round(avg_confidence * 100, 1)  # Convert to percentage
            }
            
            data.append(row)
        
        return columns, data
        
    except Exception as e:
        print(f"Error in agent confidence table callback: {e}")
        return [], []

@app.callback(
    Output("agent-success-failure-chart", "figure"),
    [Input("update-interval", "n_intervals")]
)
def update_agent_success_failure_chart(n):
    try:
        if not controller.agents:
            return go.Figure()
        
        agent_names = []
        success_counts = []
        failure_counts = []
        
        for agent in controller.agents.values():
            profile = agent.get_adaptivity_profile()
            agent_names.append(agent.name)
            success_counts.append(agent.total_tasks_completed)
            failure_counts.append(agent.total_tasks_failed)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Success',
            x=agent_names,
            y=success_counts,
            marker_color='#66bb6a'
        ))
        
        fig.add_trace(go.Bar(
            name='Failure',
            x=agent_names,
            y=failure_counts,
            marker_color='#ef5350'
        ))
        
        fig.update_layout(
            barmode='group',
            height=300,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            legend=dict(font=dict(color='white')),
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        return fig
        
    except Exception as e:
        print(f"Error in success/failure chart callback: {e}")
        return go.Figure()

@app.callback(
    Output("agent-expertise-container", "children"),
    [Input("update-interval", "n_intervals")]
)
def update_agent_expertise(n):
    try:
        if not controller.agents:
            return []
        
        expertise_cards = []
        for agent in controller.agents.values():
            profile = agent.get_adaptivity_profile()
            
            if profile["expertise"]:
                expertise_tags = [
                    html.Span(
                        expertise.replace("_", " ").title(),
                        className="expertise-tag"
                    ) for expertise in profile["expertise"]
                ]
                
                expertise_cards.append(
                    html.Div([
                        html.H4(agent.name, className="agent-name"),
                        html.Div(expertise_tags, className="expertise-tags")
                    ], className="expertise-card")
                )
        
        if not expertise_cards:
            expertise_cards.append(
                html.Div([
                    html.P("No agents have achieved expert level yet. Continue training!", 
                           className="no-expertise-message")
                ], className="no-expertise-card")
            )
        
        return expertise_cards
        
    except Exception as e:
        print(f"Error in agent expertise callback: {e}")
        return []

# Training mode callback
@app.callback(
    Output("training-mode-toggle", "value"),
    [Input("training-mode-toggle", "value")],
    prevent_initial_call=True
)
def toggle_training_mode(value):
    if value:
        controller.toggle_training_mode()
    return value

# Simulation control callbacks
@app.callback(
    Output("start-sim-btn", "n_clicks"),
    [Input("start-sim-btn", "n_clicks")],
    prevent_initial_call=True
)
def start_simulation(n_clicks):
    if n_clicks:
        controller.start_simulation()
        start_simulation_thread()
    return 0

@app.callback(
    Output("stop-sim-btn", "n_clicks"),
    [Input("stop-sim-btn", "n_clicks")],
    prevent_initial_call=True
)
def stop_simulation_callback(n_clicks):
    if n_clicks:
        controller.stop_simulation()
        stop_simulation_thread()
    return 0

@app.callback(
    Output("add-demo-tasks-btn", "n_clicks"),
    [Input("add-demo-tasks-btn", "n_clicks")],
    prevent_initial_call=True
)
def add_demo_tasks(n_clicks):
    if n_clicks:
        for template in TASK_TEMPLATES:
            controller.create_task(
                name=template["name"],
                description=template["description"],
                required_capabilities=template["required_capabilities"],
                complexity=template["complexity"],
                priority=template["priority"],
                estimated_duration=template["estimated_duration"]
            )
    return 0

# Agent management callbacks
@app.callback(
    [Output("add-agent-btn", "n_clicks"),
     Output("agent-name-input", "value"),
     Output("agent-capabilities-dropdown", "value")],
    [Input("add-agent-btn", "n_clicks")],
    [State("agent-name-input", "value"),
     State("agent-capabilities-dropdown", "value")],
    prevent_initial_call=True
)
def add_agent(n_clicks, name, capabilities):
    if n_clicks and name and capabilities:
        controller.add_agent(name, capabilities)
        return 0, "", []
    return 0, "", []

# Task management callbacks
@app.callback(
    [Output("create-task-btn", "n_clicks"),
     Output("task-name-input", "value"),
     Output("task-description-input", "value"),
     Output("task-capabilities-dropdown", "value"),
     Output("task-complexity-slider", "value"),
     Output("task-priority-slider", "value"),
     Output("task-duration-slider", "value")],
    [Input("create-task-btn", "n_clicks")],
    [State("task-name-input", "value"),
     State("task-description-input", "value"),
     State("task-capabilities-dropdown", "value"),
     State("task-complexity-slider", "value"),
     State("task-priority-slider", "value"),
     State("task-duration-slider", "value")],
    prevent_initial_call=True
)
def create_task(n_clicks, name, description, capabilities, complexity, priority, duration):
    if n_clicks and name and description and capabilities:
        controller.create_task(
            name=name,
            description=description,
            required_capabilities=capabilities,
            complexity=complexity,
            priority=priority,
            estimated_duration=duration
        )
        return 0, "", "", [], 5, 5, 10
    return 0, "", "", [], 5, 5, 10

# Live Performance Stats callback
@app.callback(
    Output('performance-data', 'figure'),
    [Input('update-interval', 'n_intervals')]
)
def update_performance_graph(n):
    import random
    
    # Update performance data for each agent
    for agent in agent_names:
        if len(performance_data[agent]['tasks_completed']) > 20:
            performance_data[agent]['tasks_completed'].pop(0)
            performance_data[agent]['confidence'].pop(0)
        
        performance_data[agent]['tasks_completed'].append(random.randint(0, 10))
        performance_data[agent]['confidence'].append(round(random.uniform(0.6, 1.0), 2))
    
    # Create the figure
    figure = {
        'data': [
            go.Scatter(
                x=list(range(len(performance_data[agent]['tasks_completed']))) or [0],
                y=performance_data[agent]['tasks_completed'],
                mode='lines+markers',
                name=f'{agent} Tasks Completed'
            ) for agent in agent_names
        ] + [
            go.Scatter(
                x=list(range(len(performance_data[agent]['confidence']))),
                y=performance_data[agent]['confidence'],
                mode='lines+markers',
                name=f'{agent} Confidence',
                line=dict(dash='dot')
            ) for agent in agent_names
        ],
        'layout': go.Layout(
            title='Live Agent Performance',
            xaxis={'title': 'Time'},
            yaxis={'title': 'Metrics'},
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(255,255,255,0.05)',
            font=dict(color='white'),
            showlegend=True,
            legend=dict(
                bgcolor='rgba(0,0,0,0.5)',
                bordercolor='rgba(255,255,255,0.2)',
                borderwidth=1,
                font=dict(color='white')
            )
        )
    }
    return figure

# Confidence Trends callback
@app.callback(
    Output('confidence-trend-graph', 'figure'),
    [Input('update-interval', 'n_intervals')]
)
def update_confidence_trends(n):
    global confidence_history
    
    try:
        if not controller.agents:
            return go.Figure()
        
        # Agent colors for distinct visualization
        agent_colors = {
            'Quantum Analyst': '#00d4ff',
            'ML Optimizer': '#ff6b6b', 
            'Adaptive Coordinator': '#4ecdc4',
            'Resource Manager': '#45b7d1'
        }
        
        # Get current confidence scores and update history
        for agent in controller.agents.values():
            agent_name = agent.name
            
            # Initialize agent in history if not exists
            if agent_name not in confidence_history:
                confidence_history[agent_name] = {}
            
            # Get current confidence scores for all capabilities
            for capability in agent.capabilities:
                confidence_score = agent.get_capability_confidence(capability)
                
                # Initialize capability history if not exists
                if capability not in confidence_history[agent_name]:
                    confidence_history[agent_name][capability] = []
                
                # Add current score to history
                confidence_history[agent_name][capability].append(confidence_score)
                
                # Keep only last 20 points to avoid memory bloat
                if len(confidence_history[agent_name][capability]) > 20:
                    confidence_history[agent_name][capability] = confidence_history[agent_name][capability][-20:]
        
        # Create the figure
        fig = go.Figure()
        
        # Add traces for each agent/capability combination
        for agent_name, capabilities_data in confidence_history.items():
            for capability, confidence_values in capabilities_data.items():
                if confidence_values:  # Only add if we have data
                    # Create line name
                    line_name = f"{agent_name} - {capability.replace('_', ' ').title()}"
                    
                    # Get color for this agent
                    color = agent_colors.get(agent_name, '#ffffff')
                    
                    # Add trace
                    fig.add_trace(go.Scatter(
                        x=list(range(len(confidence_values))),
                        y=confidence_values,
                        mode='lines+markers',
                        name=line_name,
                        line=dict(
                            color=color,
                            width=2,
                            shape='spline'  # Smooth curved lines
                        ),
                        marker=dict(
                            size=4,
                            color=color
                        ),
                        hovertemplate=f'<b>{line_name}</b><br>' +
                                    'Time: %{x}<br>' +
                                    'Confidence: %{y:.3f}<br>' +
                                    '<extra></extra>'
                    ))
        
        # Update layout with dark theme styling
        fig.update_layout(
            title='Agent Capability Confidence Trends',
            xaxis=dict(
                title='Time Intervals',
                gridcolor='rgba(0, 212, 255, 0.1)',
                color='white',
                showgrid=True
            ),
            yaxis=dict(
                title='Confidence Score',
                range=[0, 1],
                gridcolor='rgba(0, 212, 255, 0.1)',
                color='white',
                showgrid=True
            ),
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            showlegend=True,
            legend=dict(
                bgcolor='rgba(0,0,0,0.5)',
                bordercolor='rgba(255,255,255,0.2)',
                borderwidth=1,
                font=dict(color='white')
            ),
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        return fig
        
    except Exception as e:
        print(f"Error in confidence trends callback: {e}")
        return go.Figure()

# Navigation callbacks
@app.callback(
    [Output(f"slide-{i}", "className") for i in range(1, 6)] +
    [Output(f"nav-dot-{i}", "className") for i in range(1, 6)] +
    [Output("current-slide", "data")],
    [Input(f"nav-dot-{i}", "n_clicks") for i in range(1, 6)] +
    [Input("current-slide", "data")]
)
def navigate_slides(*args):
    from dash import callback_context
    ctx = callback_context
    if not ctx.triggered:
        return ["slide active"] + ["slide"] * 4 + ["nav-dot active"] + ["nav-dot"] * 4 + [1]
    
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if 'nav-dot' in trigger_id:
        slide_num = int(trigger_id.split('-')[-1])
    else:
        slide_num = args[-1] if args[-1] else 1
    
    slide_classes = []
    nav_classes = []
    
    for i in range(1, 6):
        if i == slide_num:
            slide_classes.append("slide active")
            nav_classes.append("nav-dot active")
        else:
            slide_classes.append("slide")
            nav_classes.append("nav-dot")
    
    return slide_classes + nav_classes + [slide_num]

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050) 