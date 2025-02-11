import parsl
from parsl.config import Config
from parsl.providers import KubernetesProvider
from parsl.executors import HighThroughputExecutor

# Configure Parsl with a LocalProvider
config = Config(
    executors=[
        HighThroughputExecutor(
            label="k8s_executor",
            provider = KubernetesProvider(
                namespace = "pw-qa-test",
                image = "avidalto/parsl-container:latest"
            )
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
    parsl.dfk().cleanup()
