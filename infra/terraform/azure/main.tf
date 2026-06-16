data "azurerm_client_config" "current" {}

resource "random_string" "suffix" {
  length  = 6
  lower   = true
  numeric = true
  special = false
  upper   = false
}

locals {
  resource_group_name       = "rg-${var.name_prefix}-${var.location}"
  storage_account_name      = "st${var.name_prefix}${random_string.suffix.result}"
  key_vault_name            = "kv-${var.name_prefix}-${random_string.suffix.result}"
  log_analytics_name        = "law-${var.name_prefix}-${random_string.suffix.result}"
  application_insights_name = "appi-${var.name_prefix}-${random_string.suffix.result}"
}

resource "azurerm_resource_group" "main" {
  name     = local.resource_group_name
  location = var.location
  tags     = var.tags
}

resource "azurerm_storage_account" "main" {
  name                            = local.storage_account_name
  resource_group_name             = azurerm_resource_group.main.name
  location                        = azurerm_resource_group.main.location
  account_tier                    = "Standard"
  account_replication_type        = "LRS"
  account_kind                    = "StorageV2"
  min_tls_version                 = "TLS1_2"
  allow_nested_items_to_be_public = false
  shared_access_key_enabled       = true
  tags                            = var.tags
}

resource "azurerm_key_vault" "main" {
  name                            = local.key_vault_name
  resource_group_name             = azurerm_resource_group.main.name
  location                        = azurerm_resource_group.main.location
  tenant_id                       = data.azurerm_client_config.current.tenant_id
  sku_name                        = "standard"
  soft_delete_retention_days      = 7
  purge_protection_enabled        = false
  rbac_authorization_enabled      = true
  enabled_for_deployment          = true
  enabled_for_disk_encryption     = true
  enabled_for_template_deployment = true
  tags                            = var.tags
}

resource "azurerm_log_analytics_workspace" "main" {
  name                = local.log_analytics_name
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  sku                 = "PerGB2018"
  retention_in_days   = 30
  tags                = var.tags
}

resource "azurerm_application_insights" "main" {
  name                = local.application_insights_name
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  application_type    = "web"
  workspace_id        = azurerm_log_analytics_workspace.main.id
  tags                = var.tags
}

resource "azurerm_machine_learning_workspace" "main" {
  name                          = var.workspace_name
  resource_group_name           = azurerm_resource_group.main.name
  location                      = azurerm_resource_group.main.location
  friendly_name                 = var.workspace_name
  application_insights_id       = azurerm_application_insights.main.id
  key_vault_id                  = azurerm_key_vault.main.id
  storage_account_id            = azurerm_storage_account.main.id
  public_network_access_enabled = true
  tags                          = var.tags

  identity {
    type = "SystemAssigned"
  }
}
