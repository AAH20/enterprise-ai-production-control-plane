targetScope = 'resourceGroup'

@description('Globally unique suffix for Azure resource names')
param suffix string = uniqueString(resourceGroup().id)
param location string = resourceGroup().location
param tags object = {
  workload: 'enterprise-ai-production-control-plane'
  evidence: 'deployment-contract'
}

resource logs 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: 'law-aicontrol-${suffix}'
  location: location
  tags: tags
  properties: {
    retentionInDays: 30
    features: {
      enableLogAccessUsingOnlyResourcePermissions: true
    }
  }
}

resource insights 'Microsoft.Insights/components@2020-02-02' = {
  name: 'appi-aicontrol-${suffix}'
  location: location
  kind: 'web'
  tags: tags
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logs.id
  }
}

resource registry 'Microsoft.ContainerRegistry/registries@2023-07-01' = {
  name: 'acraicontrol${suffix}'
  location: location
  tags: tags
  sku: {
    name: 'Basic'
  }
  properties: {
    adminUserEnabled: false
    publicNetworkAccess: 'Enabled'
    policies: {
      quarantinePolicy: { status: 'disabled' }
      retentionPolicy: { days: 7, status: 'enabled' }
      trustPolicy: { type: 'Notary', status: 'disabled' }
    }
  }
}

output logAnalyticsWorkspaceId string = logs.id
output applicationInsightsId string = insights.id
output registryLoginServer string = registry.properties.loginServer

