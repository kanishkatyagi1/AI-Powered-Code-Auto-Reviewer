import ast
import tokenize
from io import BytesIO

# Sample Python code (as a normal string)
code = """
x = 10
y = 20
def add(a, b):
    result = a + b
    return result

z = add(x, y)
# This is a sample Python script

def greet(name):
    # This function prints a greeting
    print(f"Hello, {name}!")

for i in range(3):  # Looping through numbers
    print(i)
"""

# Parse the code into an AST
tree = ast.parse(code)

# Lists to store extracted details
function_names = []
variable_names = []
assigned_variable_names = []
loops = []

# Walk through the AST
for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef):
        function_names.append(node.name)
    elif isinstance(node, (ast.For, ast.While)):
        loop_type = "for-loop" if isinstance(node, ast.For) else "while-loop"
        loops.append((loop_type, node.lineno))
    elif isinstance(node, ast.Name):
        variable_names.append(node.id)
    elif isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name):
                assigned_variable_names.append(target.id)

# Extract comments using tokenize
comments = []
tokens = tokenize.tokenize(BytesIO(code.encode()).readline)
for token in tokens:
    if token.type == tokenize.COMMENT:
        comments.append(token.string)

# Display results
print(f"🔹 Functions Found: {function_names}")
print(f"🔄 Loops Found: {loops}")
print(f"📌 Variables Found: {variable_names}")
print(f"📌 Assigned Variables Found: {assigned_variable_names}")
print(f"💬 Comments Found: {comments}")
