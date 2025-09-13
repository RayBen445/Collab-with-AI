#!/usr/bin/env python3
"""
Automation Scripts Collection
Useful automation tools for common development and system administration tasks.
"""

import os
import sys
import shutil
import json
import time
import requests
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import argparse

class SystemAutomation:
    """Collection of system automation utilities."""
    
    def __init__(self):
        self.logs = []
    
    def log(self, message: str):
        """Log a message with timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.logs.append(log_entry)
        print(log_entry)
    
    def backup_directory(self, source: str, destination: str, exclude_patterns: List[str] = None) -> bool:
        """Backup a directory with optional exclusion patterns."""
        if exclude_patterns is None:
            exclude_patterns = ['.git', '__pycache__', '*.pyc', 'node_modules']
        
        try:
            source_path = Path(source)
            dest_path = Path(destination)
            
            if not source_path.exists():
                self.log(f"❌ Source directory does not exist: {source}")
                return False
            
            # Create timestamped backup directory
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = dest_path / f"backup_{source_path.name}_{timestamp}"
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            self.log(f"🔄 Starting backup from {source} to {backup_dir}")
            
            def should_exclude(file_path: Path) -> bool:
                for pattern in exclude_patterns:
                    if pattern in str(file_path) or file_path.match(pattern):
                        return True
                return False
            
            # Copy files recursively
            for item in source_path.rglob('*'):
                if should_exclude(item):
                    continue
                
                relative_path = item.relative_to(source_path)
                dest_item = backup_dir / relative_path
                
                if item.is_dir():
                    dest_item.mkdir(parents=True, exist_ok=True)
                elif item.is_file():
                    dest_item.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(item, dest_item)
            
            self.log(f"✅ Backup completed successfully: {backup_dir}")
            return True
            
        except Exception as e:
            self.log(f"❌ Backup failed: {e}")
            return False
    
    def cleanup_old_files(self, directory: str, days_old: int = 30, dry_run: bool = True) -> List[str]:
        """Clean up files older than specified days."""
        try:
            dir_path = Path(directory)
            if not dir_path.exists():
                self.log(f"❌ Directory does not exist: {directory}")
                return []
            
            cutoff_date = datetime.now() - timedelta(days=days_old)
            old_files = []
            
            for file_path in dir_path.rglob('*'):
                if file_path.is_file():
                    file_mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                    if file_mtime < cutoff_date:
                        old_files.append(str(file_path))
                        
                        if not dry_run:
                            file_path.unlink()
                            self.log(f"🗑️ Deleted: {file_path}")
                        else:
                            self.log(f"🔍 Would delete: {file_path}")
            
            if dry_run:
                self.log(f"📊 Found {len(old_files)} files older than {days_old} days (dry run)")
            else:
                self.log(f"✅ Cleaned up {len(old_files)} old files")
            
            return old_files
            
        except Exception as e:
            self.log(f"❌ Cleanup failed: {e}")
            return []
    
    def monitor_system_resources(self, duration_minutes: int = 5) -> Dict[str, Any]:
        """Monitor system resources for specified duration."""
        try:
            import psutil
        except ImportError:
            self.log("❌ psutil library required. Install with: pip install psutil")
            return {}
        
        self.log(f"📊 Starting system monitoring for {duration_minutes} minutes")
        
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        
        metrics = {
            'cpu_usage': [],
            'memory_usage': [],
            'disk_usage': [],
            'timestamps': []
        }
        
        try:
            while time.time() < end_time:
                timestamp = datetime.now()
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                disk = psutil.disk_usage('/')
                
                metrics['cpu_usage'].append(cpu_percent)
                metrics['memory_usage'].append(memory.percent)
                metrics['disk_usage'].append(disk.percent)
                metrics['timestamps'].append(timestamp.isoformat())
                
                self.log(f"CPU: {cpu_percent}%, Memory: {memory.percent}%, Disk: {disk.percent}%")
                time.sleep(10)  # Sample every 10 seconds
            
            # Calculate averages
            avg_cpu = sum(metrics['cpu_usage']) / len(metrics['cpu_usage'])
            avg_memory = sum(metrics['memory_usage']) / len(metrics['memory_usage'])
            avg_disk = sum(metrics['disk_usage']) / len(metrics['disk_usage'])
            
            summary = {
                'duration_minutes': duration_minutes,
                'average_cpu': round(avg_cpu, 2),
                'average_memory': round(avg_memory, 2),
                'average_disk': round(avg_disk, 2),
                'max_cpu': max(metrics['cpu_usage']),
                'max_memory': max(metrics['memory_usage']),
                'samples_collected': len(metrics['cpu_usage']),
                'detailed_metrics': metrics
            }
            
            self.log(f"📈 Monitoring complete. Avg CPU: {avg_cpu}%, Avg Memory: {avg_memory}%")
            return summary
            
        except KeyboardInterrupt:
            self.log("⏹️ Monitoring stopped by user")
            return metrics
        except Exception as e:
            self.log(f"❌ Monitoring failed: {e}")
            return {}

class DevelopmentAutomation:
    """Automation tools for development workflows."""
    
    def __init__(self):
        self.logs = []
    
    def log(self, message: str):
        """Log a message with timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.logs.append(log_entry)
        print(log_entry)
    
    def setup_project_structure(self, project_name: str, project_type: str = "python") -> bool:
        """Create a standard project structure."""
        try:
            project_path = Path(project_name)
            
            if project_path.exists():
                self.log(f"❌ Project directory already exists: {project_name}")
                return False
            
            self.log(f"🏗️ Creating {project_type} project: {project_name}")
            
            if project_type == "python":
                # Python project structure
                dirs = [
                    f"{project_name}/src",
                    f"{project_name}/tests",
                    f"{project_name}/docs",
                    f"{project_name}/scripts",
                    f"{project_name}/data"
                ]
                
                files = {
                    f"{project_name}/README.md": f"# {project_name}\n\nProject description goes here.\n",
                    f"{project_name}/requirements.txt": "# Add your dependencies here\n",
                    f"{project_name}/setup.py": f'''from setuptools import setup, find_packages

setup(
    name="{project_name}",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="Your Name",
    description="A short description of the project",
)''',
                    f"{project_name}/.gitignore": '''__pycache__/
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
venv/
ENV/
''',
                    f"{project_name}/src/__init__.py": "",
                    f"{project_name}/tests/__init__.py": "",
                    f"{project_name}/tests/test_main.py": f'''import unittest
from src import main

class TestMain(unittest.TestCase):
    def test_example(self):
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
'''
                }
            
            elif project_type == "web":
                # Web project structure
                dirs = [
                    f"{project_name}/src",
                    f"{project_name}/src/css",
                    f"{project_name}/src/js",
                    f"{project_name}/src/images",
                    f"{project_name}/tests",
                    f"{project_name}/docs"
                ]
                
                files = {
                    f"{project_name}/README.md": f"# {project_name}\n\nWeb application description goes here.\n",
                    f"{project_name}/package.json": f'''{
  "name": "{project_name.lower()}",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "start": "node server.js",
    "test": "echo \\"Error: no test specified\\" && exit 1"
  },
  "keywords": [],
  "author": "",
  "license": "ISC"
}''',
                    f"{project_name}/src/index.html": f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name}</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <h1>Welcome to {project_name}</h1>
    <script src="js/main.js"></script>
</body>
</html>''',
                    f"{project_name}/src/css/style.css": '''body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 20px;
    background-color: #f4f4f4;
}

h1 {
    color: #333;
    text-align: center;
}''',
                    f"{project_name}/src/js/main.js": '''document.addEventListener('DOMContentLoaded', function() {
    console.log('Welcome to your new project!');
});''',
                    f"{project_name}/.gitignore": '''node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.env
dist/
build/
'''
                }
            
            # Create directories
            for dir_path in dirs:
                Path(dir_path).mkdir(parents=True, exist_ok=True)
                self.log(f"📁 Created directory: {dir_path}")
            
            # Create files
            for file_path, content in files.items():
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.log(f"📄 Created file: {file_path}")
            
            self.log(f"✅ Project {project_name} created successfully!")
            return True
            
        except Exception as e:
            self.log(f"❌ Project creation failed: {e}")
            return False
    
    def run_tests_with_coverage(self, test_directory: str = "tests") -> Dict[str, Any]:
        """Run tests with coverage reporting."""
        try:
            self.log("🧪 Running tests with coverage...")
            
            # Check if pytest and coverage are available
            try:
                subprocess.run(["pytest", "--version"], capture_output=True, check=True)
                subprocess.run(["coverage", "--version"], capture_output=True, check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                self.log("❌ pytest and coverage required. Install with: pip install pytest coverage")
                return {}
            
            # Run tests with coverage
            coverage_cmd = [
                "coverage", "run", "-m", "pytest", test_directory, "-v"
            ]
            
            result = subprocess.run(coverage_cmd, capture_output=True, text=True)
            
            # Generate coverage report
            report_result = subprocess.run(
                ["coverage", "report"], capture_output=True, text=True
            )
            
            # Generate HTML coverage report
            html_result = subprocess.run(
                ["coverage", "html"], capture_output=True, text=True
            )
            
            test_output = {
                'exit_code': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'coverage_report': report_result.stdout,
                'html_report_generated': html_result.returncode == 0
            }
            
            if result.returncode == 0:
                self.log("✅ All tests passed!")
            else:
                self.log("❌ Some tests failed")
            
            if html_result.returncode == 0:
                self.log("📊 HTML coverage report generated in htmlcov/")
            
            return test_output
            
        except Exception as e:
            self.log(f"❌ Test execution failed: {e}")
            return {}

def main():
    parser = argparse.ArgumentParser(description="Automation Scripts Collection")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Backup command
    backup_parser = subparsers.add_parser('backup', help='Backup directory')
    backup_parser.add_argument('source', help='Source directory to backup')
    backup_parser.add_argument('destination', help='Destination for backup')
    backup_parser.add_argument('--exclude', nargs='*', default=[], help='Patterns to exclude')
    
    # Cleanup command
    cleanup_parser = subparsers.add_parser('cleanup', help='Cleanup old files')
    cleanup_parser.add_argument('directory', help='Directory to clean')
    cleanup_parser.add_argument('--days', type=int, default=30, help='Files older than this many days')
    cleanup_parser.add_argument('--execute', action='store_true', help='Actually delete files (default is dry run)')
    
    # Monitor command
    monitor_parser = subparsers.add_parser('monitor', help='Monitor system resources')
    monitor_parser.add_argument('--duration', type=int, default=5, help='Duration in minutes')
    
    # Project setup command
    project_parser = subparsers.add_parser('create-project', help='Create project structure')
    project_parser.add_argument('name', help='Project name')
    project_parser.add_argument('--type', choices=['python', 'web'], default='python', help='Project type')
    
    # Test command
    test_parser = subparsers.add_parser('test', help='Run tests with coverage')
    test_parser.add_argument('--directory', default='tests', help='Test directory')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == 'backup':
        automation = SystemAutomation()
        automation.backup_directory(args.source, args.destination, args.exclude)
    
    elif args.command == 'cleanup':
        automation = SystemAutomation()
        automation.cleanup_old_files(args.directory, args.days, not args.execute)
    
    elif args.command == 'monitor':
        automation = SystemAutomation()
        metrics = automation.monitor_system_resources(args.duration)
        if metrics:
            # Save metrics to file
            with open(f"system_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", 'w') as f:
                json.dump(metrics, f, indent=2)
    
    elif args.command == 'create-project':
        automation = DevelopmentAutomation()
        automation.setup_project_structure(args.name, args.type)
    
    elif args.command == 'test':
        automation = DevelopmentAutomation()
        results = automation.run_tests_with_coverage(args.directory)
        if results:
            print("\n" + "="*50)
            print("TEST RESULTS SUMMARY")
            print("="*50)
            print(f"Exit Code: {results['exit_code']}")
            if results.get('coverage_report'):
                print("\nCoverage Report:")
                print(results['coverage_report'])

if __name__ == "__main__":
    main()