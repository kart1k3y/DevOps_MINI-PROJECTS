Write-Host "--- Chaos Monkey Auto-Healing Demo (Infinite Loop) ---" -ForegroundColor Yellow
Write-Host "Press [Ctrl+C] to stop the script." -ForegroundColor DarkYellow

while ($true) {
    # Get pods with selector
    $pods = kubectl get pods -l app=calculator-app -o jsonpath='{.items[*].metadata.name}'
    if (-not $pods) {
        Write-Warning "No active pods found! Waiting for deployment to recover..."
        Start-Sleep -Seconds 5
        continue
    }

    # Split space-separated list of pods
    $podList = $pods.Trim() -split '\s+'
    Write-Host "`nActive Pods: $($podList -join ', ')" -ForegroundColor Cyan

    # Pick a random pod
    $randomPod = Get-Random -InputObject $podList
    Write-Host "Targeting random pod for deletion: $randomPod" -ForegroundColor Red

    # Delete the chosen pod
    kubectl delete pod $randomPod

    # Wait 15 seconds to let the deployment self-heal and display the logs
    Write-Host "Waiting 15 seconds for Kubernetes to auto-heal before the next check..." -ForegroundColor Gray
    Start-Sleep -Seconds 15
}
