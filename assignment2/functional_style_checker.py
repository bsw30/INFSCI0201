import os
import re
import sys
from datetime import datetime

# File Analyzer to read file
class FileAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.content = []

    def read_file(self):
        try:
            with open(self.file_path, "r") as file:
                self.content = file.readlines()
        except FileNotFoundError:
            print(f"Error: File {self.file_path} not found. Please provide a valid path.")
            exit(1)
        except IOError:
            print(f"Error: Cannot read file {self.file_path}. Check file permissions.")
            exit(1)

# Code Analyzer Class to analyze code structure
class CodeAnalyzer:
    def __init__(self, content):
        self.content = content
        self.imports = []
        self.classes = []
        self.functions = []
        self.issues = []
        self.docstrings = {}
        self.non_compliant_classes = []
        self.non_compliant_functions = []
        self.unannotated_functions = []

    def analyze(self):
        for line_num, line in enumerate(self.content, start=1):
            self._analyze_line(line, line_num)
        self._check_naming_conventions()
        self._check_type_annotations()

    def _analyze_line(self, line, line_num):
        # Check for imports
        if line.startswith("import ") or line.startswith("from "):
            self.imports.append(line.strip())

        # Check for classes and functions
        class_match = re.match(r"^\s*class\s+(\w+)", line)
        func_match = re.match(r"^\s*def\s+(\w+)", line)

        if class_match:
            class_name = class_match.group(1)
            self.classes.append(class_name)
            self.docstrings[class_name] = self._get_docstring(line_num)

        elif func_match:
            func_name = func_match.group(1)
            is_method = line.startswith(" ")
            current_class = self.classes[-1] if self.classes and is_method else None
            qualified_name = f"{current_class}.{func_name}" if current_class else func_name

            # Track function and check docstring
            self.functions.append(qualified_name)
            self.docstrings[qualified_name] = self._get_docstring(line_num)

    def _get_docstring(self, start_line):
        for i in range(start_line, len(self.content)):
            line = self.content[i].strip()
            if line.startswith('"""') or line.startswith("'''"):
                docstring = []
                for j in range(i, len(self.content)):
                    line = self.content[j].strip()
                    docstring.append(line)
                    if line.endswith('"""') or line.endswith("'''") and j != i:
                        return "\n".join(docstring)
                break
        return "DocString not found."

    def _check_naming_conventions(self):
        camel_case = re.compile(r"^[A-Z][a-zA-Z0-9]*$")
        snake_case = re.compile(r"^[a-z_][a-z0-9_]*$")

        for class_name in self.classes:
            if not camel_case.match(class_name):
                self.non_compliant_classes.append(class_name)

        for func_name in self.functions:
            func_name = func_name.split(".")[-1]
            if not snake_case.match(func_name):
                self.non_compliant_functions.append(func_name)

    def _check_type_annotations(self):
        for line in self.content:
            if "def " in line:
                if not self._has_type_annotations(line):
                    func_name = line.split("def ")[1].split("(")[0]
                    self.unannotated_functions.append(func_name)

    def _has_type_annotations(self, line):
        param_pattern = r"\((.*?)\):"
        return_type_pattern = r"->\s*\w+"

        # Check parameter type
        param_match = re.search(param_pattern, line)
        params = param_match.group(1) if param_match else ""
        has_param_annotations = all(":" in param.strip() for param in params.split(",") if param.strip())

        # Check return type
        has_return_annotation = bool(re.search(return_type_pattern, line))

        return has_param_annotations and has_return_annotation


# Report Generator Class
class ReportGenerator:
    def __init__(self, analysis_data, report_path):
        self.analysis_data = analysis_data
        self.report_path = report_path

    def generate_report(self):
        report_content = [
            f"Style Report\nGenerated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"File structure: {self.report_path}",
            f"Total lines of code: {len([line for line in self.analysis_data.content if line.strip()])}",
        ]

        # Imports
        if self.analysis_data.imports:
            report_content.append("\nImports:")
            report_content.append("\n".join(self.analysis_data.imports))
        else:
            report_content.append("\nNo imports found.")

        # Classes
        if self.analysis_data.classes:
            report_content.append("\nClasses:")
            report_content.append("\n".join(self.analysis_data.classes))
        else:
            report_content.append("\nNo classes found.")

        # Functions excluding methods
        if self.analysis_data.functions:
            non_method_functions = [f for f in self.analysis_data.functions if '.' not in f]
            report_content.append("\nFunctions (excluding methods):")
            report_content.append("\n".join(non_method_functions))
        else:
            report_content.append("\nNo functions found.")

        # DocStrings
        if self.analysis_data.docstrings:
            report_content.append("\nDocStrings:")
            for name, docstring in self.analysis_data.docstrings.items():
                report_content.append(f"{name}: {docstring}\n")

        # Type Annotation Check
        if self.analysis_data.unannotated_functions:
            report_content.append("\nFunctions without type annotations:")
            report_content.append("\n".join(self.analysis_data.unannotated_functions))
        else:
            report_content.append("\nAll functions and methods have type annotations.")

        # Naming Convention Check
        if self.analysis_data.non_compliant_classes:
            report_content.append("\nClasses not following CamelCase:")
            report_content.append("\n".join(self.analysis_data.non_compliant_classes))
        else:
            report_content.append("\nAll classes follow CamelCase.")

        if self.analysis_data.non_compliant_functions:
            report_content.append("\nFunctions not following snake_case:")
            report_content.append("\n".join(self.analysis_data.non_compliant_functions))
        else:
            report_content.append("\nAll functions follow snake_case.")

        # Write to file
        with open(self.report_path, "w") as report_file:
            report_file.write("\n".join(report_content))


# Analysis and generate report
def main(file_path, report_path):
    file_analyzer = FileAnalyzer(file_path)
    file_analyzer.read_file()

    code_analyzer = CodeAnalyzer(file_analyzer.content)
    code_analyzer.analyze()

    report_generator = ReportGenerator(code_analyzer, report_path)
    report_generator.generate_report()
    print(f"Report generated at: {report_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <path_to_python_file>")
        sys.exit(1)
    file_path = sys.argv[1]
    report_path = f"style_report_{os.path.basename(file_path)}.txt"
    main(file_path, report_path)