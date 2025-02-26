from django.core.exceptions import FieldDoesNotExist
from django.db import connection
from django.test import TestCase

from django_mongodb_backend.indexes import AtlasSearchIndex

from .models import Article


class PartialIndexTests(TestCase):
    # Schema editor is used to  create the index to test that it works.
    # available_apps = ["indexes"]
    available_apps = None

    def assertAddRemoveIndex(self, editor, model, index):
        editor.add_index(index=index, model=model)
        self.assertIn(
            index.name,
            connection.introspection.get_constraints(
                cursor=None,
                table_name=model._meta.db_table,
            ),
        )
        editor.remove_index(index=index, model=model)
        self.assertNotIn(
            index.name,
            connection.introspection.get_constraints(
                cursor=None,
                table_name=model._meta.db_table,
            ),
        )

    def test_simple_atlas_index(self):
        with connection.schema_editor() as editor:
            index = AtlasSearchIndex(
                name="recent_article_idx",
                fields=["number"],
            )
            editor.add_index(index=index, model=Article)
            self.assertAddRemoveIndex(editor, Article, index)

    def test_multiple_fields_atlas_index(self):
        with connection.schema_editor() as editor:
            index = AtlasSearchIndex(
                name="recent_article_idx",
                fields=["headline", "number", "body", "data", "embedded", "auto_now"],
            )
            editor.add_index(index=index, model=Article)
            index_info = connection.introspection.get_constraints(
                cursor=None,
                table_name=Article._meta.db_table,
            )
            expected_options = {
                "dynamic": False,
                "fields": {
                    "auto_now": {"type": "date"},
                    "body": {
                        "indexOptions": "offsets",
                        "norms": "include",
                        "store": True,
                        "type": "string",
                    },
                    "data": {"dynamic": False, "fields": {}, "type": "document"},
                    "embedded": {"dynamic": False, "fields": {}, "type": "embeddedDocuments"},
                    "headline": {
                        "indexOptions": "offsets",
                        "norms": "include",
                        "store": True,
                        "type": "string",
                    },
                    "number": {
                        "indexDoubles": True,
                        "indexIntegers": True,
                        "representation": "double",
                        "type": "number",
                    },
                },
            }
            self.assertCountEqual(index_info[index.name]["columns"], index.fields)
            self.assertEqual(index_info[index.name]["options"], expected_options)
            self.assertAddRemoveIndex(editor, Article, index)

    def test_field_not_exists(self):
        index = AtlasSearchIndex(
            name="recent_article_idx",
            fields=["headline", "number1"],
        )
        with connection.schema_editor() as editor:
            msg = "Article has no field named 'number1'"
            with self.assertRaisesMessage(
                FieldDoesNotExist, msg
            ), connection.schema_editor() as editor:
                editor.add_index(index=index, model=Article)
