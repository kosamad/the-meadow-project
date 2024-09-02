import os
import sys

# Check if env.py exists and import it
env_path = os.path.join(os.path.dirname(__file__), 'env.py')
if os.path.exists(env_path):
    sys.path.append(os.path.dirname(__file__))
    import env