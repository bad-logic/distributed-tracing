import url from "node:url";
import { getKafkaTopicAndItsListeners } from "./lib/readYaml.js";
import { ListenToKafkaTopicsAndNotifyTheConsumers } from "./lib/notifyConsumers.js";

if (import.meta.url === url.pathToFileURL(process.argv[1]).href) {
  const errorTypes = ["unhandledRejection", "uncaughtException"];
  const signalTraps = ["SIGTERM", "SIGINT"];

  errorTypes.forEach((type) => {
    process.on(type, async (e) => {
      try {
        console.log(`process.on ${type}`);
        console.error(e);
        process.exit(0);
      } catch (_) {
        process.exit(1);
      }
    });
  });

  signalTraps.forEach((type) => {
    process.once(type, async () => {
      try {
        console.log(`Received ${type} signal`);
      } finally {
        process.kill(process.pid, type);
      }
    });
  });

  try {
    const kafkaBrokersList = process.env["KAFKA_BROKERS"];
    if (!kafkaBrokersList) {
      throw Error("KAFKA_BROKERS not provided");
    }
    const { groupId, listeners } = getKafkaTopicAndItsListeners();
    ListenToKafkaTopicsAndNotifyTheConsumers(
      groupId,
      listeners,
      kafkaBrokersList
    );
  } catch (err) {
    console.log("ERROR: ", err);
    process.exit(1);
  }
}
