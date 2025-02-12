from kubernetes import client, config

def create_job():
    # Load the Kubernetes configuration (assumes running in-cluster or kubeconfig is set)
    config.load_kube_config()  # Use load_incluster_config() if running inside a cluster

    batch_v1 = client.BatchV1Api()

    # Define the container
    container = client.V1Container(
        name="example-container",
        image="avidalto/parsl-container:latest",
        command=["echo", "Hello, Kubernetes!"]
    )

    # Define the service account name to be used
    service_account_name = "parsl-service-account"

    # Define the job spec
    job = client.V1Job(
        metadata=client.V1ObjectMeta(name="example-job"),
        spec=client.V1JobSpec(
            template=client.V1PodTemplateSpec(
                spec=client.V1PodSpec(
                    restart_policy="Never",
                    containers=[container],
                    service_account_name=service_account_name  # Specify the service account here
                )
            )
        )
    )

    # Submit the job to the default namespace
    api_response = batch_v1.create_namespaced_job(namespace="pw-qa-test", body=job)
    print("Job created:", api_response.metadata.name)

if __name__ == "__main__":
    create_job()
