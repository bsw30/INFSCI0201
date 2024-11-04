import os
import re
from datetime import datetime

class FileAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.content = []
        self.line_count = 0  # New attribute

    def read_file(self):
        try:
            with open(self.file_path, "r") as file:
                self.content = file.readlines()
                self.line_count = len(self.content)
        except FileNotFoundError:
            print(f"Error: The file {self.file_path} was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

class CodeAnalyzer:
    def __init__(self, content, file_path, line_count):
        self.content = content
        self.file_path = file_path
        self.line_count = line_count
        self.imports = []
        self.classes = []
        self.functions = []
        self.issues = []
        self.docstrings = {}
        self.non_compliant_classes = []
        self.non_compliant_functions = []
        self.unannotated_functions = []
        self.current_class = None  # Track the current class context

    def analyze(self):
        for line_num, line in enumerate(self.content, start=1):
            self._analyze_line(line, line_num)
        self._check_naming_conventions()
        self._check_type_annotations()

    def _analyze_line(self, line, line_num):
        # Check for imports
        if line.startswith("import ") or line.startswith("from "):
            self.imports.append(line.strip())

        # Check for classes
        class_match = re.match(r"^\s*class\s+(\w+)", line)
        if class_match:
            class_name = class_match.group(1)
            self.classes.append(class_name)
            self.docstrings[class_name] = self._get_docstring(line_num)
            self.current_class = class_name  # Set current class context
            return

        # Check for functions
        func_match = re.match(r"^\s*def\s+(\w+)", line)
        if func_match:
            func_name = func_match.group(1)
            # Determine if the function is a method within a class
            qualified_name = f"{self.current_class}.{func_name}" if self.current_class else func_name
            self.functions.append(qualified_name)
            self.docstrings[qualified_name] = self._get_docstring(line_num)

        # Reset class context if non-indented is detected
        if line.strip() and not line.startswith(" "):
            self.current_class = None  # Reset class context

    def _get_docstring(self, start_line):
        for i in range(start_line, len(self.content)):
            line = self.content[i].strip()
            if line.startswith('"""') or line.startswith("'''"):
                docstring = [line]  # Start docstring with the opening line
                for j in range(i + 1, len(self.content)):
                    line = self.content[j].strip()
                    docstring.append(line)
                    if line.endswith('"""') or line.endswith("'''"):
                        docstring.append(line)
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

        # Check for parameter type annotations
        param_match = re.search(param_pattern, line)
        params = param_match.group(1) if param_match else ""
        has_param_annotations = all(":" in param.strip() for param in params.split(",") if param.strip())
        has_return_annotation = bool(re.search(return_type_pattern, line))
        return has_param_annotations and has_return_annotation


class ReportGenerator:
    def __init__(self, analysis_data):
        self.analysis_data = analysis_data
        self.report_path = f"style_report_{os.path.basename(self.analysis_data.file_path).replace('.py', '')}.txt"

    def _format_list_section(self, title, items):
        return f"\n{title}:\n" + "\n".join(items) if items else f"{title} not found."

    def generate_report(self):
        report_content = [
            f"Style Report\nGenerated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Total number of lines: {self.analysis_data.line_count}",
            self._format_list_section("Imports", self.analysis_data.imports),
            self._format_list_section("Classes", self.analysis_data.classes),
            self._format_list_section("Functions", self.analysis_data.functions),
            "\nDocStrings:\n" + "\n\n".join(f"{k}: {v}" for k, v in self.analysis_data.docstrings.items())
        ]

        # Annotations and naming conventions
        if self.analysis_data.unannotated_functions:
            report_content.append("\nFunctions without type annotations:")
            report_content.append("\n".join(self.analysis_data.unannotated_functions))
        else:
            report_content.append("\nAll functions have type annotations.")

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

        # Write the report to a file
        with open(self.report_path, 'w') as report_file:
            report_file.write("\n".join(report_content))

        print(f"Report generated: {self.report_path}")

# Example usage
if __name__ == "__main__":
    file_analyzer = FileAnalyzer("sample_code.py")  # Change this to your actual file path
    file_analyzer.read_file()

    if file_analyzer.content:  # Proceed only if the file was read successfully
        code_analyzer = CodeAnalyzer(file_analyzer.content, file_analyzer.file_path, file_analyzer.line_count)
        code_analyzer.analyze()

        report_generator = ReportGenerator(code_analyzer)
        report_generator.generate_report()