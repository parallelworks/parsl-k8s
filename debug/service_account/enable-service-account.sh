kubectl apply -f service-account.yaml -n pw-qa-test
kubectl apply -f role.yaml -n pw-qa-test
kubectl apply -f role-binding.yaml -n pw-qa-test
kubectl create token parsl-service-account -n pw-qa-test
