import kafkajs from "kafkajs";
import {
  SpanStatusCode,
  trace,
  ROOT_CONTEXT,
  propagation,
  SpanKind,
} from "@opentelemetry/api";
import {
  SemanticAttributes,
  MessagingOperationValues,
  MessagingDestinationKindValues,
} from "@opentelemetry/semantic-conventions";

const { Kafka } = kafkajs;
const serviceName = process.env["SERVICE_NAME"];

const bufferTextMapGetter = {
  get(carrier, key) {
    return carrier?.[key]?.toString();
  },

  keys(carrier) {
    return carrier ? Object.keys(carrier) : [];
  },
};

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
      eachMessage: async (kafkaPayload) => {
        const { topic, partition, message } = kafkaPayload;
        const { headers, value, key, offset } = message;

        // transparent: {version}-{trace_id}-{span_id}-{trace_flags}
        let traceparent;
        Object.keys(headers).forEach((key) => {
          if (key.toLowerCase() === "traceparent") {
            traceparent = headers[key].toString();
          }
        });
        const payload = value.toString();
        console.log(
          `[+] Received message with key  ${key}, topic -> ${topic} on Partition ${partition}, offset ${offset} , with payload  ${payload}`
        );

        const propagatedContext = propagation.extract(
          ROOT_CONTEXT,
          headers,
          bufferTextMapGetter
        );

        const span = tracer.startSpan(
          `${serviceName}`,
          {
            kind: SpanKind.CONSUMER,
            attributes: {
              [SemanticAttributes.MESSAGING_SYSTEM]: "kafka",
              [SemanticAttributes.MESSAGING_DESTINATION]: topic,
              [SemanticAttributes.MESSAGING_DESTINATION_KIND]:
                MessagingDestinationKindValues.TOPIC,
              [SemanticAttributes.MESSAGING_OPERATION]:
                MessagingOperationValues.PROCESS,
              [SemanticAttributes.MESSAGING_KAFKA_MESSAGE_KEY]: key,
              [SemanticAttributes.MESSAGING_KAFKA_PARTITION]: partition,
              offset: offset,
            },
          },
          propagatedContext
        );

        try {
          span.addEvent("log", {
            severity: "info",
            partition,
            topic,
            key,
            message: `Received kafka payload`,
          });
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
