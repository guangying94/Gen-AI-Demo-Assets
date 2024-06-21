const { app } = require('@azure/functions');

app.http('GetLLMResponse', {
    methods: ['POST'],
    authLevel: 'anonymous',
    handler: async (request, context) => {
        const requestBodyText = await request.text();
        const requestBody = JSON.parse(requestBodyText);

        let llmBody = {
            "history": requestBody.history,
            "question": requestBody.question,
            "roles": requestBody.roles
        };

        const requestHeader = new Headers({ "Content-Type": "application/json" });
        requestHeader.append("Authorization", "Bearer " + process.env.LLM_KEY);
        requestHeader.append("azureml-model-deployment", process.env.LLM_DEPLOYMENT_NAME);

        const response = await fetch(process.env.LLM_ENDPOINT, {
            method: "POST",
            body: JSON.stringify(llmBody),
            headers: requestHeader
        });

        if (response.ok) {
            const json = await response.json();
            context.log(json.response);
            return {body: json.response};
        }
        else {
            context.log(response.headers);
            context.log(response.body);
            throw new Error("Request failed with status code" + response.status);
        }
    }
});
