param
(
    [parameter(Mandatory = $true)] [String] $databricksWorkspaceResourceId,
    [parameter(Mandatory = $true)] [String] $databricksWorkspaceUrl,
    [parameter(Mandatory = $false)] [int] $tokenLifeTimeSeconds = 300
)

$azureDatabricksPrincipalId = '2ff814a6-3304-4ab8-85cb-cd0e6f879c1d'

$headers = @{}
$headers["Authorization"] = "Bearer $((az account get-access-token --resource $azureDatabricksPrincipalId | ConvertFrom-Json).accessToken)"
$headers["X-Databricks-Azure-SP-Management-Token"] = "$((az account get-access-token --resource https://management.core.windows.net/ | ConvertFrom-Json).accessToken)"
$headers["X-Databricks-Azure-Workspace-Resource-Id"] = $databricksWorkspaceResourceId

$json = @{}
$json["lifetime_seconds"] = $tokenLifeTimeSeconds

$req = Invoke-WebRequest -Uri "https://$databricksWorkspaceUrl/api/2.0/token/create" -Body ($json | convertTo-Json) -ContentType "application/json" -Headers $headers -Method Post
$bearerToken = ($req.Content | ConvertFrom-Json).token_value

return $bearerToken