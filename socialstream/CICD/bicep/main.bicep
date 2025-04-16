@description('Environment name (dev, uat, prod)')
param environment string

@description('Location for all resources.')
param location string = 'centralindia'

@description('Prefix to be used for resource naming')
param prefix string = 'dbx'

@description('Tags to be applied to all resources')
param tags object = {
  Environment: environment
  Project: 'DatabricksCICD'
}

// Get current subscription to use in the managed resource group name
var subscriptionId = subscription().subscriptionId

// Resource naming
var workspaceName = '${prefix}-${environment}-dbx'
var storageAccountName = '${prefix}${environment}shutu'
var keyVaultName = '${prefix}-${environment}-kv'
var managedResourceGroupName = '${prefix}-${environment}-dbx-mrg'

// Use subscription ID and resource group name to create the resource ID
var managedResourceGroupId = '/subscriptions/${subscriptionId}/resourceGroups/${managedResourceGroupName}'

// Deploy Key Vault
module keyVaultDeploy 'keyvault.bicep' = {
  name: 'keyVault-Deployment'
  params: {
    keyVaultName: keyVaultName
    location: location
    tags: tags
  }
}

// Deploy Storage Account
module storageDeploy 'storage.bicep' = {
  name: 'storage-Deployment'
  params: {
    storageAccountName: storageAccountName
    location: location
    tags: tags
  }
}

// Deploy Databricks Workspace
module databricksDeploy 'databricks.bicep' = {
  name: 'databricks-Deployment'
  params: {
    workspaceName: workspaceName
    location: location
    managedResourceGroupId: managedResourceGroupId
    tags: tags
  }
}

// Outputs
output databricksWorkspaceUrl string = databricksDeploy.outputs.workspaceUrl
output databricksWorkspaceName string = databricksDeploy.outputs.workspaceName
output databricksWorkspaceId string = databricksDeploy.outputs.workspaceId
output storageAccountName string = storageDeploy.outputs.storageAccountName
output keyVaultName string = keyVaultDeploy.outputs.keyVaultName
