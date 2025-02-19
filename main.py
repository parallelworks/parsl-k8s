import parsl
from parsl.config import Config
from parsl.providers import KubernetesProvider
from parsl.executors import HighThroughputExecutor

print(parsl.__version__)
# Configure Parsl with a LocalProvider
config = Config(
    executors=[
        HighThroughputExecutor(
            label="k8s_executor",
            worker_debug = True,
            provider = KubernetesProvider(
                namespace = "pw-qa-test",
                image = "avidalto/parsl-container:latest",
                service_account_name = "parsl-service-account",
                nodes_per_block=1,
                init_blocks=1,
                min_blocks=1,
                max_blocks=1,
                max_cpu=3,
                max_mem="3Gi",
                init_cpu=2,
                init_mem="2Gi"
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
