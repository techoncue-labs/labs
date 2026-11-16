from opensandbox import SandboxSync

# 1. Ask our local server for a fresh sandbox
sandbox = SandboxSync.create("python:3.12-slim")
print("Sandbox ready:", sandbox.id)

try:
    # 2. Run commands inside it
    for cmd in ["head -n 1 /etc/os-release", "python3 --version", "whoami"]:
        result = sandbox.commands.run(cmd)
        for line in result.logs.stdout:
            print(f"[sandbox] {cmd} -> {line.text}")
finally:
    # 3. Throw it away
    sandbox.destroy()
    print("Sandbox destroyed")
