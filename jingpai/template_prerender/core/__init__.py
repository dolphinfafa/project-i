#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Django template preprocessor.
Author: Jonathan Slenders, City Live
"""
from jingpai.template_prerender.core.context import Context
from jingpai.template_prerender.core.django_processor import parse


def output_tree(tree):
    return tree.output_as_string()


def _default_loader(path):
    return open(path).read()


def render(code, path='', loader=None, options=None):
    """
    Compile the template, do everything, and return a single document
    as a string. The loader should look like: (lambda path: return code)
    and is called for the includes/extends.
    """
    tree, context = render_to_parse_tree(code, path, loader, options)

    # print(tree._print())
    # print(output_tree(tree))

    return output_tree(tree), context


def render_to_parse_tree(code, path='', loader=None, options=None):
    # Make the loader also parse the templates
    def new_loader(include_path):
        return parse((loader or _default_loader)(include_path), include_path, context)

    # Create preprocess context
    context = (Context)(new_loader, options)

    # Parse template, and return output
    return parse(code, path, context, main_template=True), context
