import ast
import tokenize
from io import BytesIO

# Sample Python code (as a normal string)
code = """
x = 10
y = 20
def add(a, b=10, *args, **kwargs):
    return a + b + sum(args)

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
function_argument={}
default_values = {}
arg={}
kwarg={}
# Walk through the AST
for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef):
        function_names.append(node.name)
        arg_names=[arg.arg for arg in node.args.args]
        if node.args.vararg:
            arg[node.name]={node.args.vararg.arg}
        if node.args.kwarg:
            kwarg[node.name]=[node.args.kwarg.arg]
        function_argument[node.name]=arg_names
        defaults = node.args.defaults
        if defaults:
            default_pairings = {}
            for i, default in enumerate(defaults):
                try:
                    value = ast.literal_eval(default)
                except:
                    value = "complex_expression"
                # Match with the last N arguments
                arg_with_default = arg_names[len(arg_names) - len(defaults) + i]
                default_pairings[arg_with_default] = value

            default_values[node.name] = default_pairings
        
        
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
print(f"📥 Arguments Found:\nPositional Args:{function_argument}\nDefault:{default_values}\n🌟 *args:{arg}\n🚀 **kwargs:{kwarg}")
