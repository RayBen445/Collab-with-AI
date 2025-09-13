#!/usr/bin/env python3
"""
Testing Utilities and Framework Collection
Comprehensive testing tools for various programming languages and frameworks.
"""

import os
import sys
import json
import subprocess
import time
import re
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple, Union
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import tempfile
import shutil

@dataclass
class TestResult:
    """Data class for test results."""
    name: str
    status: str  # 'passed', 'failed', 'skipped', 'error'
    duration: float
    message: str = ""
    details: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class TestSuite:
    """Data class for test suite results."""
    name: str
    tests: List[TestResult] = field(default_factory=list)
    total_tests: int = 0
    passed: int = 0
    failed: int = 0
    skipped: int = 0
    errors: int = 0
    total_duration: float = 0.0
    coverage_percentage: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

class TestRunner(ABC):
    """Abstract base class for test runners."""
    
    @abstractmethod
    def discover_tests(self, directory: str) -> List[str]:
        """Discover test files in directory."""
        pass
    
    @abstractmethod
    def run_tests(self, test_files: List[str], **kwargs) -> TestSuite:
        """Run tests and return results."""
        pass
    
    @abstractmethod
    def generate_report(self, test_suite: TestSuite, format: str = 'text') -> str:
        """Generate test report in specified format."""
        pass

class PythonTestRunner(TestRunner):
    """Test runner for Python projects using pytest."""
    
    def __init__(self):
        self.name = "Python Test Runner"
        self.test_patterns = ['test_*.py', '*_test.py']
        
    def discover_tests(self, directory: str) -> List[str]:
        """Discover Python test files."""
        test_files = []
        dir_path = Path(directory)
        
        if not dir_path.exists():
            return test_files
        
        for pattern in self.test_patterns:
            test_files.extend(str(f) for f in dir_path.rglob(pattern))
        
        return test_files
    
    def run_tests(self, test_files: List[str] = None, directory: str = ".", **kwargs) -> TestSuite:
        """Run Python tests using pytest."""
        suite = TestSuite(name="Python Test Suite")
        
        try:
            # Check if pytest is available
            subprocess.run(['pytest', '--version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ pytest not found. Install with: pip install pytest")
            return suite
        
        # Build pytest command
        cmd = ['pytest', directory, '--verbose', '--tb=short']
        
        # Add coverage if available
        try:
            subprocess.run(['coverage', '--version'], capture_output=True, check=True)
            cmd.extend(['--cov=.', '--cov-report=term-missing', '--cov-report=json'])
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
        
        # Add specific test files if provided
        if test_files:
            cmd = ['pytest'] + test_files + ['--verbose', '--tb=short']
        
        # Additional pytest options from kwargs
        if kwargs.get('markers'):
            cmd.extend(['-m', kwargs['markers']])
        if kwargs.get('keywords'):
            cmd.extend(['-k', kwargs['keywords']])
        if kwargs.get('maxfail'):
            cmd.extend(['--maxfail', str(kwargs['maxfail'])])
        
        start_time = time.time()
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=directory)
            suite.total_duration = time.time() - start_time
            
            # Parse pytest output
            output_lines = result.stdout.split('\n')
            
            # Parse individual test results
            for line in output_lines:
                if '::' in line and any(status in line for status in ['PASSED', 'FAILED', 'SKIPPED', 'ERROR']):
                    test_result = self._parse_test_line(line)
                    if test_result:
                        suite.tests.append(test_result)
            
            # Parse summary line
            summary_pattern = r'(\d+) passed.*?(\d+) failed.*?(\d+) skipped'
            for line in reversed(output_lines):
                if 'passed' in line or 'failed' in line:
                    match = re.search(r'(\d+) passed', line)
                    if match:
                        suite.passed = int(match.group(1))
                    
                    match = re.search(r'(\d+) failed', line)
                    if match:
                        suite.failed = int(match.group(1))
                    
                    match = re.search(r'(\d+) skipped', line)
                    if match:
                        suite.skipped = int(match.group(1))
                    
                    match = re.search(r'(\d+) error', line)
                    if match:
                        suite.errors = int(match.group(1))
                    
                    break
            
            suite.total_tests = suite.passed + suite.failed + suite.skipped + suite.errors
            
            # Parse coverage if available
            try:
                with open(Path(directory) / 'coverage.json', 'r') as f:
                    coverage_data = json.load(f)
                    suite.coverage_percentage = coverage_data.get('totals', {}).get('percent_covered', 0.0)
            except FileNotFoundError:
                pass
            
        except Exception as e:
            print(f"❌ Test execution failed: {e}")
        
        return suite
    
    def _parse_test_line(self, line: str) -> Optional[TestResult]:
        """Parse a single test result line."""
        try:
            # Example: "test_file.py::test_function PASSED [100%]"
            parts = line.split()
            if len(parts) < 2:
                return None
            
            test_name = parts[0]
            status = parts[1].lower()
            
            # Extract duration if present
            duration = 0.0
            duration_match = re.search(r'\[(\d+\.\d+)s\]', line)
            if duration_match:
                duration = float(duration_match.group(1))
            
            return TestResult(
                name=test_name,
                status=status,
                duration=duration,
                message=""
            )
        except Exception:
            return None
    
    def generate_report(self, test_suite: TestSuite, format: str = 'text') -> str:
        """Generate test report."""
        if format == 'json':
            return json.dumps({
                'name': test_suite.name,
                'timestamp': test_suite.timestamp,
                'total_tests': test_suite.total_tests,
                'passed': test_suite.passed,
                'failed': test_suite.failed,
                'skipped': test_suite.skipped,
                'errors': test_suite.errors,
                'duration': test_suite.total_duration,
                'coverage': test_suite.coverage_percentage,
                'tests': [
                    {
                        'name': test.name,
                        'status': test.status,
                        'duration': test.duration,
                        'message': test.message
                    }
                    for test in test_suite.tests
                ]
            }, indent=2)
        
        # Text format
        report = f"""
{test_suite.name} - Test Report
{'='*50}
Timestamp: {test_suite.timestamp}
Duration: {test_suite.total_duration:.2f}s

Results Summary:
  Total Tests: {test_suite.total_tests}
  Passed: {test_suite.passed} ✅
  Failed: {test_suite.failed} ❌
  Skipped: {test_suite.skipped} ⏭️
  Errors: {test_suite.errors} 💥

Success Rate: {(test_suite.passed / max(test_suite.total_tests, 1)) * 100:.1f}%
"""
        
        if test_suite.coverage_percentage > 0:
            report += f"Coverage: {test_suite.coverage_percentage:.1f}%\n"
        
        if test_suite.failed > 0 or test_suite.errors > 0:
            report += "\nFailed/Error Tests:\n"
            for test in test_suite.tests:
                if test.status in ['failed', 'error']:
                    report += f"  • {test.name} ({test.status})\n"
        
        return report

class JavaScriptTestRunner(TestRunner):
    """Test runner for JavaScript/Node.js projects using Jest."""
    
    def __init__(self):
        self.name = "JavaScript Test Runner"
        self.test_patterns = ['*.test.js', '*.spec.js', '__tests__/**/*.js']
    
    def discover_tests(self, directory: str) -> List[str]:
        """Discover JavaScript test files."""
        test_files = []
        dir_path = Path(directory)
        
        if not dir_path.exists():
            return test_files
        
        # Look for Jest test files
        for pattern in self.test_patterns:
            if '**' in pattern:
                # Handle glob patterns
                pattern_parts = pattern.split('**')
                if len(pattern_parts) == 2:
                    for subdir in dir_path.rglob(pattern_parts[0].strip('/')):
                        if subdir.is_dir():
                            test_files.extend(str(f) for f in subdir.glob(pattern_parts[1].strip('/')))
            else:
                test_files.extend(str(f) for f in dir_path.rglob(pattern))
        
        return test_files
    
    def run_tests(self, test_files: List[str] = None, directory: str = ".", **kwargs) -> TestSuite:
        """Run JavaScript tests using Jest or npm test."""
        suite = TestSuite(name="JavaScript Test Suite")
        
        # Try to find appropriate test command
        test_cmd = None
        
        # Check for Jest
        try:
            subprocess.run(['npx', 'jest', '--version'], capture_output=True, check=True, cwd=directory)
            test_cmd = ['npx', 'jest', '--verbose', '--coverage', '--json']
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
        
        # Check for npm test script
        if not test_cmd:
            package_json = Path(directory) / 'package.json'
            if package_json.exists():
                try:
                    with open(package_json, 'r') as f:
                        package_data = json.load(f)
                        if 'scripts' in package_data and 'test' in package_data['scripts']:
                            test_cmd = ['npm', 'test']
                except Exception:
                    pass
        
        if not test_cmd:
            print("❌ No JavaScript test runner found (Jest or npm test)")
            return suite
        
        start_time = time.time()
        
        try:
            result = subprocess.run(test_cmd, capture_output=True, text=True, cwd=directory)
            suite.total_duration = time.time() - start_time
            
            # Try to parse JSON output (Jest)
            if '--json' in test_cmd:
                try:
                    test_output = json.loads(result.stdout)
                    suite = self._parse_jest_output(test_output, suite)
                except json.JSONDecodeError:
                    # Fallback to text parsing
                    suite = self._parse_text_output(result.stdout, suite)
            else:
                suite = self._parse_text_output(result.stdout, suite)
                
        except Exception as e:
            print(f"❌ JavaScript test execution failed: {e}")
        
        return suite
    
    def _parse_jest_output(self, output: Dict[str, Any], suite: TestSuite) -> TestSuite:
        """Parse Jest JSON output."""
        try:
            suite.total_tests = output.get('numTotalTests', 0)
            suite.passed = output.get('numPassedTests', 0)
            suite.failed = output.get('numFailedTests', 0)
            suite.skipped = output.get('numPendingTests', 0)
            
            # Parse individual test results
            for test_result in output.get('testResults', []):
                test_file = test_result.get('name', '')
                
                for assertion in test_result.get('assertionResults', []):
                    test = TestResult(
                        name=f"{test_file}::{assertion.get('title', '')}",
                        status=assertion.get('status', '').lower(),
                        duration=assertion.get('duration', 0) / 1000.0,  # Convert ms to seconds
                        message=assertion.get('failureMessages', [''])[0] if assertion.get('failureMessages') else ""
                    )
                    suite.tests.append(test)
            
            # Coverage information
            coverage_map = output.get('coverageMap')
            if coverage_map:
                # Calculate overall coverage percentage
                total_lines = 0
                covered_lines = 0
                
                for file_coverage in coverage_map.values():
                    if isinstance(file_coverage, dict):
                        statements = file_coverage.get('s', {})
                        total_lines += len(statements)
                        covered_lines += sum(1 for count in statements.values() if count > 0)
                
                if total_lines > 0:
                    suite.coverage_percentage = (covered_lines / total_lines) * 100
            
        except Exception as e:
            print(f"⚠️ Failed to parse Jest output: {e}")
        
        return suite
    
    def _parse_text_output(self, output: str, suite: TestSuite) -> TestSuite:
        """Parse text output from test runners."""
        lines = output.split('\n')
        
        for line in lines:
            # Look for test result indicators
            if '✓' in line or '✗' in line or 'PASS' in line or 'FAIL' in line:
                # This is a basic parser - could be enhanced for specific test runners
                status = 'passed' if ('✓' in line or 'PASS' in line) else 'failed'
                test_name = line.strip()
                
                test = TestResult(
                    name=test_name,
                    status=status,
                    duration=0.0
                )
                suite.tests.append(test)
        
        # Count results
        suite.total_tests = len(suite.tests)
        suite.passed = sum(1 for test in suite.tests if test.status == 'passed')
        suite.failed = sum(1 for test in suite.tests if test.status == 'failed')
        suite.skipped = sum(1 for test in suite.tests if test.status == 'skipped')
        
        return suite
    
    def generate_report(self, test_suite: TestSuite, format: str = 'text') -> str:
        """Generate JavaScript test report."""
        # Same as Python implementation - could be customized
        return PythonTestRunner().generate_report(test_suite, format)

class TestUtilities:
    """Collection of testing utilities and tools."""
    
    def __init__(self):
        self.runners = {
            'python': PythonTestRunner(),
            'javascript': JavaScriptTestRunner(),
            'js': JavaScriptTestRunner(),
            'node': JavaScriptTestRunner()
        }
    
    def detect_project_type(self, directory: str) -> str:
        """Detect project type based on files present."""
        dir_path = Path(directory)
        
        # Check for Python project indicators
        if any(dir_path.glob('*.py')) or (dir_path / 'setup.py').exists() or (dir_path / 'pyproject.toml').exists():
            return 'python'
        
        # Check for JavaScript/Node.js project indicators
        if (dir_path / 'package.json').exists() or any(dir_path.glob('*.js')):
            return 'javascript'
        
        return 'unknown'
    
    def run_tests(self, directory: str = ".", project_type: str = None, **kwargs) -> TestSuite:
        """Run tests automatically detecting project type."""
        if project_type is None:
            project_type = self.detect_project_type(directory)
        
        if project_type not in self.runners:
            print(f"❌ Unsupported project type: {project_type}")
            return TestSuite(name="Unknown Project")
        
        runner = self.runners[project_type]
        print(f"🧪 Running {runner.name} for {project_type} project...")
        
        return runner.run_tests(directory=directory, **kwargs)
    
    def generate_test_template(self, test_type: str, target_file: str, output_file: str = None) -> str:
        """Generate test template for a given file."""
        if output_file is None:
            target_path = Path(target_file)
            output_file = f"test_{target_path.stem}.py"
        
        if test_type == 'python':
            template = f'''import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add the source directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the module to test
# from {Path(target_file).stem} import YourClass, your_function

class Test{Path(target_file).stem.title()}(unittest.TestCase):
    """Test cases for {target_file}."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        pass
    
    def tearDown(self):
        """Clean up after each test method."""
        pass
    
    def test_example_function(self):
        """Test example function."""
        # Arrange
        expected_result = "expected"
        
        # Act
        # result = your_function()
        
        # Assert
        # self.assertEqual(result, expected_result)
        self.assertTrue(True)  # Placeholder test
    
    def test_example_class(self):
        """Test example class."""
        # Arrange
        # obj = YourClass()
        
        # Act & Assert
        # self.assertIsInstance(obj, YourClass)
        self.assertTrue(True)  # Placeholder test
    
    @patch('builtins.input', return_value='test_input')
    def test_with_mock_input(self, mock_input):
        """Test function that requires input."""
        # This is an example of mocking input
        # result = function_that_uses_input()
        # self.assertEqual(result, expected_result)
        pass
    
    def test_exception_handling(self):
        """Test exception handling."""
        # with self.assertRaises(ValueError):
        #     function_that_should_raise_exception()
        pass

if __name__ == '__main__':
    unittest.main()
'''
        
        elif test_type == 'javascript':
            template = f'''const {{ /* import functions to test */ }} = require('../{target_file}');

describe('{Path(target_file).stem}', () => {{
    beforeEach(() => {{
        // Set up test fixtures before each test
    }});
    
    afterEach(() => {{
        // Clean up after each test
    }});
    
    test('should pass example test', () => {{
        // Arrange
        const expected = 'expected result';
        
        // Act
        // const result = yourFunction();
        
        // Assert
        // expect(result).toBe(expected);
        expect(true).toBe(true); // Placeholder test
    }});
    
    test('should handle async operations', async () => {{
        // Arrange
        const expected = 'async result';
        
        // Act
        // const result = await yourAsyncFunction();
        
        // Assert
        // expect(result).toBe(expected);
        expect(true).toBe(true); // Placeholder test
    }});
    
    test('should handle errors', () => {{
        // Test error handling
        // expect(() => {{
        //     functionThatThrows();
        // }}).toThrow();
    }});
    
    test('should mock dependencies', () => {{
        // Example of mocking
        // const mockFunction = jest.fn().mockReturnValue('mocked result');
        // const result = functionUsingDependency(mockFunction);
        // expect(mockFunction).toHaveBeenCalled();
        // expect(result).toBe('expected with mock');
    }});
}});
'''
        else:
            print(f"❌ Unsupported test type: {test_type}")
            return ""
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(template)
            print(f"✅ Test template created: {output_file}")
            return output_file
        except Exception as e:
            print(f"❌ Failed to create test template: {e}")
            return ""
    
    def run_performance_test(self, directory: str, iterations: int = 100) -> Dict[str, Any]:
        """Run performance tests and collect metrics."""
        print(f"⚡ Running performance tests ({iterations} iterations)...")
        
        results = {
            'iterations': iterations,
            'total_time': 0.0,
            'average_time': 0.0,
            'min_time': float('inf'),
            'max_time': 0.0,
            'success_rate': 0.0,
            'timestamps': []
        }
        
        successful_runs = 0
        
        for i in range(iterations):
            start_time = time.time()
            
            try:
                # Run a single test iteration
                suite = self.run_tests(directory)
                duration = time.time() - start_time
                
                results['timestamps'].append(duration)
                results['total_time'] += duration
                results['min_time'] = min(results['min_time'], duration)
                results['max_time'] = max(results['max_time'], duration)
                
                if suite.failed == 0 and suite.errors == 0:
                    successful_runs += 1
                
                if (i + 1) % 10 == 0:
                    print(f"  Progress: {i + 1}/{iterations}")
                
            except Exception as e:
                print(f"❌ Performance test iteration {i + 1} failed: {e}")
        
        if results['total_time'] > 0:
            results['average_time'] = results['total_time'] / iterations
            results['success_rate'] = (successful_runs / iterations) * 100
        
        if results['min_time'] == float('inf'):
            results['min_time'] = 0.0
        
        print(f"📊 Performance test completed:")
        print(f"  Average time: {results['average_time']:.3f}s")
        print(f"  Min time: {results['min_time']:.3f}s")
        print(f"  Max time: {results['max_time']:.3f}s")
        print(f"  Success rate: {results['success_rate']:.1f}%")
        
        return results
    
    def generate_coverage_report(self, directory: str, output_dir: str = "coverage_report") -> str:
        """Generate comprehensive coverage report."""
        print("📊 Generating coverage report...")
        
        project_type = self.detect_project_type(directory)
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        if project_type == 'python':
            try:
                # Run tests with coverage
                subprocess.run([
                    'coverage', 'run', '-m', 'pytest', directory
                ], check=True, cwd=directory)
                
                # Generate HTML report
                subprocess.run([
                    'coverage', 'html', '-d', str(output_path)
                ], check=True, cwd=directory)
                
                # Generate XML report
                subprocess.run([
                    'coverage', 'xml', '-o', str(output_path / 'coverage.xml')
                ], check=True, cwd=directory)
                
                print(f"✅ Coverage report generated in {output_path}")
                return str(output_path)
                
            except subprocess.CalledProcessError as e:
                print(f"❌ Coverage report generation failed: {e}")
                return ""
            except FileNotFoundError:
                print("❌ Coverage tools not found. Install with: pip install coverage")
                return ""
        
        elif project_type == 'javascript':
            try:
                # Run Jest with coverage
                subprocess.run([
                    'npx', 'jest', '--coverage', '--coverageDirectory', str(output_path)
                ], check=True, cwd=directory)
                
                print(f"✅ Coverage report generated in {output_path}")
                return str(output_path)
                
            except subprocess.CalledProcessError as e:
                print(f"❌ Coverage report generation failed: {e}")
                return ""
            except FileNotFoundError:
                print("❌ Jest not found. Install with: npm install jest")
                return ""
        
        else:
            print(f"❌ Coverage reports not supported for project type: {project_type}")
            return ""

def main():
    parser = argparse.ArgumentParser(description="Testing Utilities and Framework Collection")
    parser.add_argument('--directory', '-d', default='.', help='Directory to test')
    parser.add_argument('--type', choices=['python', 'javascript', 'js', 'auto'], default='auto', help='Project type')
    parser.add_argument('--report', choices=['text', 'json'], default='text', help='Report format')
    parser.add_argument('--output', '-o', help='Output file for report')
    parser.add_argument('--coverage', action='store_true', help='Generate coverage report')
    parser.add_argument('--performance', action='store_true', help='Run performance tests')
    parser.add_argument('--iterations', type=int, default=10, help='Performance test iterations')
    parser.add_argument('--template', help='Generate test template for file')
    parser.add_argument('--template-type', choices=['python', 'javascript'], help='Test template type')
    
    args = parser.parse_args()
    
    utilities = TestUtilities()
    
    if args.template:
        if not args.template_type:
            args.template_type = utilities.detect_project_type(args.directory)
        utilities.generate_test_template(args.template_type, args.template)
        return
    
    # Determine project type
    project_type = args.type
    if project_type == 'auto':
        project_type = utilities.detect_project_type(args.directory)
        print(f"🔍 Detected project type: {project_type}")
    
    # Run performance tests
    if args.performance:
        utilities.run_performance_test(args.directory, args.iterations)
        return
    
    # Generate coverage report
    if args.coverage:
        utilities.generate_coverage_report(args.directory)
        return
    
    # Run tests
    test_suite = utilities.run_tests(args.directory, project_type)
    
    # Generate report
    runner = utilities.runners.get(project_type)
    if runner:
        report = runner.generate_report(test_suite, args.report)
        
        if args.output:
            try:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(report)
                print(f"📄 Report saved to: {args.output}")
            except Exception as e:
                print(f"❌ Failed to save report: {e}")
        else:
            print(report)

if __name__ == "__main__":
    main()