Do a head to head comparison of rabbitMQ and google pub-sub in the context of a task os designing an event-based chat system with multiple microservices interacting with each other through a message queue.

Make sure to highlight at least (but not only) the following questions:
1. Ease of maintenance
2. Average latency (especially on low to medium load)
3. Are there mechanisms to ensure the delivery to a particular consumer? For example if one service instance sends a message to another service, I want the response to be sent to the same instance that sent the initial message.