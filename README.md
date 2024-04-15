# real-estate-backend
This is a Real Estate Application that leverages AI for enhanced functionality.

## Setup

Follow these steps to set up the project:

1. Install Django:
   Use the following command to install Django:
   ```pip install Django```

2. Start the Django project:
   Use the following command to start the Django project:
   ```django-admin startproject tappy .```

3. Start the Django app:
   Use the following command to start the Django app:
   ```python manage.py startapp common```

# Unit Testing

Here are some instructions for running unit tests:

### Running the unit tests using coverage:
   Use the following command to run the unit tests using coverage:
   ```
   coverage run manage.py test
   docker exec -it real-estate-backend_django_1 coverage run manage.py test
   ```

### Adding verbosity (level 2 is recommended):
   Use the following command to add verbosity:
   ```
   coverage run manage.py test -v 2 --no-logs
   docker exec -it real-estate-backend_django_1 coverage run manage.py test -v 2 --no-logs
   ```

### Running a specific test case:
   Use the following command to run a specific test case:
   ```
   coverage run manage.py test domain.users.tests -v 2
   ```

### Generating the coverage report:
   Use the following commands to generate the coverage report:
   ```
   coverage html
   docker exec -it real-estate-backend_django_1 coverage html

   or

   coverage report
   ```

### Combining all test commands:
   Use the following commands to run all tests and generate a coverage report:
   ```
   docker exec -it real-estate-backend_django_1 coverage run manage.py test
   docker exec -it real-estate-backend_django_1 coverage html
   open htmlcov/index.html
   ```

### Project Roadmap

Here is a sample roadmap for this project:
- [x] Authentication
- [x] Lead Model
- [x] System Model
- [x] Send Page Message
- [x] Messaging Webhooks (Sent and Received messages)
- [ ] Properties and Property Details (FAQ or Details for RAG)
- [ ] Question and Answer model for ChatGPT Custom Model :)
- [x] Facebook Messages Sync
- [ ] Facebook Page Integration / Login with Facebook (Select Page)
- [ ] Manage Page Subscribers
- [ ] Page Broadcast Message


### NGROK

ngrok config add-authtoken <token>

### Facebook Webhooks

- https://developers.facebook.com/docs/messenger-platform/webhooks/
- https://developers.facebook.com/docs/messenger-platform/reference/send-api/
- https://support.manychat.com/support/solutions/articles/36000195552-message-tags

- https://www.facebook.com/settings/?tab=advanced_messaging
- App settings > Handover protocol > Messenger receiver > Tappy

- https://support.manychat.com/en/support/solutions/articles/36000103309-handover-protocol
- Closing the Conversation in Manychat will fixed the: "Message failed to send because another app is controlling this thread now"

- To disable Handover protocol, head to the same place. Click on an app again. That will de-select it and the "Select" option will remain. Handover's disabled.
- After any change, make sure to Refresh Permissions through the Help button.

## NOTES:

1. During ads Enable the Handover protocol and refresh permission
2. Must closed the conversation once done so that we can received the webhook for this user conversation
3. Add Sync button to sync-messages after interacting with Manychats

## NOTE: WORKING WITH MANYCHAT

1. Allow ManyChat to Handle automation
2. Once done, with automation Close the conversation in ManyChat
3. Sync conversations on Real Estate App
4. Start conversations
5. To start automationn again in Manychat Re-open conversation

## Goal

1. Get Rid of Manychat (Remove from Page Integration via Manychat Interface or Page Advance Messaging)
2. Setup Async Task for Get Started, Details Conversation Flow
3. 