# Form Extraction Approval
This is a demo project to show how to leverage GPT4 model to extract information from forms and trigger approval workflows.

The demo is build using [Azure Logic Apps](https://learn.microsoft.com/en-us/azure/logic-apps/logic-apps-overview) and [Azure Container Apps](https://learn.microsoft.com/en-us/azure/container-apps/overview).

Azure Logic Apps is being used as a trigger to extract attachements (in this case, PDF), upload the PDF to Azure Blob Storage, and call the Azure Container Apps to extract the information from the PDF. The Azure Container Apps runs the API that convert PDF to images, and call Azure Open AI GPT4 model to extract the information.

## Architecture
![Architecture](./assets/architecture.png)

Integration to Microsoft Outlook and Microsoft Teams are optional, it was selected for demostration purposes. The highlight for this sample is to show how Azure Open AI GPT4o can be used to extract content from forms.

## Test the API locally
The API is built using Flask, written in Python. Provide the following environment variables.

| Environment Variable | Remarks |
| -------- | -------- |
| BLOB_CONNECTION_STRING  | Connection string for Azure Storage to store images  |
| CONTAINER_NAME  | Azure Storage Container name to store images  |
|GPT4_ENDPOINT | Azure Open AI GPT4o model endpoint|
|GPT4_KEY | Azure Open AI GPT4o API key|

Run the following command to start the API
```bash
python3 main.py
```

The API will be available at http://localhost:5000. Test the API as follow:
```bash
curl --request POST --url http://localhost:5000/convert-pdf --header 'content-type: application/json' --data '{"pdf_url":"https://test.blob.core.windows.net/medicalcertificate/mc.pdf"}'
```

## Deploy to Azure Container Apps
Create an [Azure Container Registry](https://learn.microsoft.com/en-us/azure/container-registry/), or any container registry of your choice. Build the container image and push to the container registry.

Command to build this container image and push to Azure Container Registry. Replace container registry name, image name and tag accordingly.
```bash
docker build -t <container-registry-name>.azurecr.io/<image-name>:<tag> .
docker push <container-registry-name>.azurecr.io/<image-name>:<tag>
```

## Sample flow using Azure Logic Apps
<video width="320" height="240" controls>
  <source src="./assets/logic app.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>