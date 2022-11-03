import kafkajs from "kafkajs";

const { Kafka } = kafkajs;

export async function ListenToKafkaTopicsAndNotifyTheConsumers(
  groupId,
  consumers,
  kafka_brokers
) {
  const kafka = new Kafka({
    clientId: process.env["SERVICE_NAME"],
    brokers: [kafka_brokers],
  });

  const consumer = kafka.consumer({ groupId });
  try {
    await consumer.connect();

    const topics = Object.keys(consumers);
    console.log(`[+] Listening for topics ${topics}`);

    await consumer.subscribe({ topics, fromBeginning: false });

    await consumer.run({
      eachMessage: async ({ topic, partition, message }) => {
        const { headers, value, key, offset } = message;
        let traceparent;
        Object.keys(headers).forEach((key) => {
          if (key.toLocaleLowerCase() === "traceparent") {
            traceparent = headers[key].toString();
          }
        });
        const payload = value.toString();
        console.log(
          `[+] Received message with key  ${key}, topic -> ${topic} on Partition ${partition}, offset ${offset} , with payload  ${payload}`
        );
        try {
          await sendDataToConsumer(consumers[topic], payload, traceparent);
          console.log("✔️  Data Sent Successfully !!!");
        } catch (err) {
          console.log("Error Sending Data !!!");
        }
      },
    });
  } catch (err) {
    await consumer.disconnect();
    throw err;
  }
}

async function sendDataToConsumer(host, payload, traceparent) {
  console.log(`[+] Sending data to ${host}  ...`);
  const response = await fetch(`http://${host}`, {
    method: "POST",
    body: payload,
    headers: {
      "Content-type": "application/json",
      traceparent: traceparent,
    },
  });
  if (response.status !== 200) {
    throw Error(`cannot send data to ${host}`);
  }
}
