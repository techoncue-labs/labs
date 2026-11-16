from datetime import timedelta
from opensandbox import SandboxSync

# Create a sandbox that lives for 15 minutes
sandbox = SandboxSync.create("python:3.12-slim", timeout=timedelta(minutes=15))
print(sandbox.id)

# Close only our local connection; the sandbox keeps running
sandbox.close()
