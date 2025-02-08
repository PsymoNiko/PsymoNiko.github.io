from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter, SimpleSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import Resource

from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def configure_tracing(service_name="aliiiiiiiiiiiiiiiiiiiiiiiiiii"):
    try:
        # Set up the Tracer Provider with a service name

        resource = Resource.create({"service.name": service_name})

        print("ldfjslkdjflskdjflskdjflksjflksdjdflksjdlfkjsldkfjslkdfj")
        print(resource)
        provider = TracerProvider(resource=resource)
        trace.set_tracer_provider(provider)

        # Configure Jaeger Exporter
        jaeger_host = os.getenv("JAEGER_AGENT_HOST", "localhost")
        jaeger_port = int(os.getenv("JAEGER_AGENT_PORT", 6831))

        jaeger_exporter = JaegerExporter(
            agent_host_name=jaeger_host,
            agent_port=jaeger_port,
        )

        # Add the Jaeger exporter to the TracerProvider
        span_processor = BatchSpanProcessor(jaeger_exporter)
        provider.add_span_processor(span_processor)

        # Optionally add ConsoleSpanExporter for debugging
        console_exporter = ConsoleSpanExporter()
        provider.add_span_processor(SimpleSpanProcessor(console_exporter))

        # Instrument Django and additional libraries
        DjangoInstrumentor().instrument()
        RequestsInstrumentor().instrument()
        Psycopg2Instrumentor().instrument()

        logger.info(f"Tracing configured. Exporting to Jaeger at {jaeger_host}:{jaeger_port}")
    except Exception as e:
        logger.error(f"Error configuring tracing: {e}")

# Call the tracing configuration function at the start of your application
configure_tracing()



