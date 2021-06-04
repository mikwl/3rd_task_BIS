"""As the first task you should use pet swagger:
https://petstore.swagger.io/Endpoint - users.
You need to write CRUD operation tests for testing this  endpoint."""

import unittest.mock
import re
import os.path as osp
import json

import responses

import swaggerconformance
import swaggerconformance.response


TEST_SCHEMA_DIR = osp.relpath(osp.join(osp.dirname(osp.realpath(__file__)),
                                       'test_schemas/'))
TEST_SCHEMA_PATH = osp.join(TEST_SCHEMA_DIR, 'test_schema.json')
FULL_PUT_SCHEMA_PATH = osp.join(TEST_SCHEMA_DIR, 'full_put_schema.json')
ALL_CONSTRAINTS_SCHEMA_PATH = osp.join(TEST_SCHEMA_DIR,
                                       'all_constraints_schema.json')
PETSTORE_SCHEMA_PATH = osp.join(TEST_SCHEMA_DIR, 'petstore.json')
UBER_SCHEMA_PATH = osp.join(TEST_SCHEMA_DIR, 'uber.json')
MIRROR_REQS_SCHEMA_PATH = osp.join(TEST_SCHEMA_DIR, 'mirror_requests.json')
SCHEMA_URL_BASE = 'http://127.0.0.1:5000/api'
CONTENT_TYPE_JSON = 'application/json'


def _respond_to_method(method, path, response_json, status, content_type):
    url_re = re.compile(SCHEMA_URL_BASE + path + '$')
    responses.add(method, url_re, json=response_json, status=status,
                  content_type=content_type)

def respond_to_get(path, response_json=None, status=200,
                   content_type=CONTENT_TYPE_JSON):
    _respond_to_method(responses.GET, path, response_json, status,
                       content_type)

def respond_to_post(path, response_json=None, status=200,
                    content_type=CONTENT_TYPE_JSON):
    _respond_to_method(responses.POST, path, response_json, status,
                       content_type)

def respond_to_put(path, response_json=None, status=200,
                   content_type=CONTENT_TYPE_JSON):
    _respond_to_method(responses.PUT, path, response_json, status,
                       content_type)

def respond_to_delete(path, response_json=None, status=200,
                      content_type=CONTENT_TYPE_JSON):
    _respond_to_method(responses.DELETE, path, response_json, status,
                       content_type)


class APITemplateTestCase(unittest.TestCase):

    def setUp(self):
        self.client = swaggerconformance.client.Client(TEST_SCHEMA_PATH)

    def tearDown(self):
        pass

    def test_schema_parse(self):
        api_template = swaggerconformance.schema.Api(self.client)
        expected_endpoints = {'/schema', '/apps', '/apps/{appid}'}
        self.assertSetEqual(set(api_template.endpoints.keys()),
                            expected_endpoints)

    @responses.activate
    def test_endpoint_manually(self):
        api_template = swaggerconformance.schema.Api(self.client)

        app_id_get_op = None
        for operation_template in api_template.operations():
            if (operation_template.method == 'get' and
                    operation_template.path == '/apps/{appid}'):
                self.assertIsNone(app_id_get_op)
                app_id_get_op = operation_template
        self.assertIsNotNone(app_id_get_op)

        self.assertSetEqual(set(app_id_get_op.parameters.keys()),
                            {'appid', 'X-Fields'})
        self.assertEqual(app_id_get_op.parameters['appid'].type, 'string')

        params = {'appid': 'test_string'}
        respond_to_get('/apps/test_string',
                       response_json={'name': 'abc', 'data': {}},
                       status=200)
        result = self.client.request(app_id_get_op, params)
        self.assertEqual(result.status, 200)
        self.assertEqual(json.loads(result.raw.decode('utf-8')), result.body)

    def test_operation_access(self):
        api_template = swaggerconformance.schema.Api(self.client)
        self.assertEqual(api_template.endpoints['/apps/{appid}']['get'],
                         api_template.operation('get_apps_resource'))

class BasicConformanceAPITestCase(unittest.TestCase):

    @responses.activate
    def test_immediate_failure(self):
        respond_to_get('/schema')
        respond_to_get('/apps', status=500)
        respond_to_get(r'/apps/.+', status=404)
        respond_to_put(r'/apps/.+', status=204)
        respond_to_delete(r'/apps/.+', status=204)

        self.assertRaises(AssertionError,
                          swaggerconformance.api_conformance_test,
                          TEST_SCHEMA_PATH,
                          cont_on_err=False)

    @responses.activate
    def test_deferred_failure(self):
        """Errors should be counted and reported in a single exception."""
        respond_to_get('/schema')
        respond_to_get('/apps', status=500)
        respond_to_get(r'/apps/.+', status=500)
        respond_to_put(r'/apps/.+', status=500)
        respond_to_delete(r'/apps/.+', status=204)

        self.assertRaisesRegex(Exception,
                               r"3 operation\(s\) failed",
                               swaggerconformance.api_conformance_test,
                               TEST_SCHEMA_PATH,
                               cont_on_err=True)

    @responses.activate
    def test_running_as_module(self):
        from swaggerconformance.__main__ import main as dunder_main
        respond_to_get('/schema')
        respond_to_get('/apps', status=500)
        respond_to_get(r'/apps/.+', status=500)
        respond_to_put(r'/apps/.+', status=500)
        respond_to_delete(r'/apps/.+', status=204)

        self.assertRaisesRegex(Exception,
                               r"3 operation\(s\) failed",
                               dunder_main,
                               [TEST_SCHEMA_PATH])

    @responses.activate
    def test_content_type_header_with_parameters(self):
        content_type_extra = 'application/json; charset=utf-8'
        respond_to_get('/schema')
        respond_to_get('/apps',
                       response_json=[{'name': 'test'}],
                       content_type=content_type_extra)
        respond_to_get(r'/apps/.+', status=404,
                       content_type=content_type_extra)
        respond_to_put(r'/apps/.+', status=204,
                       content_type=content_type_extra)
        respond_to_delete(r'/apps/.+', status=204,
                          content_type=content_type_extra)

        swaggerconformance.api_conformance_test(TEST_SCHEMA_PATH,
                                                cont_on_err=False)


class ParameterTypesTestCase(unittest.TestCase):

    @responses.activate
    def test_full_put(self):
        respond_to_get('/example')
        respond_to_delete('/example', status=204)
        respond_to_put(r'/example/-?\d+', status=204)

        swaggerconformance.api_conformance_test(FULL_PUT_SCHEMA_PATH,
                                                cont_on_err=False)

    @responses.activate
    def test_all_constraints(self):
        respond_to_get('/schema')
        respond_to_put(r'/example/-?\d+', status=204)

        swaggerconformance.api_conformance_test(ALL_CONSTRAINTS_SCHEMA_PATH,
                                                cont_on_err=False)


class ExternalExamplesTestCase(unittest.TestCase):

    @responses.activate
    def test_swaggerio_petstore(self):
        user = {"id": 0,
                "username": "string",
                "firstName": "string",
                "lastName": "string",
                "email": "string",
                "password": "string",
                "phone": "string",
                "userStatus": 0}

        respond_to_get('/user')
        respond_to_post('/user')
        respond_to_delete('/user')
        respond_to_get(r'/user/(?!login).+', response_json=user)
        respond_to_put(r'/user/(?!login).+')
        respond_to_delete(r'/user/(?!login).+')
        respond_to_get(r'/user/login\?username=.*&password=.*',
                       response_json="example")
        respond_to_get('/user/logout')
        respond_to_post('/user/createWithArray')
        respond_to_post('/user/createWithList')
        respond_to_put(r'/example/-?\d+')

        swaggerconformance.api_conformance_test(PETSTORE_SCHEMA_PATH,
                                                cont_on_err=False)