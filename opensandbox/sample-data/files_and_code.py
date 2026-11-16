from opensandbox import SandboxSync
from opensandbox.models import WriteEntry

# Pretend an AI agent wrote this code for us
agent_code = """
temps = [18, 21, 19, 24, 22, 20, 23]
avg = sum(temps) / len(temps)
with open('/tmp/summary.txt', 'w') as f:
    f.write(f'Days: {len(temps)}\\n')
    f.write(f'Warmest: {max(temps)} C\\n')
    f.write(f'Average: {avg:.1f} C\\n')
print('summary written')
"""

sandbox = SandboxSync.create("python:3.12-slim")
try:
    # 1. Write the code into a file inside the sandbox
    sandbox.files.write_files([
        WriteEntry(path="/tmp/agent_task.py", data=agent_code, mode=644)
    ])

    # 2. Run it inside the sandbox
    result = sandbox.commands.run("python3 /tmp/agent_task.py")
    print("[sandbox]", result.logs.stdout[0].text)

    # 3. Read back the file it created
    print(sandbox.files.read_file("/tmp/summary.txt"))
finally:
    sandbox.destroy()
