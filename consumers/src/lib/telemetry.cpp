
#include <opentelemetry/exporters/otlp/otlp_grpc_exporter.h>
#include <opentelemetry/sdk/trace/samplers/always_on.h>
#include <opentelemetry/sdk/trace/processor.h>
#include <opentelemetry/sdk/trace/simple_processor.h>
#include <opentelemetry/sdk/trace/tracer_provider.h>
#include <opentelemetry/trace/provider.h>
#include <opentelemetry/sdk/trace/batch_span_processor.h>

void setUpTelemetry()
{
    // resources
    auto resource_attributes = opentelemetry::sdk::resource::ResourceAttributes{
        {"service.namespace", "shop"},
        {"service.name", std::getenv("SERVICE_NAME")},
        {"service.instance.id", std::getenv("HOSTNAME")},
        {"service.version", "v1.0.0"}};
    auto resource = opentelemetry::sdk::resource::Resource::Create(resource_attributes);

    // exporter
    opentelemetry::exporter::otlp::OtlpGrpcExporterOptions opts;
    opts.endpoint = std::getenv("LOG_COLLECTOR_ENDPOINT");
    opts.use_ssl_credentials = true;
    opts.ssl_credentials_cacert_as_string = "ssl-certificate";
    auto exporter =
        std::unique_ptr<opentelemetry::sdk::trace::SpanExporter>(opentelemetry::exporter::otlp::OtlpGrpcExporter(opts));

    // exporter
    opentelemetry::sdk::trace::BatchSpanProcessorOptions options;
    auto processor = std::unique_ptr<opentelemetry::sdk::trace::SpanProcessor>(
        opentelemetry::sdk::trace::BatchSpanProcessor(std::move(exporter), options));

    // sampler
    // auto sampler = std::unique_ptr<opentelemetry::sdk::trace::Sampler>(new opentelemetry::sdk::trace::AlwaysOnSampler);

    // trace provider
    auto provider = opentelemetry::nostd::shared_ptr<opentelemetry::trace::TracerProvider>(opentelemetry::sdk::trace::TracerProvider(std::move(processor),
                                                                                                                                     resource));

    // set the global tracer TraceProvider
    opentelemetry::trace::Provider::SetTracerProvider(std::move(provider));
}