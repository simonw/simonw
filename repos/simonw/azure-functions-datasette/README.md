# Deploying Datasette using Azure Functions

This repository shows an example of Datasette deployed using Azure Functions.

https://azure-functions-datasette.azurewebsites.net/

It uses a slightly modified version of the ASGI proof of concept wrapper created by Anthony Shaw in [this GitHub issues thread](https://github.com/Azure/azure-functions-python-library/issues/75#issuecomment-808553496).

To deploy you'll need an Azure account, plus the `az` and `func` command-line tools. I installed these following the instructions in [this tutorial](https://docs.microsoft.com/en-us/azure/azure-functions/create-first-function-cli-python?tabs=azure-cli%2Cbash%2Cbrowser) - specifically [this](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=macos%2Ccsharp%2Cbash#v2) and [this](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli).

You'll need to create a resource group, a storage account and a function app.

I found that the resource group needed to be in `westeurope` for functions to work correctly.

Creating the resource group:

```
az group create \
    --name datasette-rg \
    --location westeurope
```
Creating the storage account:
```
az storage account create \
    --name datasettestorage \
    --location westeurope \
    --resource-group datasette-rg \
    --sku Standard_LRS
```
Creating the function app. The name here is the name that will be exposed in the default URL, so it needs to be globally unique - unlike the storage account and resource group which only have to be unique within your Azure account.
```
az functionapp create \
    --resource-group datasette-rg \
    --consumption-plan-location westeurope \
    --runtime python \
    --runtime-version 3.8 \
    --functions-version 3 \
    --storage-account datasettestorage \
    --os-type linux \
    --name azure-functions-datasette
```
Finally, deploy the application like so:
```
func azure functionapp publish azure-functions-datasette
```
