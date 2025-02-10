import sys
import io
from flask import Flask, render_template, request

app = Flask(__name__)

def run_python_code(code):
    """ Execute Python code and capture output """
    old_stdout = sys.stdout  # Save current stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout
    error = None
    
    try:
        exec(code, {})  # Running Python code (Multiline Support)
    except Exception as e:
        error = str(e)  # Capture error
    
    sys.stdout = old_stdout  # Restore stdout
    return error if error else new_stdout.getvalue()  # Return output or error message

@app.route("/", methods=["GET", "POST"])
def index():
    output = ""
    if request.method == "POST":
        code = request.form["code"]
        output = run_python_code(code)  # Run user code
    return render_template("index.html", output=output)

if __name__ == "__main__":
    app.run(debug=True)
