variable "subscription_id" {
  description = "Azure subscription ID used by the azurerm provider."
  type        = string
}

variable "location" {
  description = "Azure region for all resources."
  type        = string
  default     = "westeurope"
}

variable "name_prefix" {
  description = "Short lowercase prefix used in resource names."
  type        = string
  default     = "fmlcyber"

  validation {
    condition     = can(regex("^[a-z0-9]{3,12}$", var.name_prefix))
    error_message = "name_prefix must contain only lowercase letters and digits, length 3-12."
  }
}

variable "workspace_name" {
  description = "Azure Machine Learning workspace name."
  type        = string
  default     = "mlw-fair-ml-cyber"
}

variable "tags" {
  description = "Tags added to all resources."
  type        = map(string)
  default = {
    project     = "fair-ml-cyber"
    article     = "q1-cyber-nids"
    managed_by  = "terraform"
    environment = "research"
  }
}
