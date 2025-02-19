#!/bin/bash

# Set variables
k8s_namespace="pw-qa-test"
workflow_name="parsl-demo"
job_number="00001"
docker_image="avidalto/parsl-container:latest"

# Define pod name
pod_name="${PW_USER}-${workflow_name}-${job_number}"

# Define target directory inside the pod
remote_workdir="/pw/jobs/${workflow_name}/${job_number}"

# Start the pod
kubectl run ${pod_name} -n ${k8s_namespace} --image=${docker_image} --restart=Never -- sleep infinity

# Wait for the pod to be ready
echo "Waiting for pod ${pod_name} to be ready..."
kubectl wait --for=condition=Ready pod/${pod_name} -n ${k8s_namespace} --timeout=120s

# Create target directory inside the pod
kubectl exec ${pod_name} -n ${k8s_namespace} -- mkdir -p ${remote_workdir}

# Copy working directory into the pod
kubectl cp . ${pod_name}:${remote_workdir} -n ${k8s_namespace}

# Run script inside the pod
kubectl exec ${pod_name} -n ${k8s_namespace} -- python ${remote_workdir}/main.py

# Wait 10 seconds and then check if the pod is still terminating
echo "Waiting 10 seconds for graceful termination..."
sleep 10

# Check if the pod is still running or terminating
pod_status=$(kubectl get pod ${pod_name} -n ${k8s_namespace} -o jsonpath='{.status.phase}')

# Force delete the pod if it's still running or terminating
if [[ "$pod_status" == "Running" || "$pod_status" == "Terminating" ]]; then
    echo "Pod is still ${pod_status}. Force deleting pod..."
    kubectl delete pod ${pod_name} -n ${k8s_namespace} --grace-period=0 --force
else
    echo "Pod terminated gracefully."
fi
