import collections
import json
import os
import unittest

from dash.development.base_component import generate_class, Component, ISUNDEFINED, MUSTBEDEFINED
from dash.development.component_loader import load_components

METADATA_PATH = 'metadata.json'

METADATA_STRING = '''{
    "MyComponent.react.js": {
        "props": {
            "foo": {
                "type": {
                    "name": "number"
                },
                "required": false,
                "description": "Description of prop foo.",
                "defaultValue": {
                    "value": "42",
                    "computed": false
                }
            },
            "children": {
                "type": {
                    "name": "object"
                },
                "description": "Children",
                "required": false
            },
            "bar": {
                "type": {
                    "name": "custom"
                },
                "required": false,
                "description": "Description of prop bar.",
                "defaultValue": {
                    "value": "21",
                    "computed": false
                }
            },
            "baz": {
                "type": {
                    "name": "union",
                    "value": [
                        {
                            "name": "number"
                        },
                        {
                            "name": "string"
                        }
                    ]
                },
                "required": false,
                "description": ""
            }
        },
        "description": "General component description.",
        "methods": []
    },
    "A.react.js": {
        "description": "",
        "methods": [],
        "props": {
            "href": {
                "type": {
                    "name": "string"
                },
                "required": false,
                "description": "The URL of a linked resource."
            },
            "children": {
                "type": {
                    "name": "object"
                },
                "description": "Children",
                "required": false
            }
        }
    }
}'''
METADATA = json \
    .JSONDecoder(object_pairs_hook=collections.OrderedDict) \
    .decode(METADATA_STRING)


class TestLoadComponents(unittest.TestCase):
    def setUp(self):
        with open(METADATA_PATH, 'w') as f:
            f.write(METADATA_STRING)

    def tearDown(self):
        os.remove(METADATA_PATH)

    def test_loadcomponents(self):
        scope = {"Component": Component, "ISUNDEFINED": ISUNDEFINED, "MUSTBEDEFINED": MUSTBEDEFINED}

        MyComponent = generate_class(
            'MyComponent',
            METADATA['MyComponent.react.js']['props'],
            METADATA['MyComponent.react.js']['description'],
            'default_namespace'
        )
        exec(MyComponent, scope)
        MyComponent = scope['MyComponent']

        A = generate_class(
            'A',
            METADATA['A.react.js']['props'],
            METADATA['A.react.js']['description'],
            'default_namespace'
        )
        exec(A, scope)
        A = scope['A']

        c = load_components(METADATA_PATH)
        import metadata as c

        MyComponentKwargs = {
            'foo': 'Hello World',
            'bar': 'Lah Lah',
            'baz': 'Lemons',
            'children': 'Child'
        }
        AKwargs = {
            'children': 'Child',
            'href': 'Hello World'
        }

        self.assertTrue(
            isinstance(MyComponent(**MyComponentKwargs), Component)
        )

        self.assertEqual(
            repr(MyComponent(**MyComponentKwargs)),
            repr(getattr(c, c.__all__[0])(**MyComponentKwargs))
        )

        self.assertEqual(
            repr(A(**AKwargs)),
            repr(getattr(c, c.__all__[1])(**AKwargs))
        )
