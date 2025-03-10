#!/usr/bin/env python
import os
import pathlib
import sys

test_apps = [
    "admin_changelist",
    "admin_checks",
    "admin_custom_urls",
    "admin_docs",
    "admin_filters",
    "admin_inlines",
    "admin_ordering",
    "admin_scripts",
    "admin_utils",
    "admin_views",
    "admin_widgets",
    "aggregation",
    "aggregation_regress",
    "annotations",
    "apps",
    "async",
    "auth_tests",
    "backends",
    "basic",
    "bulk_create",
    "cache",
    "check_framework",
    "constraints",
    "contenttypes_tests",
    "context_processors",
    "custom_columns",
    "custom_lookups",
    "custom_managers",
    "custom_pk",
    "datatypes",
    "dates",
    "datetimes",
    "db_functions",
    "defer",
    "defer_regress",
    "delete",
    "delete_regress",
    "empty",
    "empty_models",
    "expressions",
    "expressions_case",
    "field_defaults",
    "file_storage",
    "file_uploads",
    "fixtures",
    "fixtures_model_package",
    "fixtures_regress",
    "flatpages_tests",
    "force_insert_update",
    "foreign_object",
    "forms_tests",
    "from_db_value",
    "generic_inline_admin",
    "generic_relations",
    "generic_relations_regress",
    "generic_views",
    "get_earliest_or_latest",
    "get_object_or_404",
    "get_or_create",
    "i18n",
    "indexes",
    "inline_formsets",
    "introspection",
    "invalid_models_tests",
    "known_related_objects",
    "lookup",
    "m2m_and_m2o",
    "m2m_intermediary",
    "m2m_multiple",
    "m2m_recursive",
    "m2m_regress",
    "m2m_signals",
    "m2m_through",
    "m2m_through_regress",
    "m2o_recursive",
    "managers_regress",
    "many_to_many",
    "many_to_one",
    "many_to_one_null",
    "max_lengths",
    "messages_tests",
    "migrate_signals",
    "migration_test_data_persistence",
    "migrations",
    "model_fields",
    "model_forms",
    "model_formsets",
    "model_formsets_regress",
    "model_indexes",
    "model_inheritance",
    "model_inheritance_regress",
    "model_options",
    "model_package",
    "model_regress",
    "model_utils",
    "modeladmin",
    "multiple_database",
    "mutually_referential",
    "nested_foreign_keys",
    "null_fk",
    "null_fk_ordering",
    "null_queries",
    "one_to_one",
    "or_lookups",
    "order_with_respect_to",
    "ordering",
    "pagination",
    "prefetch_related",
    "proxy_model_inheritance",
    "proxy_models",
    "queries",
    "queryset_pickle",
    "redirects_tests",
    "reserved_names",
    "reverse_lookup",
    "save_delete_hooks",
    "schema",
    "select_for_update",
    "select_related",
    "select_related_onetoone",
    "select_related_regress",
    "serializers",
    "servers",
    "sessions_tests",
    "shortcuts",
    "signals",
    "sitemaps_tests",
    "sites_framework",
    "sites_tests",
    "string_lookup",
    "swappable_models",
    "syndication_tests",
    "test_client",
    "test_client_regress",
    "test_runner",
    "test_utils",
    "timezones",
    "transactions",
    "unmanaged_models",
    "update",
    "update_only_fields",
    "user_commands",
    "validation",
    "view_tests",
    "xor_lookups",
    # Add directories in django_mongodb_backend/tests
    *sorted(
        [
            x.name
            for x in (pathlib.Path(__file__).parent.parent.parent.resolve() / "tests").iterdir()
        ]
    ),
]
runtests = pathlib.Path(__file__).parent.resolve() / "runtests.py"
run_tests_cmd = f"python3 {runtests} %s --settings mongodb_settings -v 2"

shouldFail = False
for app_name in test_apps:
    res = os.system(run_tests_cmd % app_name)  # noqa: S605
    if res != 0:
        shouldFail = True
sys.exit(1 if shouldFail else 0)
