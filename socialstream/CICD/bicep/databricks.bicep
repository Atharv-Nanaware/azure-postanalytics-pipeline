@description('Name for the Databricks workspace resource')
param workspaceName string

@description('Location for all resources')
param location string = 'centralindia'

@description('The ID of the managed resource group')
param managedResourceGroupId string

@description('Tags to be applied to the Databricks workspace')
param tags object = {}

resource databricksWorkspace 'Microsoft.Databricks/workspaces@2023-02-01' = {
  name: workspaceName
  location: location
  tags: tags
  sku: {
    name: 'premium' // Using Premium tier for all environments as requested
  }
  properties: {
    managedResourceGroupId: managedResourceGroupId
    // Optional parameters for networking, encryption, etc. can be added here
  }
}

// Outputs
output workspaceUrl string = databricksWorkspace.properties.workspaceUrl
output workspaceName string = databricksWorkspace.name
output workspaceId string = databricksWorkspace.id
