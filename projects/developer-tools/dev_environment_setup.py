#!/usr/bin/env python3
"""
Development Environment Setup Tool
Automated setup of development environments for various programming languages and frameworks.
"""

import os
import sys
import json
import subprocess
import shutil
import platform
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import argparse
import tempfile
import zipfile
import tarfile
import urllib.request
from dataclasses import dataclass

@dataclass
class EnvironmentConfig:
    """Configuration for development environment."""
    name: str
    description: str
    dependencies: List[str]
    setup_commands: List[str]
    verify_commands: List[str]
    environment_variables: Dict[str, str]
    config_files: Dict[str, str]

class DevEnvironmentSetup:
    """Development environment setup automation."""
    
    def __init__(self):
        self.system = platform.system().lower()
        self.architecture = platform.machine().lower()
        self.logs = []
        
        # Common paths
        self.home_dir = Path.home()
        self.cache_dir = self.home_dir / ".dev_setup_cache"
        self.cache_dir.mkdir(exist_ok=True)
        
        # Load environment configurations
        self.environments = self._load_environment_configs()
    
    def log(self, message: str):
        """Log a message with timestamp."""
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.logs.append(log_entry)
        print(log_entry)
    
    def _load_environment_configs(self) -> Dict[str, EnvironmentConfig]:
        """Load predefined environment configurations."""
        configs = {}
        
        # Python Development Environment
        configs['python'] = EnvironmentConfig(
            name="Python Development",
            description="Complete Python development environment with common tools",
            dependencies=[
                "python3",
                "python3-pip",
                "python3-venv",
                "python3-dev"
            ],
            setup_commands=[
                "pip3 install --upgrade pip",
                "pip3 install virtualenv",
                "pip3 install pipenv",
                "pip3 install poetry",
                "pip3 install black flake8 pylint mypy",
                "pip3 install pytest pytest-cov",
                "pip3 install jupyter notebook",
                "pip3 install requests pandas numpy matplotlib seaborn"
            ],
            verify_commands=[
                "python3 --version",
                "pip3 --version",
                "virtualenv --version",
                "black --version",
                "pytest --version"
            ],
            environment_variables={
                "PYTHONPATH": ".",
                "PIP_REQUIRE_VIRTUALENV": "true"
            },
            config_files={
                ".gitignore": """__pycache__/
*.py[cod]
*$py.class
*.so
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
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/
""",
                "pyproject.toml": """[tool.black]
line-length = 88
target-version = ['py38']

[tool.isort]
profile = "black"

[tool.pylint.messages_control]
disable = "C0330, C0326"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
addopts = "-v --tb=short"
"""
            }
        )
        
        # Node.js Development Environment
        configs['nodejs'] = EnvironmentConfig(
            name="Node.js Development",
            description="Complete Node.js development environment",
            dependencies=[
                "nodejs",
                "npm"
            ],
            setup_commands=[
                "npm install -g yarn",
                "npm install -g @angular/cli",
                "npm install -g create-react-app",
                "npm install -g vue-cli",
                "npm install -g typescript",
                "npm install -g eslint prettier",
                "npm install -g nodemon",
                "npm install -g pm2"
            ],
            verify_commands=[
                "node --version",
                "npm --version",
                "yarn --version",
                "tsc --version",
                "eslint --version"
            ],
            environment_variables={
                "NODE_ENV": "development"
            },
            config_files={
                ".gitignore": """node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.env
.env.local
.env.development.local
.env.test.local
.env.production.local
dist/
build/
coverage/
""",
                "package.json": """{
  "name": "project",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "start": "node index.js",
    "dev": "nodemon index.js",
    "test": "jest",
    "lint": "eslint .",
    "format": "prettier --write ."
  },
  "keywords": [],
  "author": "",
  "license": "ISC"
}""",
                ".eslintrc.json": """{
  "env": {
    "es2021": true,
    "node": true
  },
  "extends": "eslint:recommended",
  "parserOptions": {
    "ecmaVersion": 12,
    "sourceType": "module"
  },
  "rules": {}
}"""
            }
        )
        
        # Docker Development Environment
        configs['docker'] = EnvironmentConfig(
            name="Docker Development",
            description="Docker and container development tools",
            dependencies=[
                "docker",
                "docker-compose"
            ],
            setup_commands=[
                "docker --version",
                "docker-compose --version"
            ],
            verify_commands=[
                "docker --version",
                "docker-compose --version",
                "docker run hello-world"
            ],
            environment_variables={},
            config_files={
                "Dockerfile": """FROM node:16-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
""",
                "docker-compose.yml": """version: '3.8'
services:
  app:
    build: .
    ports:
      - "3000:3000"
    volumes:
      - .:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
""",
                ".dockerignore": """node_modules
npm-debug.log
.git
.gitignore
README.md
.env
.nyc_output
coverage
.nyc_output
"""
            }
        )
        
        # Git Development Environment
        configs['git'] = EnvironmentConfig(
            name="Git Development",
            description="Git version control with common configurations",
            dependencies=[
                "git"
            ],
            setup_commands=[
                "git config --global init.defaultBranch main",
                "git config --global core.autocrlf input",
                "git config --global core.editor vim",
                "git config --global pull.rebase false",
                "git config --global alias.st status",
                "git config --global alias.co checkout",
                "git config --global alias.br branch",
                "git config --global alias.ci commit",
                "git config --global alias.unstage 'reset HEAD --'",
                "git config --global alias.last 'log -1 HEAD'",
                "git config --global alias.visual '!gitk'"
            ],
            verify_commands=[
                "git --version",
                "git config --global --list"
            ],
            environment_variables={},
            config_files={
                ".gitconfig": """[user]
	name = Your Name
	email = your.email@example.com

[core]
	autocrlf = input
	editor = vim

[init]
	defaultBranch = main

[pull]
	rebase = false

[alias]
	st = status
	co = checkout
	br = branch
	ci = commit
	unstage = reset HEAD --
	last = log -1 HEAD
	visual = !gitk
""",
                ".gitignore": """.env
.env.local
.env.*.local
.DS_Store
.vscode/
.idea/
*.log
node_modules/
dist/
build/
coverage/
"""
            }
        )
        
        return configs
    
    def run_command(self, command: str, check: bool = True) -> Tuple[bool, str, str]:
        """Run a shell command and return success status and output."""
        try:
            self.log(f"🔧 Running: {command}")
            
            if self.system == "windows":
                # Use cmd on Windows
                process = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=300
                )
            else:
                # Use bash on Unix-like systems
                process = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    executable='/bin/bash',
                    timeout=300
                )
            
            success = process.returncode == 0
            stdout = process.stdout.strip()
            stderr = process.stderr.strip()
            
            if success:
                self.log(f"✅ Command succeeded: {command}")
                if stdout:
                    self.log(f"📝 Output: {stdout}")
            else:
                self.log(f"❌ Command failed: {command}")
                if stderr:
                    self.log(f"📝 Error: {stderr}")
                
                if check:
                    raise subprocess.CalledProcessError(process.returncode, command, stderr)
            
            return success, stdout, stderr
            
        except subprocess.TimeoutExpired:
            self.log(f"⏱️ Command timed out: {command}")
            return False, "", "Command timed out"
        except Exception as e:
            self.log(f"❌ Command error: {command} - {e}")
            return False, "", str(e)
    
    def check_system_dependencies(self) -> Dict[str, bool]:
        """Check if system-level dependencies are available."""
        dependencies = {
            'python3': False,
            'pip3': False,
            'node': False,
            'npm': False,
            'git': False,
            'docker': False,
            'curl': False,
            'wget': False
        }
        
        self.log("🔍 Checking system dependencies...")
        
        for dep in dependencies:
            success, _, _ = self.run_command(f"{dep} --version", check=False)
            dependencies[dep] = success
            
            if success:
                self.log(f"✅ {dep} is available")
            else:
                self.log(f"❌ {dep} is not available")
        
        return dependencies
    
    def install_package_manager(self) -> bool:
        """Install package manager based on system."""
        try:
            if self.system == "darwin":  # macOS
                self.log("🍺 Installing Homebrew (macOS package manager)...")
                success, _, _ = self.run_command(
                    '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
                )
                return success
            
            elif self.system == "linux":
                # Check for different Linux distributions
                success, stdout, _ = self.run_command("cat /etc/os-release", check=False)
                if success and "ubuntu" in stdout.lower():
                    self.log("🐧 Updating apt package manager (Ubuntu)...")
                    success, _, _ = self.run_command("sudo apt update")
                    return success
                elif success and any(distro in stdout.lower() for distro in ["fedora", "rhel", "centos"]):
                    self.log("🐧 Updating yum/dnf package manager (RedHat-based)...")
                    success, _, _ = self.run_command("sudo dnf update || sudo yum update", check=False)
                    return success
            
            elif self.system == "windows":
                self.log("🪟 Installing Chocolatey (Windows package manager)...")
                success, _, _ = self.run_command(
                    'powershell -Command "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString(\'https://community.chocolatey.org/install.ps1\'))"'
                )
                return success
            
            return True
            
        except Exception as e:
            self.log(f"❌ Package manager installation failed: {e}")
            return False
    
    def setup_environment(self, env_name: str, skip_dependencies: bool = False) -> bool:
        """Set up a specific development environment."""
        if env_name not in self.environments:
            self.log(f"❌ Unknown environment: {env_name}")
            self.log(f"Available environments: {', '.join(self.environments.keys())}")
            return False
        
        config = self.environments[env_name]
        self.log(f"🚀 Setting up {config.name} environment...")
        
        # Install dependencies
        if not skip_dependencies:
            self.log("📦 Installing dependencies...")
            for dep in config.dependencies:
                if self.system == "darwin":
                    success, _, _ = self.run_command(f"brew install {dep}", check=False)
                elif self.system == "linux":
                    success, _, _ = self.run_command(f"sudo apt install -y {dep} || sudo dnf install -y {dep} || sudo yum install -y {dep}", check=False)
                elif self.system == "windows":
                    success, _, _ = self.run_command(f"choco install {dep} -y", check=False)
                
                if not success:
                    self.log(f"⚠️ Failed to install {dep}, continuing...")
        
        # Run setup commands
        self.log("⚙️ Running setup commands...")
        for command in config.setup_commands:
            success, _, _ = self.run_command(command, check=False)
            if not success:
                self.log(f"⚠️ Setup command failed: {command}")
        
        # Set environment variables
        if config.environment_variables:
            self.log("🌐 Setting environment variables...")
            for var, value in config.environment_variables.items():
                os.environ[var] = value
                self.log(f"Set {var}={value}")
        
        # Create config files
        if config.config_files:
            self.log("📄 Creating configuration files...")
            for filename, content in config.config_files.items():
                file_path = Path(filename)
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    self.log(f"✅ Created {filename}")
                except Exception as e:
                    self.log(f"❌ Failed to create {filename}: {e}")
        
        # Verify installation
        self.log("🔍 Verifying installation...")
        verification_passed = True
        for command in config.verify_commands:
            success, stdout, _ = self.run_command(command, check=False)
            if success:
                self.log(f"✅ Verification passed: {command}")
                if stdout:
                    self.log(f"   Version: {stdout.split('\n')[0]}")
            else:
                self.log(f"❌ Verification failed: {command}")
                verification_passed = False
        
        if verification_passed:
            self.log(f"🎉 {config.name} environment setup completed successfully!")
        else:
            self.log(f"⚠️ {config.name} environment setup completed with some issues")
        
        return verification_passed
    
    def create_project_template(self, project_name: str, template_type: str) -> bool:
        """Create a project template based on environment type."""
        if template_type not in self.environments:
            self.log(f"❌ Unknown template type: {template_type}")
            return False
        
        project_path = Path(project_name)
        if project_path.exists():
            self.log(f"❌ Project directory already exists: {project_name}")
            return False
        
        try:
            project_path.mkdir(parents=True)
            self.log(f"📁 Created project directory: {project_name}")
            
            config = self.environments[template_type]
            
            # Create config files in project directory
            for filename, content in config.config_files.items():
                file_path = project_path / filename
                file_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.log(f"✅ Created {file_path}")
            
            # Create basic project structure
            if template_type == "python":
                (project_path / "src").mkdir()
                (project_path / "tests").mkdir()
                (project_path / "docs").mkdir()
                
                # Create basic Python files
                with open(project_path / "src" / "__init__.py", 'w') as f:
                    f.write("")
                
                with open(project_path / "src" / "main.py", 'w') as f:
                    f.write('''#!/usr/bin/env python3
"""
Main module for the project.
"""

def main():
    """Main function."""
    print("Hello, World!")

if __name__ == "__main__":
    main()
''')
                
                with open(project_path / "tests" / "test_main.py", 'w') as f:
                    f.write('''import unittest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import main

class TestMain(unittest.TestCase):
    def test_main(self):
        # Test that main function runs without error
        try:
            main()
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"main() raised {e} unexpectedly!")

if __name__ == '__main__':
    unittest.main()
''')
            
            elif template_type == "nodejs":
                (project_path / "src").mkdir()
                (project_path / "tests").mkdir()
                (project_path / "public").mkdir()
                
                # Create basic Node.js files
                with open(project_path / "src" / "index.js", 'w') as f:
                    f.write('''const express = require('express');
const app = express();
const port = process.env.PORT || 3000;

app.get('/', (req, res) => {
    res.send('Hello, World!');
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
''')
                
                with open(project_path / "public" / "index.html", 'w') as f:
                    f.write('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project</title>
</head>
<body>
    <h1>Welcome to your project!</h1>
</body>
</html>
''')
            
            self.log(f"🎉 Project template '{template_type}' created successfully in {project_name}")
            return True
            
        except Exception as e:
            self.log(f"❌ Project template creation failed: {e}")
            return False
    
    def list_environments(self):
        """List all available environments."""
        self.log("📋 Available development environments:")
        for name, config in self.environments.items():
            self.log(f"  • {name}: {config.description}")
    
    def generate_setup_script(self, env_name: str, filename: str = None) -> str:
        """Generate a setup script for the environment."""
        if env_name not in self.environments:
            self.log(f"❌ Unknown environment: {env_name}")
            return ""
        
        if filename is None:
            filename = f"setup_{env_name}.sh"
        
        config = self.environments[env_name]
        
        script_content = f"""#!/bin/bash
# {config.name} Setup Script
# Generated automatically by DevEnvironmentSetup
# Description: {config.description}

set -e  # Exit on any error

echo "🚀 Setting up {config.name} environment..."

# Install dependencies
echo "📦 Installing dependencies..."
"""
        
        for dep in config.dependencies:
            if self.system == "darwin":
                script_content += f"brew install {dep} || echo 'Failed to install {dep}'\n"
            elif self.system == "linux":
                script_content += f"sudo apt install -y {dep} || sudo dnf install -y {dep} || sudo yum install -y {dep} || echo 'Failed to install {dep}'\n"
        
        script_content += """
# Run setup commands
echo "⚙️ Running setup commands..."
"""
        
        for command in config.setup_commands:
            script_content += f"{command} || echo 'Failed: {command}'\n"
        
        script_content += """
# Verify installation
echo "🔍 Verifying installation..."
"""
        
        for command in config.verify_commands:
            script_content += f"{command} && echo '✅ {command}' || echo '❌ {command}'\n"
        
        script_content += f"""
echo "🎉 {config.name} environment setup completed!"
"""
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(script_content)
            
            # Make script executable on Unix-like systems
            if self.system != "windows":
                os.chmod(filename, 0o755)
            
            self.log(f"✅ Setup script generated: {filename}")
            return filename
            
        except Exception as e:
            self.log(f"❌ Script generation failed: {e}")
            return ""

def main():
    parser = argparse.ArgumentParser(description="Development Environment Setup Tool")
    parser.add_argument('--list', action='store_true', help='List available environments')
    parser.add_argument('--setup', help='Setup environment (python, nodejs, docker, git)')
    parser.add_argument('--check', action='store_true', help='Check system dependencies')
    parser.add_argument('--create-project', help='Create project template')
    parser.add_argument('--template-type', default='python', help='Project template type')
    parser.add_argument('--generate-script', help='Generate setup script for environment')
    parser.add_argument('--skip-deps', action='store_true', help='Skip dependency installation')
    parser.add_argument('--install-pm', action='store_true', help='Install package manager')
    
    args = parser.parse_args()
    
    setup_tool = DevEnvironmentSetup()
    
    if args.list:
        setup_tool.list_environments()
    
    elif args.check:
        deps = setup_tool.check_system_dependencies()
        print("\n📊 SYSTEM DEPENDENCIES STATUS")
        print("=" * 40)
        for dep, available in deps.items():
            status = "✅ Available" if available else "❌ Missing"
            print(f"{dep:15} {status}")
    
    elif args.install_pm:
        setup_tool.install_package_manager()
    
    elif args.setup:
        setup_tool.setup_environment(args.setup, args.skip_deps)
    
    elif args.create_project:
        setup_tool.create_project_template(args.create_project, args.template_type)
    
    elif args.generate_script:
        setup_tool.generate_setup_script(args.generate_script)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()