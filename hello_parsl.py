import parsl
from parsl.config import Config
from parsl.executors import HighThroughputExecutor
from parsl.providers import LocalProvider

# Configure Parsl with a LocalProvider
config = Config(
    executors=[
        HighThroughputExecutor(
            label="local_htex",
            provider=LocalProvider()
        )
    ]
)

# Load the configuration
parsl.load(config)

# Define a simple Parsl app
@parsl.python_app
def hello():
    return "Hello, Parsl!"

# Run the app and get the result
if __name__ == "__main__":
    future = hello()
    print(future.result())  # Should print "Hello, Parsl!"
