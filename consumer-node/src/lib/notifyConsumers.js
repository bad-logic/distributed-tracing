import kafkajs from "kafkajs";
import { SpanStatusCode, trace } from "@opentelemetry/api";

const { Kafka } = kafkajs;
const serviceName = process.env["SERVICE_NAME"];

export async function ListenToKafkaTopicsAndNotifyTheConsumers(
  groupId,
  consumers,
  kafka_brokers
) {
  const kafka = new Kafka({
    clientId: serviceName,
    brokers: [kafka_brokers],
  });

  const consumer = kafka.consumer({ groupId });
  try {
    await consumer.connect();

    const topics = Object.keys(consumers);
    console.log(`[+] Listening for topics ${topics}`);

    await consumer.subscribe({ topics, fromBeginning: false });

    const tracer = trace.getTracer(serviceName);
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

        tracer.startActiveSpan(`${serviceName}`, async (span) => {
          span.setAttribute("key", key);
          span.setAttribute("partition", partition);
          span.setAttribute("offset", offset);
          span.setAttribute("topic", topic);

          try {
            await sendDataToConsumer(consumers[topic], payload, traceparent);
            console.log("✔️  Data Sent Successfully !!!");
            span.addEvent("log", {
              severity: "info",
              message: `Successfully exported data to ${consumers[topic]}.`,
            });
          } catch (err) {
            console.log("Error Sending Data !!!", err);
            span.recordException(err);
            span.setStatus({ code: SpanStatusCode.ERROR });
            span.addEvent("log", {
              severity: "critical",
              message: `unable to send data to ${consumers[topic]}.`,
            });
          } finally {
            span.end();
          }
        });
      },
    });

    ["SIGINT", "SIGTERM"].forEach((signal) => {
      process.on(signal, () => consumer.disconnect().catch(console.error));
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
