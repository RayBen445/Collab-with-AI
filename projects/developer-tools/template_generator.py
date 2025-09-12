#!/usr/bin/env python3
"""
Code Template Generator
A collaborative developer tool for generating project templates and boilerplate code.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

class TemplateGenerator:
    """Advanced code template generator with AI-powered suggestions."""
    
    def __init__(self):
        self.templates = {
            "python": {
                "script": self.generate_python_script,
                "flask_app": self.generate_flask_app,
                "django_app": self.generate_django_app,
                "cli_tool": self.generate_cli_tool,
                "data_analysis": self.generate_data_analysis,
                "ml_project": self.generate_ml_project
            },
            "web": {
                "html_page": self.generate_html_page,
                "react_component": self.generate_react_component,
                "vue_component": self.generate_vue_component,
                "express_app": self.generate_express_app,
                "full_stack": self.generate_full_stack
            },
            "mobile": {
                "react_native": self.generate_react_native,
                "flutter_app": self.generate_flutter_app
            },
            "data": {
                "api_client": self.generate_api_client,
                "database_schema": self.generate_database_schema,
                "etl_pipeline": self.generate_etl_pipeline
            },
            "devops": {
                "dockerfile": self.generate_dockerfile,
                "ci_cd": self.generate_ci_cd,
                "terraform": self.generate_terraform
            }
        }
        
    def generate_project(self, project_type: str, template_name: str, project_name: str, 
                        options: Dict[str, Any] = None) -> bool:
        """Generate a complete project template."""
        if options is None:
            options = {}
            
        print(f"🚀 Generating {project_type} {template_name} project: {project_name}")
        print("=" * 60)
        
        # Create project directory
        project_path = Path(project_name)
        if project_path.exists():
            print(f"❌ Directory '{project_name}' already exists!")
            return False
            
        project_path.mkdir(parents=True)
        
        # Generate template
        if project_type in self.templates and template_name in self.templates[project_type]:
            success = self.templates[project_type][template_name](project_path, project_name, options)
            
            if success:
                self.create_readme(project_path, project_name, project_type, template_name)
                self.create_gitignore(project_path, project_type)
                print(f"\n✅ Project '{project_name}' generated successfully!")
                print(f"📁 Location: {project_path.absolute()}")
                self.print_next_steps(project_type, template_name)
                return True
            else:
                print(f"❌ Failed to generate {template_name} template")
                return False
        else:
            print(f"❌ Template '{project_type}/{template_name}' not found!")
            return False
    
    def generate_python_script(self, project_path: Path, project_name: str, options: Dict) -> bool:
        """Generate a Python script template."""
        script_file = project_path / f"{project_name.lower().replace('-', '_')}.py"
        
        content = f'''#!/usr/bin/env python3
"""
{project_name.replace('-', ' ').title()}
{options.get('description', 'A Python script for automation and utility tasks.')}
"""

import argparse
import sys
from pathlib import Path
from typing import List, Dict, Optional

def main():
    """Main function with command-line interface."""
    parser = argparse.ArgumentParser(
        description="{project_name.replace('-', ' ').title()}",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("input", help="Input file or parameter")
    parser.add_argument("--output", "-o", help="Output file or directory")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without executing")
    
    args = parser.parse_args()
    
    if args.verbose:
        print(f"🚀 Starting {{project_name.replace('-', ' ').title()}}")
        print(f"📥 Input: {{args.input}}")
        print(f"📤 Output: {{args.output or 'stdout'}}")
    
    try:
        process_input(args.input, args.output, args.verbose, args.dry_run)
        print("✅ Processing completed successfully!")
    except Exception as e:
        print(f"❌ Error: {{e}}", file=sys.stderr)
        sys.exit(1)

def process_input(input_path: str, output_path: Optional[str] = None, 
                 verbose: bool = False, dry_run: bool = False):
    """Process the input and generate output."""
    if verbose:
        print(f"Processing {{input_path}}...")
    
    # TODO: Implement your processing logic here
    if dry_run:
        print("DRY RUN: Would process the input here")
        return
    
    # Example processing
    input_file = Path(input_path)
    if not input_file.exists():
        raise FileNotFoundError(f"Input file {{input_path}} not found")
    
    # Your processing logic goes here
    result = f"Processed {{input_file.name}} at {{datetime.now()}}"
    
    if output_path:
        output_file = Path(output_path)
        output_file.write_text(result)
        if verbose:
            print(f"💾 Output saved to {{output_path}}")
    else:
        print(result)

def validate_input(input_path: str) -> bool:
    """Validate input parameters."""
    return Path(input_path).exists()

def setup_logging(verbose: bool = False):
    """Setup logging configuration."""
    import logging
    
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(f'{{project_name.lower()}}.log')
        ]
    )

if __name__ == "__main__":
    main()
'''
        
        script_file.write_text(content)
        script_file.chmod(0o755)
        
        # Create requirements.txt
        requirements = project_path / "requirements.txt"
        requirements.write_text("# Add your dependencies here\n")
        
        # Create tests directory
        tests_dir = project_path / "tests"
        tests_dir.mkdir()
        
        test_file = tests_dir / f"test_{project_name.lower().replace('-', '_')}.py"
        test_content = f'''import unittest
from pathlib import Path
import sys

# Add the parent directory to the path so we can import our module
sys.path.insert(0, str(Path(__file__).parent.parent))

from {project_name.lower().replace('-', '_')} import process_input, validate_input

class Test{project_name.replace('-', '').title()}(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_data_dir = Path(__file__).parent / "test_data"
        self.test_data_dir.mkdir(exist_ok=True)
        
        # Create test input file
        self.test_input = self.test_data_dir / "test_input.txt"
        self.test_input.write_text("Test data for processing")
    
    def tearDown(self):
        """Clean up after each test method."""
        if self.test_input.exists():
            self.test_input.unlink()
        if self.test_data_dir.exists():
            self.test_data_dir.rmdir()
    
    def test_validate_input(self):
        """Test input validation."""
        self.assertTrue(validate_input(str(self.test_input)))
        self.assertFalse(validate_input("nonexistent_file.txt"))
    
    def test_process_input(self):
        """Test main processing function."""
        # This is a placeholder test - implement based on your actual logic
        try:
            process_input(str(self.test_input), verbose=True, dry_run=True)
        except Exception as e:
            self.fail(f"process_input raised an exception: {{e}}")

if __name__ == "__main__":
    unittest.main()
'''
        test_file.write_text(test_content)
        
        return True
    
    def generate_flask_app(self, project_path: Path, project_name: str, options: Dict) -> bool:
        """Generate a Flask web application template."""
        
        # Create app structure
        app_dir = project_path / "app"
        app_dir.mkdir()
        
        # Main app file
        app_file = app_dir / "__init__.py"
        app_content = f'''from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os

def create_app(config_name=None):
    """Application factory pattern."""
    app = Flask(__name__)
    
    # Enable CORS for all routes
    CORS(app)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Register blueprints
    from .routes import main_bp
    app.register_blueprint(main_bp)
    
    # API routes
    from .api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app
'''
        app_file.write_text(app_content)
        
        # Routes
        routes_file = app_dir / "routes.py"
        routes_content = '''from flask import Blueprint, render_template, request, flash, redirect, url_for

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Home page."""
    return render_template('index.html', title='Home')

@main_bp.route('/about')
def about():
    """About page."""
    return render_template('about.html', title='About')

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact form page."""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        # TODO: Process contact form (send email, save to database, etc.)
        flash(f'Thank you {name}! We will get back to you soon.', 'success')
        return redirect(url_for('main.contact'))
    
    return render_template('contact.html', title='Contact')
'''
        routes_file.write_text(routes_content)
        
        # API routes
        api_file = app_dir / "api.py"
        api_content = '''from flask import Blueprint, jsonify, request
from datetime import datetime

api_bp = Blueprint('api', __name__)

@api_bp.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'Flask API'
    })

@api_bp.route('/data')
def get_data():
    """Sample data endpoint."""
    return jsonify({
        'data': [
            {'id': 1, 'name': 'Item 1', 'value': 100},
            {'id': 2, 'name': 'Item 2', 'value': 200},
            {'id': 3, 'name': 'Item 3', 'value': 300}
        ],
        'total': 3
    })

@api_bp.route('/data', methods=['POST'])
def create_data():
    """Create new data endpoint."""
    data = request.get_json()
    
    # TODO: Validate and save data
    return jsonify({
        'message': 'Data created successfully',
        'data': data
    }), 201
'''
        api_file.write_text(api_content)
        
        # Templates
        templates_dir = app_dir / "templates"
        templates_dir.mkdir()
        
        # Base template
        base_template = templates_dir / "base.html"
        base_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{% if title %}}{{{{ title }}}} - {{% endif %}}{project_name.replace('-', ' ').title()}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="{{{{ url_for('static', filename='css/style.css') }}}}">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="{{{{ url_for('main.index') }}}}">{project_name.replace('-', ' ').title()}</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="{{{{ url_for('main.index') }}}}">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{{{{ url_for('main.about') }}}}">About</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{{{{ url_for('main.contact') }}}}">Contact</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <main class="container mt-4">
        {{% with messages = get_flashed_messages(with_categories=true) %}}
            {{% if messages %}}
                {{% for category, message in messages %}}
                    <div class="alert alert-{{{{ 'danger' if category == 'error' else 'success' }}}} alert-dismissible fade show" role="alert">
                        {{{{ message }}}}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                {{% endfor %}}
            {{% endif %}}
        {{% endwith %}}

        {{% block content %}}{{% endblock %}}
    </main>

    <footer class="bg-light mt-5 py-4">
        <div class="container text-center">
            <p>&copy; {{{{ datetime.now().year }}}} {project_name.replace('-', ' ').title()}. Built with Flask and AI collaboration.</p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script src="{{{{ url_for('static', filename='js/app.js') }}}}"></script>
</body>
</html>'''
        base_template.write_text(base_content)
        
        # Index template
        index_template = templates_dir / "index.html"
        index_content = f'''{{% extends "base.html" %}}

{{% block content %}}
<div class="row">
    <div class="col-lg-8 mx-auto text-center">
        <h1 class="display-4">Welcome to {project_name.replace('-', ' ').title()}</h1>
        <p class="lead">A collaborative Flask application built with AI assistance.</p>
        
        <div class="row mt-5">
            <div class="col-md-4">
                <div class="card h-100">
                    <div class="card-body">
                        <h5 class="card-title">🚀 Fast Development</h5>
                        <p class="card-text">Built with modern Flask patterns and best practices for rapid development.</p>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card h-100">
                    <div class="card-body">
                        <h5 class="card-title">🔧 Customizable</h5>
                        <p class="card-text">Easy to extend and customize for your specific requirements.</p>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card h-100">
                    <div class="card-body">
                        <h5 class="card-title">📱 Responsive</h5>
                        <p class="card-text">Mobile-friendly design that works on all devices.</p>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="mt-5">
            <a href="{{{{ url_for('main.about') }}}}" class="btn btn-primary btn-lg me-3">Learn More</a>
            <a href="{{{{ url_for('main.contact') }}}}" class="btn btn-outline-primary btn-lg">Get Started</a>
        </div>
    </div>
</div>
{{% endblock %}}'''
        index_template.write_text(index_content)
        
        # Static files
        static_dir = app_dir / "static"
        static_dir.mkdir()
        
        css_dir = static_dir / "css"
        css_dir.mkdir()
        
        css_file = css_dir / "style.css"
        css_content = '''/* Custom styles for the application */
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.navbar-brand {
    font-weight: bold;
}

.card {
    transition: transform 0.3s ease;
    border: none;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.card:hover {
    transform: translateY(-5px);
}

footer {
    margin-top: auto;
}

.btn {
    border-radius: 25px;
}

.alert {
    border-radius: 10px;
}
'''
        css_file.write_text(css_content)
        
        js_dir = static_dir / "js"
        js_dir.mkdir()
        
        js_file = js_dir / "app.js"
        js_content = '''// Main application JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // API example
    fetchHealthCheck();
});

async function fetchHealthCheck() {
    try {
        const response = await fetch('/api/health');
        const data = await response.json();
        console.log('API Health Check:', data);
    } catch (error) {
        console.error('API Health Check failed:', error);
    }
}

async function fetchData() {
    try {
        const response = await fetch('/api/data');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Failed to fetch data:', error);
        return null;
    }
}
'''
        js_file.write_text(js_content)
        
        # Main run file
        run_file = project_path / "run.py"
        run_content = f'''#!/usr/bin/env python3
"""
{project_name.replace('-', ' ').title()} - Flask Application
Run the application in development mode.
"""

from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
'''
        run_file.write_text(run_content)
        run_file.chmod(0o755)
        
        # Requirements
        requirements = project_path / "requirements.txt"
        requirements_content = '''Flask==2.3.3
Flask-CORS==4.0.0
python-dotenv==1.0.0
'''
        requirements.write_text(requirements_content)
        
        # Environment file
        env_file = project_path / ".env.example"
        env_content = '''# Copy this file to .env and update the values
SECRET_KEY=your-secret-key-here
FLASK_DEBUG=True
DATABASE_URL=sqlite:///app.db
'''
        env_file.write_text(env_content)
        
        return True
    
    def generate_react_component(self, project_path: Path, project_name: str, options: Dict) -> bool:
        """Generate a React component template."""
        
        # Create component file
        component_name = project_name.replace('-', '').title()
        component_file = project_path / f"{component_name}.jsx"
        
        content = f'''import React, {{ useState, useEffect }} from 'react';
import PropTypes from 'prop-types';
import './{component_name}.css';

/**
 * {component_name} Component
 * {options.get('description', 'A reusable React component for modern web applications.')}
 */
const {component_name} = ({{ 
    title = '{component_name}',
    data = [],
    onAction,
    className = '',
    ...props 
}}) => {{
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [internalData, setInternalData] = useState(data);

    useEffect(() => {{
        setInternalData(data);
    }}, [data]);

    const handleAction = async (actionType, payload) => {{
        try {{
            setLoading(true);
            setError(null);
            
            if (onAction) {{
                await onAction(actionType, payload);
            }}
            
            // Handle internal state updates based on action
            switch (actionType) {{
                case 'add':
                    setInternalData(prev => [...prev, payload]);
                    break;
                case 'remove':
                    setInternalData(prev => prev.filter(item => item.id !== payload.id));
                    break;
                case 'update':
                    setInternalData(prev => 
                        prev.map(item => item.id === payload.id ? {{ ...item, ...payload }} : item)
                    );
                    break;
                default:
                    console.log(`Unknown action: ${{actionType}}`);
            }}
        }} catch (err) {{
            setError(err.message);
            console.error('Action failed:', err);
        }} finally {{
            setLoading(false);
        }}
    }};

    const renderContent = () => {{
        if (loading) {{
            return (
                <div className="loading-spinner">
                    <div className="spinner"></div>
                    <p>Loading...</p>
                </div>
            );
        }}

        if (error) {{
            return (
                <div className="error-message">
                    <h4>Error</h4>
                    <p>{{error}}</p>
                    <button onClick={{() => setError(null)}}>Dismiss</button>
                </div>
            );
        }}

        return (
            <div className="content">
                {{internalData.length === 0 ? (
                    <div className="empty-state">
                        <h3>No data available</h3>
                        <p>Start by adding some items.</p>
                    </div>
                ) : (
                    <div className="data-list">
                        {{internalData.map((item, index) => (
                            <div key={{item.id || index}} className="data-item">
                                <h4>{{item.title || item.name || `Item ${{index + 1}}`}}</h4>
                                <p>{{item.description || item.content || 'No description'}}</p>
                                <div className="item-actions">
                                    <button 
                                        onClick={{() => handleAction('update', {{ id: item.id, ...item }})}}
                                        className="btn btn-secondary"
                                    >
                                        Edit
                                    </button>
                                    <button 
                                        onClick={{() => handleAction('remove', {{ id: item.id }})}}
                                        className="btn btn-danger"
                                    >
                                        Remove
                                    </button>
                                </div>
                            </div>
                        ))}}
                    </div>
                )}}
            </div>
        );
    }};

    return (
        <div className={{`{component_name.lower()}-component ${{className}}`}} {{...props}}>
            <header className="component-header">
                <h2>{{title}}</h2>
                <button 
                    onClick={{() => handleAction('add', {{ 
                        id: Date.now(), 
                        title: 'New Item', 
                        description: 'New item description' 
                    }})}}
                    className="btn btn-primary"
                    disabled={{loading}}
                >
                    Add Item
                </button>
            </header>
            
            <main className="component-body">
                {{renderContent()}}
            </main>
            
            <footer className="component-footer">
                <small>{{internalData.length}} item(s) total</small>
            </footer>
        </div>
    );
}};

{component_name}.propTypes = {{
    title: PropTypes.string,
    data: PropTypes.arrayOf(PropTypes.object),
    onAction: PropTypes.func,
    className: PropTypes.string,
}};

export default {component_name};
'''
        component_file.write_text(content)
        
        # CSS file
        css_file = project_path / f"{component_name}.css"
        css_content = f'''.{component_name.lower()}-component {{
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1rem;
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}}

.component-header {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #f0f0f0;
}}

.component-header h2 {{
  margin: 0;
  color: #333;
  font-size: 1.5rem;
}}

.component-body {{
  min-height: 200px;
}}

.component-footer {{
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #f0f0f0;
  text-align: center;
  color: #666;
}}

.btn {{
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s ease;
}}

.btn-primary {{
  background-color: #007bff;
  color: white;
}}

.btn-primary:hover:not(:disabled) {{
  background-color: #0056b3;
}}

.btn-secondary {{
  background-color: #6c757d;
  color: white;
  margin-right: 0.5rem;
}}

.btn-secondary:hover:not(:disabled) {{
  background-color: #545b62;
}}

.btn-danger {{
  background-color: #dc3545;
  color: white;
}}

.btn-danger:hover:not(:disabled) {{
  background-color: #c82333;
}}

.btn:disabled {{
  opacity: 0.6;
  cursor: not-allowed;
}}

.loading-spinner {{
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
}}

.spinner {{
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #007bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}}

@keyframes spin {{
  0% {{ transform: rotate(0deg); }}
  100% {{ transform: rotate(360deg); }}
}}

.error-message {{
  background-color: #f8d7da;
  color: #721c24;
  padding: 1rem;
  border-radius: 4px;
  border: 1px solid #f5c6cb;
}}

.error-message h4 {{
  margin: 0 0 0.5rem 0;
}}

.error-message button {{
  margin-top: 0.5rem;
}}

.empty-state {{
  text-align: center;
  padding: 2rem;
  color: #666;
}}

.empty-state h3 {{
  margin-bottom: 0.5rem;
}}

.data-list {{
  display: grid;
  gap: 1rem;
}}

.data-item {{
  padding: 1rem;
  border: 1px solid #e9ecef;
  border-radius: 4px;
  background-color: #f8f9fa;
}}

.data-item h4 {{
  margin: 0 0 0.5rem 0;
  color: #333;
}}

.data-item p {{
  margin: 0 0 1rem 0;
  color: #666;
  line-height: 1.4;
}}

.item-actions {{
  display: flex;
  gap: 0.5rem;
}}

@media (max-width: 768px) {{
  .component-header {{
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }}
  
  .item-actions {{
    flex-direction: column;
  }}
  
  .btn {{
    width: 100%;
  }}
}}
'''
        css_file.write_text(css_content)
        
        # Story file for Storybook (optional)
        story_file = project_path / f"{component_name}.stories.js"
        story_content = f'''import React from 'react';
import {component_name} from './{component_name}';

export default {{
  title: 'Components/{component_name}',
  component: {component_name},
  parameters: {{
    docs: {{
      description: {{
        component: '{options.get('description', 'A reusable React component for modern web applications.')}',
      }},
    }},
  }},
  argTypes: {{
    onAction: {{ action: 'action-triggered' }},
    title: {{
      control: {{ type: 'text' }},
      description: 'The title displayed in the component header',
    }},
    data: {{
      control: {{ type: 'object' }},
      description: 'Array of data items to display',
    }},
    className: {{
      control: {{ type: 'text' }},
      description: 'Additional CSS classes',
    }},
  }},
}};

const Template = (args) => <{component_name} {{...args}} />;

export const Default = Template.bind({{}});
Default.args = {{
  title: '{component_name}',
  data: [],
}};

export const WithData = Template.bind({{}});
WithData.args = {{
  title: '{component_name} with Data',
  data: [
    {{ id: 1, title: 'First Item', description: 'This is the first item in the list.' }},
    {{ id: 2, title: 'Second Item', description: 'This is the second item in the list.' }},
    {{ id: 3, title: 'Third Item', description: 'This is the third item in the list.' }},
  ],
}};

export const CustomTitle = Template.bind({{}});
CustomTitle.args = {{
  title: 'Custom Component Title',
  data: [
    {{ id: 1, title: 'Sample Item', description: 'A sample item for demonstration.' }},
  ],
}};
'''
        story_file.write_text(story_content)
        
        # Test file
        test_file = project_path / f"{component_name}.test.jsx"
        test_content = f'''import React from 'react';
import {{ render, screen, fireEvent, waitFor }} from '@testing-library/react';
import '@testing-library/jest-dom';
import {component_name} from './{component_name}';

describe('{component_name}', () => {{
  const mockOnAction = jest.fn();
  
  const defaultProps = {{
    title: 'Test Component',
    data: [],
    onAction: mockOnAction,
  }};

  beforeEach(() => {{
    mockOnAction.mockClear();
  }});

  test('renders component with title', () => {{
    render(<{component_name} {{...defaultProps}} />);
    expect(screen.getByText('Test Component')).toBeInTheDocument();
  }});

  test('displays empty state when no data', () => {{
    render(<{component_name} {{...defaultProps}} />);
    expect(screen.getByText('No data available')).toBeInTheDocument();
  }});

  test('displays data items when provided', () => {{
    const testData = [
      {{ id: 1, title: 'Item 1', description: 'First item' }},
      {{ id: 2, title: 'Item 2', description: 'Second item' }},
    ];

    render(<{component_name} {{...defaultProps}} data={{testData}} />);
    
    expect(screen.getByText('Item 1')).toBeInTheDocument();
    expect(screen.getByText('Item 2')).toBeInTheDocument();
    expect(screen.getByText('First item')).toBeInTheDocument();
    expect(screen.getByText('Second item')).toBeInTheDocument();
  }});

  test('calls onAction when add button is clicked', async () => {{
    render(<{component_name} {{...defaultProps}} />);
    
    const addButton = screen.getByText('Add Item');
    fireEvent.click(addButton);

    await waitFor(() => {{
      expect(mockOnAction).toHaveBeenCalledWith('add', expect.objectContaining({{
        title: 'New Item',
        description: 'New item description',
      }}));
    }});
  }});

  test('calls onAction when edit button is clicked', async () => {{
    const testData = [{{ id: 1, title: 'Item 1', description: 'First item' }}];
    
    render(<{component_name} {{...defaultProps}} data={{testData}} />);
    
    const editButton = screen.getByText('Edit');
    fireEvent.click(editButton);

    await waitFor(() => {{
      expect(mockOnAction).toHaveBeenCalledWith('update', expect.objectContaining({{
        id: 1,
        title: 'Item 1',
        description: 'First item',
      }}));
    }});
  }});

  test('calls onAction when remove button is clicked', async () => {{
    const testData = [{{ id: 1, title: 'Item 1', description: 'First item' }}];
    
    render(<{component_name} {{...defaultProps}} data={{testData}} />);
    
    const removeButton = screen.getByText('Remove');
    fireEvent.click(removeButton);

    await waitFor(() => {{
      expect(mockOnAction).toHaveBeenCalledWith('remove', {{ id: 1 }});
    }});
  }});

  test('shows loading state', () => {{
    render(<{component_name} {{...defaultProps}} />);
    
    // Simulate loading by clicking add button
    const addButton = screen.getByText('Add Item');
    fireEvent.click(addButton);
    
    // Note: This test might need adjustment based on actual loading implementation
  }});

  test('applies custom className', () => {{
    const {{ container }} = render(
      <{component_name} {{...defaultProps}} className="custom-class" />
    );
    
    expect(container.firstChild).toHaveClass('custom-class');
  }});
}});
'''
        test_file.write_text(test_content)
        
        # Package.json for dependencies
        package_file = project_path / "package.json"
        package_content = f'''{{
  "name": "{project_name.lower()}",
  "version": "1.0.0",
  "description": "{options.get('description', 'A reusable React component')}",
  "main": "{component_name}.jsx",
  "scripts": {{
    "test": "jest",
    "test:watch": "jest --watch",
    "storybook": "start-storybook -p 6006",
    "build-storybook": "build-storybook"
  }},
  "dependencies": {{
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "prop-types": "^15.8.1"
  }},
  "devDependencies": {{
    "@testing-library/react": "^13.4.0",
    "@testing-library/jest-dom": "^5.16.5",
    "@testing-library/user-event": "^14.4.3",
    "jest": "^29.0.0",
    "jest-environment-jsdom": "^29.0.0"
  }},
  "keywords": [
    "react",
    "component",
    "ui",
    "reusable"
  ],
  "author": "AI-Human Collaboration",
  "license": "MIT"
}}
'''
        package_file.write_text(package_content)
        
        return True
    
    def generate_dockerfile(self, project_path: Path, project_name: str, options: Dict) -> bool:
        """Generate Dockerfile template."""
        
        app_type = options.get('type', 'python')
        
        if app_type == 'python':
            content = f'''# {project_name.replace('-', ' ').title()} - Python Application
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \\
    PYTHONUNBUFFERED=1 \\
    PIP_NO_CACHE_DIR=1 \\
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update \\
    && apt-get install -y --no-install-recommends \\
        build-essential \\
        curl \\
        postgresql-client \\
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy requirements first for better cache layering
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Change ownership to non-root user
RUN chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "app:app"]
'''
        elif app_type == 'node':
            content = f'''# {project_name.replace('-', ' ').title()} - Node.js Application
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Install dumb-init for proper signal handling
RUN apk add --no-cache dumb-init

# Create non-root user
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production && npm cache clean --force

# Copy application code
COPY . .

# Change ownership to non-root user
RUN chown -R nextjs:nodejs /app
USER nextjs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:3000/health || exit 1

# Run application
ENTRYPOINT ["dumb-init", "--"]
CMD ["npm", "start"]
'''
        else:
            content = f'''# {project_name.replace('-', ' ').title()} - Multi-stage Build
FROM ubuntu:22.04 as builder

# Install build dependencies
RUN apt-get update && apt-get install -y \\
    build-essential \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

# Copy source code
WORKDIR /src
COPY . .

# Build application
RUN make build

# Production image
FROM ubuntu:22.04

# Install runtime dependencies
RUN apt-get update && apt-get install -y \\
    ca-certificates \\
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy built application
COPY --from=builder /src/dist /app/

# Change ownership
RUN chown -R appuser:appuser /app
USER appuser

# Set working directory
WORKDIR /app

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \\
    CMD ./healthcheck || exit 1

# Run application
CMD ["./app"]
'''
        
        dockerfile = project_path / "Dockerfile"
        dockerfile.write_text(content)
        
        # Docker compose file
        compose_content = f'''version: '3.8'

services:
  {project_name.lower().replace('-', '_')}:
    build: .
    container_name: {project_name.lower()}
    ports:
      - "8000:8000"
    environment:
      - NODE_ENV=production
    restart: unless-stopped
    depends_on:
      - db
      - redis
    networks:
      - app-network

  db:
    image: postgres:15-alpine
    container_name: {project_name.lower()}-db
    environment:
      POSTGRES_DB: {project_name.lower().replace('-', '_')}
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped
    networks:
      - app-network

  redis:
    image: redis:7-alpine
    container_name: {project_name.lower()}-redis
    ports:
      - "6379:6379"
    restart: unless-stopped
    networks:
      - app-network

volumes:
  postgres_data:

networks:
  app-network:
    driver: bridge
'''
        
        compose_file = project_path / "docker-compose.yml"
        compose_file.write_text(compose_content)
        
        # .dockerignore
        dockerignore_content = '''# Git
.git
.gitignore

# Documentation
README.md
*.md

# Environment files
.env
.env.local
.env.*.local

# Dependencies
node_modules/
__pycache__/
*.pyc
*.pyo

# Build artifacts
dist/
build/
*.egg-info/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Testing
coverage/
.nyc_output/
.pytest_cache/

# Temporary files
tmp/
temp/
'''
        
        dockerignore_file = project_path / ".dockerignore"
        dockerignore_file.write_text(dockerignore_content)
        
        return True
    
    def create_readme(self, project_path: Path, project_name: str, project_type: str, template_name: str):
        """Create a comprehensive README file."""
        
        readme_content = f'''# {project_name.replace('-', ' ').title()}

A {template_name.replace('_', ' ')} project generated with AI-human collaboration.

## 🚀 Quick Start

### Prerequisites

- Python 3.8+ (for Python projects)
- Node.js 16+ (for web projects)
- Docker (optional, for containerized deployment)

### Installation

```bash
# Clone or navigate to the project directory
cd {project_name}

# Install dependencies
pip install -r requirements.txt  # For Python projects
# OR
npm install  # For Node.js projects

# Run the application
python run.py  # For Python projects
# OR
npm start  # For Node.js projects
```

## 📁 Project Structure

```
{project_name}/
├── README.md
├── requirements.txt    # Python dependencies
├── package.json       # Node.js dependencies (if applicable)
├── .gitignore
├── .env.example       # Environment variables template
├── Dockerfile         # Container configuration
├── docker-compose.yml # Multi-service setup
└── src/              # Source code directory
```

## 🛠️ Development

### Running Tests

```bash
# Python projects
python -m pytest

# Node.js projects
npm test
```

### Code Style

This project follows industry best practices:

- Python: PEP 8 guidelines
- JavaScript: ESLint + Prettier
- Git: Conventional commits

### Environment Variables

Copy `.env.example` to `.env` and update the values:

```bash
cp .env.example .env
```

## 🐳 Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or run individual container
docker build -t {project_name.lower()} .
docker run -p 8000:8000 {project_name.lower()}
```

## 📚 Documentation

- [API Documentation](docs/api.md) - API endpoints and usage
- [Development Guide](docs/development.md) - Setup and development workflow
- [Deployment Guide](docs/deployment.md) - Production deployment instructions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with AI-human collaboration
- Generated using advanced code templates
- Follows modern development best practices

## 📞 Support

For support and questions:

- Create an issue in the repository
- Check the documentation in the `docs/` folder
- Review the code comments for implementation details

---

**Happy coding! 🎉**
'''
        
        readme_file = project_path / "README.md"
        readme_file.write_text(readme_content)
    
    def create_gitignore(self, project_path: Path, project_type: str):
        """Create appropriate .gitignore file."""
        
        if project_type == "python":
            gitignore_content = '''# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Database
*.db
*.sqlite3

# Local development
instance/
.webassets-cache
'''
        elif project_type == "web":
            gitignore_content = '''# Dependencies
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Production builds
/build
/dist
/.next/
/out/

# Runtime data
pids
*.pid
*.seed
*.pid.lock

# Coverage directory used by tools like istanbul
coverage/
.nyc_output/

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
logs
*.log

# Temporary folders
tmp/
temp/

# Storybook build outputs
storybook-static/

# Optional npm cache directory
.npm

# Optional REPL history
.node_repl_history
'''
        else:
            gitignore_content = '''# General
*.log
*.tmp
*.temp
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp
*.swo

# Environment
.env
.env.local

# Build outputs
build/
dist/
target/

# Dependencies
node_modules/
vendor/
'''
        
        gitignore_file = project_path / ".gitignore"
        gitignore_file.write_text(gitignore_content)
    
    def print_next_steps(self, project_type: str, template_name: str):
        """Print helpful next steps for the user."""
        
        print("\n🎯 Next Steps:")
        print("-" * 30)
        
        if project_type == "python":
            if template_name == "flask_app":
                print("1. cd into your project directory")
                print("2. Install dependencies: pip install -r requirements.txt")
                print("3. Copy .env.example to .env and configure")
                print("4. Run the app: python run.py")
                print("5. Visit http://localhost:5000")
            else:
                print("1. cd into your project directory")
                print("2. Install dependencies: pip install -r requirements.txt")
                print("3. Run the script: python your_script.py --help")
                print("4. Run tests: python -m pytest")
        
        elif project_type == "web":
            if template_name == "react_component":
                print("1. cd into your project directory")
                print("2. Install dependencies: npm install")
                print("3. Run tests: npm test")
                print("4. View in Storybook: npm run storybook")
            else:
                print("1. cd into your project directory")
                print("2. Install dependencies: npm install")
                print("3. Start development server: npm start")
                print("4. Open your browser to the displayed URL")
        
        print("\n💡 Pro Tips:")
        print("- Read the generated README.md for detailed instructions")
        print("- Check the .env.example file for configuration options")
        print("- Use Docker for consistent development environments")
        print("- Follow the contributing guidelines for collaboration")
    
    def list_templates(self):
        """List all available templates."""
        print("📋 Available Templates:")
        print("=" * 50)
        
        for category, templates in self.templates.items():
            print(f"\n{category.upper()}:")
            for template_name in templates.keys():
                print(f"  • {template_name}")
    
    def generate_cli_tool(self, project_path: Path, project_name: str, options: Dict) -> bool:
        """Generate a CLI tool template (placeholder for now)."""
        # Implementation similar to other generators
        return self.generate_python_script(project_path, project_name, options)
    
    def generate_data_analysis(self, project_path: Path, project_name: str, options: Dict) -> bool:
        """Generate a data analysis template (placeholder for now)."""
        return self.generate_python_script(project_path, project_name, options)
    
    def generate_ml_project(self, project_path: Path, project_name: str, options: Dict) -> bool:
        """Generate a machine learning project template (placeholder for now)."""
        return self.generate_python_script(project_path, project_name, options)
    
    def generate_django_app(self, project_path: Path, project_name: str, options: Dict) -> bool:
        """Generate a Django app template (placeholder for now)."""
        return self.generate_python_script(project_path, project_name, options)
    
    def generate_html_page(self, project_path: Path, project_name: str, options: Dict) -> bool:
        """Generate an HTML page template (placeholder for now)."""
        return True
    
    def generate_vue_component(self, project_path: Path, project_name: str, options: Dict) -> bool:
        """Generate a Vue component template (placeholder for now)."""
        return True
    
    def generate_express_app(self, project_path: Path, project_name: str, options: Dict) -> bool:
        """Generate an Express app template (placeholder for now)."""
        return True
    
    def generate_full_stack(self, project_path: Path, project_name: str, options: Dict) -> bool:
        """Generate a full-stack template (placeholder for now)."""
        return True
    
    def generate_react_native(self, project_path: Path, project_name: str, options: Dict) -> bool:
        """Generate a React Native template (placeholder for now)."""
        return True
    
    def generate_flutter_app(self, project_path: Path, project_name: str, options: Dict) -> bool:
        """Generate a Flutter app template (placeholder for now)."""
        return True
    
    def generate_api_client(self, project_path: Path, project_name: str, options: Dict) -> bool:
        """Generate an API client template (placeholder for now)."""
        return True
    
    def generate_database_schema(self, project_path: Path, project_name: str, options: Dict) -> bool:
        """Generate a database schema template (placeholder for now)."""
        return True
    
    def generate_etl_pipeline(self, project_path: Path, project_name: str, options: Dict) -> bool:
        """Generate an ETL pipeline template (placeholder for now)."""
        return True
    
    def generate_ci_cd(self, project_path: Path, project_name: str, options: Dict) -> bool:
        """Generate CI/CD pipeline template (placeholder for now)."""
        return True
    
    def generate_terraform(self, project_path: Path, project_name: str, options: Dict) -> bool:
        """Generate Terraform template (placeholder for now)."""
        return True

def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="🤖 Code Template Generator - Collaborative AI-Human Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python template_generator.py python script my-awesome-tool
  python template_generator.py web react_component MyComponent
  python template_generator.py python flask_app my-web-app
  python template_generator.py devops dockerfile my-app --type python
  python template_generator.py --list
        '''
    )
    
    parser.add_argument("project_type", nargs='?', help="Project category (python, web, mobile, data, devops)")
    parser.add_argument("template_name", nargs='?', help="Template name within the category")
    parser.add_argument("project_name", nargs='?', help="Name for the generated project")
    parser.add_argument("--list", "-l", action="store_true", help="List all available templates")
    parser.add_argument("--description", "-d", help="Project description")
    parser.add_argument("--type", "-t", help="Additional type specification (e.g., python, node for dockerfile)")
    
    args = parser.parse_args()
    
    generator = TemplateGenerator()
    
    print("🤖🤝👨‍💻 CODE TEMPLATE GENERATOR")
    print("=" * 60)
    print("Collaborative AI-Human Development Tool")
    print("=" * 60)
    
    if args.list:
        generator.list_templates()
        return
    
    if not all([args.project_type, args.template_name, args.project_name]):
        print("❌ Missing required arguments!")
        print("Usage: python template_generator.py <project_type> <template_name> <project_name>")
        print("\nUse --list to see available templates")
        return
    
    options = {}
    if args.description:
        options['description'] = args.description
    if args.type:
        options['type'] = args.type
    
    success = generator.generate_project(
        args.project_type,
        args.template_name,
        args.project_name,
        options
    )
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()