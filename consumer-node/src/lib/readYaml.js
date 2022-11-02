import fs from "node:fs";
import path from "node:path";

import yaml from "js-yaml";

const file_path = path.resolve(
  process.cwd().toString(),
  "configs",
  "listeners.yaml"
);

export function getKafkaTopicAndItsListeners() {
  const listenersExists = fs.existsSync(file_path);
  if (!listenersExists) {
    throw new Error("Listener file not found.");
  }

  const doc = yaml.load(fs.readFileSync(file_path));

  // configs
  const configs = doc["configs"];
  if (!configs) {
    throw new Error("config file mismatch, no configs found");
  }

  // group_id
  const groupId = configs["group_id"];
  if (!groupId) {
    throw new Error("config file mismatch, no group_id found");
  }

  // consumers
  const consumers = configs["consumers"];
  if (!consumers) {
    throw new Error("config file mismatch, no consumers found");
  }

  const listeners = {};

  for (const consumer of consumers) {
    const topic = consumer["topic"];
    if (!Array.isArray(listeners[topic])) {
      listeners[topic] = [];
    }
    for (const l of consumer["listeners"]) {
      listeners[topic].push(l["host"] + "/" + l["path"]);
    }
  }

  return { groupId, listeners };
}
