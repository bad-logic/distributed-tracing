import { Resource } from "@opentelemetry/resources";
import { SemanticResourceAttributes } from "@opentelemetry/semantic-conventions";
import { NodeTracerProvider } from "@opentelemetry/sdk-trace-node";
import { BatchSpanProcessor } from "@opentelemetry/sdk-trace-base";
import { OTLPTraceExporter } from "@opentelemetry/exporter-trace-otlp-grpc";

export function setupTelemetry() {
  const resource = Resource.default().merge(
    new Resource({
      [SemanticResourceAttributes.SERVICE_NAMESPACE]: "shop",
      [SemanticResourceAttributes.SERVICE_NAME]: process.env["SERVICE_NAME"],
      [SemanticResourceAttributes.SERVICE_INSTANCE_ID]: process.env["HOSTNAME"],
      [SemanticResourceAttributes.SERVICE_VERSION]: "v1.0.0",
    })
  );

  const exporter = new OTLPTraceExporter({
    url: `http://${process.env["LOG_COLLECTOR_ENDPOINT"]}`,
  });

  const processor = new BatchSpanProcessor(exporter);

  const provider = new NodeTracerProvider({
    resource: resource,
  });
  provider.addSpanProcessor(processor);

  provider.register();

  ["SIGINT", "SIGTERM"].forEach((signal) => {
    process.on(signal, () => provider.shutdown().catch(console.error));
  });
}
