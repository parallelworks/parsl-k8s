from kubernetes import client, config
import json
import subprocess

def get_kube_token():
    try:
        # Run the command and capture output
        result = subprocess.run(
            ["pw", "kube", "token"], 
            capture_output=True, 
            text=True,
            check=True
        )

        # Parse the JSON output
        token_json = json.loads(result.stdout)

        # Extract the token
        return token_json["status"]["token"]
    
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")

    return None


def main():
    # Load kubeconfig
    config.load_kube_config()

    # Check active context
    contexts, active_context = config.list_kube_config_contexts()
    print(f"Active context: {active_context['name']}")

    # Create a Configuration object
    conf = client.Configuration()
    # Get the api key
    api_key = get_kube_token()
    conf.api_key = {"authorization": f"Bearer {api_key}"}
    config.load_kube_config(client_configuration=conf)

    # Create an API client with this configuration
    api_client = client.ApiClient(conf)

    # Extract relevant config manually
    conf_dict = {
        "host": conf.host,
        "verify_ssl": conf.verify_ssl,
        "ssl_ca_cert": conf.ssl_ca_cert,
        "api_key": conf.api_key if conf.api_key else "None",
    }

    # Print config safely
    print("Kubernetes API Client Configuration:")
    print(json.dumps(conf_dict, indent=2))

    # Initialize API instance
    api_instance = client.CoreV1Api(api_client)

    try:
        # Fetch list of pods
        pods = api_instance.list_namespaced_pod(namespace="pw-qa-test")
        print("Successfully listed pods:", [pod.metadata.name for pod in pods.items])
    except client.ApiException as e:
        print(f"Kubernetes API access failed: {e}")

if __name__ == "__main__":
    main()