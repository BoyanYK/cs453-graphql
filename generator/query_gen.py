from py_gql import build_schema
from py_gql.lang.ast import UnionTypeDefinition
from copy import deepcopy
import subprocess
from os import listdir
from os.path import isfile, join

from generator.utils import get_field_args_dict, get_args_to_vars_str, get_vars_to_types_str

def get_query_dict(sdl_path, depth_limit=100, include_deprecated_fields=True):
    """
    :param sdl_path: Path to an SDL file
    :param depth_limit: the maximum depth of nesting to probe
    :param include_deprecated_fields: whether to include deprecated fields
    :return: dictionary whose key is a function and whose value is the query string to the function
    """
    TAP_STRING = '    '

    def generate_subquery(cur_name,
                          cur_parent_type,
                          cur_parent_name=None,
                          arguments_dict=None,
                          duplicate_args_counts=None,
                          cross_reference_key_list=None,
                          cur_depth=1):
        if arguments_dict is None:
            arguments_dict = {}
        if duplicate_args_counts is None:
            duplicate_args_counts = {}
        if cross_reference_key_list is None:
            cross_reference_key_list = []

        field_args_dict= None

        field = gql_schema.get_type(cur_parent_type).field_map.get(cur_name)
        cur_type_name = field.type.type.name if hasattr(field.type, "type") else field.type.name
        cur_type = gql_schema.get_type(cur_type_name)

        query_str = ""
        child_query = ''

        if hasattr(cur_type, "fields") and cur_type.fields:
            cross_reference_key = "{}To{}Key".format(cur_parent_name, cur_name)

            if cross_reference_key in cross_reference_key_list or cur_depth > depth_limit:
                return ''
            cross_reference_key_list.append(cross_reference_key)

            if cur_type.fields != NotImplemented:
                child_keys = map(lambda x: x.name, cur_type.fields)
                child_keys = filter(
                    lambda field_name: include_deprecated_fields or not cur_type.field_map.get(
                        field_name).deprecated,
                    child_keys
                )

                child_query_list = []
                for child_key in child_keys:
                    res = generate_subquery(child_key, cur_type.name, cur_name,
                                            arguments_dict,
                                            duplicate_args_counts,
                                            deepcopy(cross_reference_key_list),
                                            cur_depth + 1)
                    if "query_str" in res:
                        child_query_list.append(res.get("query_str"))

                child_query = "\n".join(child_query_list)

        if not ((hasattr(cur_type, "fields") and cur_type.fields != NotImplemented) and (not child_query)):
            query_str = TAP_STRING * cur_depth + field.name
            if field.arguments.__len__() > 0:
                field_args_dict = get_field_args_dict(field, duplicate_args_counts, arguments_dict)
                arguments_dict.update(field_args_dict)
                query_str += "({})".format(get_args_to_vars_str(field_args_dict))
            if child_query:
                query_str += "{{\n{}\n{}}}".format(
                    child_query,
                    TAP_STRING * cur_depth
                )

        if hasattr(cur_type, "nodes") and cur_type.nodes and isinstance(cur_type.nodes[0], UnionTypeDefinition):
            types = cur_type.types

            if types:
                indent = TAP_STRING * cur_depth
                frag_indent = TAP_STRING * (cur_depth + 1)
                query_str += "{\n"

                for value_type_name in types:
                    value_type = gql_schema.get_type(value_type_name.name)

                    union_child_query_list = []
                    for cur in value_type.fields:
                        res = generate_subquery(cur.name, value_type.name, cur_name,
                                                arguments_dict,
                                                duplicate_args_counts,
                                                deepcopy(cross_reference_key_list),
                                                cur_depth + 2)
                        if "query_str" in res:
                            union_child_query_list.append(res.get("query_str"))

                        union_child_query = "\n".join(union_child_query_list)

                        query_str += "{}... on {} {{\n{}\n{}}}\n".format(
                            frag_indent, value_type_name.name, union_child_query, frag_indent
                        )
                query_str += indent + "}"

        return {
            'query_str': query_str,
            'arguments_dict': arguments_dict,
            'field_args_dict': field_args_dict
        }

    with open(sdl_path) as v:
        sdl = "".join(v.readlines())
        gql_schema = build_schema(sdl)

    if not gql_schema.query_type:
        return

    query_dict = {}

    for type in gql_schema.query_type.fields:
        field = gql_schema.get_type("Query").field_map.get(type.name)
        if not include_deprecated_fields and field.deprecated:
            continue
        query_result = generate_subquery(field.name, "Query")

        vars_to_types_str = get_vars_to_types_str(query_result["arguments_dict"])

        query = "{} {}{}{{\n{}\n}}".format(
            'query',
            type.name,
            ('(' + vars_to_types_str + ')') if vars_to_types_str else '',
            query_result["query_str"]
        )

        query_dict["resolve_{}".format(type.name)] = {
            'query' : query,
            'field_args_dict' : query_result["field_args_dict"]
        }

    return query_dict
