import subprocess

def run_pylint():
    result = subprocess.run(['pylint', 'cortex'], capture_output=True, text=True)
    print("Python suggestions:\n", result.stdout)

def run_eslint():
    result = subprocess.run(['npx', 'eslint', '/apps'], capture_output=True, text=True)
    print("JS/TS suggestions:\n", result.stdout)

if __name__ == "__main__":
    run_pylint()
    run_eslint()