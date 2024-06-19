import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def hello_world(request):
    name = request.params.get('name', 'world')
    message = f"Welcome, {name}!\n"
    logger.info(f"hello_world endpoint called with name: {name}")
    return Response(message)

def get_patients(request):
    logger.info("get_patients endpoint called")
    response_data = json.dumps(patients)
    return Response(response_data, content_type='application/json')

def get_patient_by_id(request):
    patient_id = request.matchdict['id']
    logger.info(f"get_patient_by_id endpoint called with id: {patient_id}")
    patient = next((p for p in patients if p['id'] == patient_id), None)
    if patient:
        response_data = json.dumps(patient)
        return Response(response_data, content_type='application/json')
    else:
        logger.warning(f"Patient with id {patient_id} not found")
        return Response(status=404, body='Patient not found')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))  # Default to port 8000 if not set
    with Configurator() as config:
        config.add_route('hello', '/')
        config.add_view(hello_world, route_name='hello')

        config.add_route('get_patients', '/patients')
        config.add_view(get_patients, route_name='get_patients', renderer='json')

        config.add_route('get_patient_by_id', '/patients/{id}')
        config.add_view(get_patient_by_id, route_name='get_patient_by_id', renderer='json')

        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', port, app)
    logger.info(f"Starting server on port {port}...")
    server.serve_forever()
