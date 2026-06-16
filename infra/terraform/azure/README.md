# Azure ML Infrastructure

Terraform module for the FAIR-ML-CYBER article experiments.

It creates:

- one Azure resource group;
- one Azure Storage account for workspace data/artifacts;
- one Azure Key Vault;
- one Log Analytics workspace;
- one Application Insights resource;
- one Azure Machine Learning workspace.

The module intentionally does not create a compute cluster by default. Compute should be created after the workspace is visible, with an autoscaling minimum of zero nodes, so that experiment cost and VM quota failures are documented separately.

## Apply

```bash
terraform init
terraform validate
terraform apply -auto-approve \
  -var="subscription_id=ec0e829d-64e1-43fd-b721-ecf5b5112773" \
  -var="location=westeurope"
```

## Expected Workspace

- Resource group: `rg-fmlcyber-westeurope`
- Azure ML workspace: `mlw-fair-ml-cyber`
- Region: `westeurope`

After apply, verify with:

```bash
az ml workspace show \
  --resource-group rg-fmlcyber-westeurope \
  --name mlw-fair-ml-cyber
```
