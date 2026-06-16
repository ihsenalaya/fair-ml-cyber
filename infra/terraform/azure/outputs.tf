output "resource_group_name" {
  value = azurerm_resource_group.main.name
}

output "machine_learning_workspace_name" {
  value = azurerm_machine_learning_workspace.main.name
}

output "machine_learning_workspace_id" {
  value = azurerm_machine_learning_workspace.main.id
}

output "storage_account_name" {
  value = azurerm_storage_account.main.name
}

output "key_vault_name" {
  value = azurerm_key_vault.main.name
}

output "application_insights_name" {
  value = azurerm_application_insights.main.name
}

output "log_analytics_workspace_name" {
  value = azurerm_log_analytics_workspace.main.name
}
