Below is a comprehensive, step-by-step guide for you to obtain and securely store API keys for both OpenAI ChatGPT and Anthropic Claude. It assumes you already have active accounts but need to know exactly where to navigate in each console to generate keys, fund your projects, and follow best practices for management.

## How to get an API key: OpenAI ChatGPT

1. **Log in to the OpenAI Platform**
   Go to [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys) and sign in with your ChatGPT credentials if prompted.

2. **Create a Project**
   Navigate to [https://platform.openai.com/settings/organization/projects](https://platform.openai.com/settings/organization/projects) and click **+ Create**, enter a project name (e.g., “LLM Course”), then click **Create**.

3. **Set up Billing (Add Prepaid Credits)**
   In the left-hand menu under **Billing**, click **Add payment method**, enter your credit card details, then purchase the minimum \$5 to fund your project.

4. **Generate Your API Key**
   Within your project, go to the **API Keys** tab, click **+ Create new secret key**, give it a descriptive name (e.g., “Course Project Key”), and click **Create**. 

5. **Copy and Secure Your Key**
   The full secret key string will be displayed **only once**—**copy** it immediately and store it in a password manager or secure vault. You will not be able to view it again. 

### Best Practices

* Rotate keys every 90 days and revoke any that are no longer in use to limit exposure if compromised.
* Monitor your usage via the **Usage** dashboard at [https://platform.openai.com/account/usage](https://platform.openai.com/account/usage) or the **Usage** tab under Settings. 
* Never commit API keys to version control—add them to `.gitignore` or use secret-management tools
  
---

## How to get an API key: Anthropic Claude

1. **Log in to the Anthropic Console**
   Navigate to [https://console.anthropic.com](https://console.anthropic.com) and sign in with your Claude account credentials.

2. **Access the API Keys Section**
   Click **the key icon** in the left-hand navigation. 

3. **Generate a New API Key**
   On the **API Keys** page, click **+ Create Key**, enter a descriptive name (e.g., “Course Key”), and click **Add**. 

4. **Copy and Secure Your Key**
   The full API key string is shown **only once**—**copy** it immediately and store it in a secure vault. You will not be able to view it again.

5. **Set Up Billing or Claim Free Credits**
   In the left navigation, select **Billing**. If you have trial credits, you may need to verify your phone number to claim them; otherwise, under **Buy credits** purchase the minimum \$5 to fund your usage. 

### Best Practices

* Rotate keys periodically and delete any unused or compromised keys to maintain security. 
* Never expose keys in public repositories—use environment variables or secret managers and add any config files with keys to `.gitignore`. 
* Monitor your credit balance and API usage in **Billing** to avoid unexpected costs.
