"""This module implements the prometheus metrics API."""

from flask import Response

from flask_restplus import Namespace, Resource

from prometheus_client import CollectorRegistry, CONTENT_TYPE_LATEST, generate_latest, multiprocess

api = Namespace('metrics', description='Prometheus metrics')


@api.route('/')
class Metrics(Resource):
    """Resource providing metrics about this ml service."""

    def get(self):
        """Return the collected prometheus data."""
        registry = CollectorRegistry()
        multiprocess.MultiProcessCollector(registry)
        data = generate_latest(registry)
        return Response(data, mimetype=CONTENT_TYPE_LATEST)
