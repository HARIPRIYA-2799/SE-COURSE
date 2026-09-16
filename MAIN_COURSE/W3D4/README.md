# 🍳 Slack Recipe Assistant with n8n + AI

A beginner-friendly n8n automation that works entirely inside Slack. A user types a recipe name in a Slack channel, an AI generates the products and ingredients needed, and the workflow posts the response back to the same Slack channel.

## 📌 Problem Statement

Build an n8n workflow that:

1. Listens for a recipe name in Slack.
2. Sends the recipe request to an AI model.
3. Generates a list of required products and ingredients.
4. Replies in the same Slack channel.

**Difficulty:** Beginner to Medium  
**Tools:** n8n, Slack, and an LLM

---

## 🏗️ Workflow Overview

```text
Slack Trigger
      ↓
AI Agent
      ↓
Slack - Send Message
```

### Workflow Flow

1. A user sends a recipe name in Slack.
2. The Slack Trigger receives the message.
3. The AI Agent identifies the ingredients and products needed.
4. The Slack node posts the AI-generated response in the original channel.

---

## 🧰 Prerequisites

Before starting, make sure you have:

- An active n8n instance (cloud or self-hosted).
- A Slack workspace where you can install an app.
- Permission to create and configure a Slack app.
- An API key or credentials for your selected LLM provider.
- A Slack test channel, such as `#recipe-bot`.

---

## 🔐 1. Configure the Slack App

1. Open the [Slack API Apps page](https://api.slack.com/apps).
2. Click **Create New App**.
3. Select **From scratch**.
4. Choose your Slack workspace.
5. Give the app a name, such as `n8n Recipe Assistant`.

### Recommended Slack Permissions

Under **OAuth & Permissions**, configure the permissions required by your workflow.

Common permissions include:

| Permission | Purpose |
|---|---|
| `chat:write` | Send messages to Slack |
| `channels:read` | Access public channel information |
| `channels:history` | Read public channel messages, when required |

Additional permissions may be needed depending on the Slack Trigger event and channel type.

Install the app in your workspace and configure the corresponding Slack credentials in n8n.

> Never commit Slack tokens or API keys to GitHub.

---

## 📥 2. Configure the Slack Trigger

1. Open n8n and create a new workflow.
2. Add a **Slack Trigger** node.
3. Create or select your Slack credentials.
4. Choose the event for receiving new messages.
5. Configure the channel or event settings supported by your n8n version.

### Slack Event Subscriptions

Depending on the trigger configuration:

1. Open your Slack app.
2. Navigate to **Event Subscriptions**.
3. Enable events.
4. Add the n8n webhook URL as the **Request URL**.
5. Configure the required bot events.

Your n8n instance must be reachable by Slack for webhook delivery.

### Test the Trigger

Send a message such as:

```text
Pizza
```

Inspect the trigger output and identify:

- The recipe text field.
- The Slack channel ID.

The exact output structure may vary by node version and event type.

---

## 🤖 3. Configure the AI Agent

Add an **AI Agent** node after the Slack Trigger.

Connect a supported chat model, such as an OpenAI Chat Model, and configure the relevant credentials.

### Suggested AI Prompt

```text
You are a helpful recipe ingredient assistant.

The user will provide a recipe name.

Identify the ingredients and products needed to prepare that recipe.

Instructions:
1. List the ingredients clearly.
2. Include approximate quantities when reasonable.
3. Group similar ingredients where helpful.
4. Mention common optional ingredients separately.
5. Do not invent unusual ingredients unnecessarily.
6. If the recipe name is unclear, ask the user for clarification.
7. Return a concise, Slack-friendly response.
8. Do not provide lengthy cooking instructions unless requested.

Recipe requested:
{{ $json.event.text }}
```

> The expression `{{ $json.event.text }}` is an example. Use the actual recipe text field shown in your Slack Trigger output.

### Example Input

```text
Chicken Biryani
```

### Example Output

```text
🛒 Ingredients for Chicken Biryani

- Basmati rice — 2 cups
- Chicken — 500 g
- Onion — 2 medium
- Tomato — 2
- Ginger-garlic paste — 1 tbsp
- Biryani spices — as needed
- Oil or ghee
- Salt
```

The exact ingredients and quantities depend on the AI model and recipe interpretation.

---

## 📤 4. Configure the Slack Send Message Node

1. Add a **Slack** node after the AI Agent.
2. Select the message-sending operation supported by your n8n version.
3. Select your Slack credentials.
4. Set the destination channel to the original Slack channel.
5. Set the message content to the AI Agent output.

### Message Expression

A commonly used AI Agent output field is:

```javascript
{{ $json.output }}
```

Confirm the actual output field in the AI Agent execution data.

### Same-Channel Expression

If the Slack Trigger output uses the structure shown below:

```json
{
  "event": {
    "text": "Pizza",
    "channel": "C123456"
  }
}
```

You can reference the original channel using:

```javascript
{{ $('Slack Trigger').item.json.event.channel }}
```

Replace the node name or field path if your actual data structure differs.

---

## 🧪 5. Test the Complete Workflow

1. Activate the workflow or start a test execution.
2. Open your Slack test channel.
3. Send a recipe name, for example:

```text
Pasta Alfredo
```

4. Check the Slack Trigger output.
5. Check the AI Agent output.
6. Check the Slack Send Message node.
7. Confirm that the answer appears in the same Slack channel.

### Expected Result

```text
🛒 Ingredients for Pasta Alfredo

- Pasta
- Butter
- Cream
- Parmesan cheese
- Garlic
- Salt and pepper
```

---

## 🛠️ Troubleshooting

| Problem | Possible Solution |
|---|---|
| Slack Trigger receives no messages | Check event subscriptions, webhook URL, and channel access |
| Recipe text is empty | Inspect the Slack Trigger output and update the expression |
| AI output is empty | Check the AI Agent and chat model credentials |
| Slack message fails | Verify Slack credentials and `chat:write` permission |
| Reply goes to the wrong channel | Reference the original channel ID from the trigger |
| Bot triggers itself repeatedly | Filter out bot-generated messages |

### Avoid Infinite Loops

If the Slack Trigger receives messages posted by the bot, the workflow may trigger itself.

Add a filtering condition to ignore bot-generated events when necessary. Inspect your Slack event payload to determine the appropriate bot-related field.

---

## 🔒 Security Best Practices

- Do not commit Slack tokens, API keys, or credentials.
- Use n8n credentials rather than hardcoding secrets.
- Give your Slack app only the permissions it needs.
- Test the workflow in a dedicated Slack channel.
- Consider filtering unsupported or empty recipe requests.
- Review AI-generated ingredient lists before relying on them for dietary or allergy-sensitive use cases.

---

## 🚀 Possible Improvements

You can extend the workflow with:

- Ingredient quantities and serving sizes.
- Dietary preferences, such as vegetarian or vegan.
- Shopping list formatting.
- Google Sheets integration.
- Grocery store API integration.
- Recipe clarification questions.
- Error handling and fallback responses.
- AI-generated cooking instructions on request.

### Example Extended Workflow

```text
Slack Trigger
      ↓
Filter Bot Messages
      ↓
AI Agent
      ↓
Format Response
      ↓
Slack - Send Message
```

---

## 📚 Useful Resources

- [n8n Documentation](https://docs.n8n.io/)
- [n8n Slack Integration](https://n8n.io/integrations/slack/)
- [n8n Slack Credentials](https://docs.n8n.io/integrations/builtin/credentials/slack/)
- [Slack API Documentation](https://api.slack.com/)
- [Slack Event Subscriptions](https://api.slack.com/apis/connections/events-api)

---

## ✅ Final Workflow Checklist

- [ ] Slack app created.
- [ ] Slack permissions configured.
- [ ] Slack credentials added to n8n.
- [ ] Slack Trigger configured.
- [ ] Slack webhook or event subscription configured.
- [ ] AI Agent connected to a chat model.
- [ ] AI prompt configured.
- [ ] Slack Send Message node configured.
- [ ] Original channel ID mapped correctly.
- [ ] Workflow tested in Slack.
- [ ] Bot-loop protection considered.

---

## 📄 License

This project is provided for learning and educational purposes.
