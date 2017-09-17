#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Django template preprocessor.
Author: jmp0xf, Jonathan Slenders, City Live
"""
from jingpai.template_prerender.core.lexer import CompileException


class Context(object):
    """
    Preprocess context. Contains the render settings, error logging,
    remembers dependencies, etc...
    """

    def __init__(self, loader=None, extra_options=None, insert_debug_symbols=False):
        self.loader = loader
        self.insert_debug_symbols = insert_debug_symbols

        # Remember stuff
        self.warnings = []

        # template_dependencies: will contains all other templates which are
        # needed for compilation of this template.
        self.template_dependencies = []

        # Only direct dependencies (first level {% include %} and {% extends %})
        self.include_dependencies = []
        self.extends_dependencies = []

        # Process options
        self.options = Options()
        for o in extra_options or []:
            self.options.change(o)

    def raise_warning(self, node, message):
        """
        Log warnings: this will not raise an exception. So, preprocessing
        for the current template will go on. But it's possible to retreive a
        list of all the warnings at the end.
        """
        self.warnings.append(PreprocessWarning(node, message))

    def load(self, template):
        if self.loader:
            self.template_dependencies.append(template)
            return self.loader(template)
        else:
            raise Exception('Preprocess context does not support template loading')

    def remember_include(self, template):
        self.include_dependencies.append(template)

    def remember_extends(self, template):
        self.extends_dependencies.append(template)


class PreprocessWarning(Warning):
    def __init__(self, node, message):
        self.node = node
        self.message = message
        super().__init__()


class Options(object):  # pylint: disable=too-many-instance-attributes
    """
    What options are used for compiling the current template.
    """

    def __init__(self):
        # Default settings
        self.merge_all_load_tags = True
        self.preprocess_macros = True
        self.remove_block_tags = True  # Should propably not be disabled
        self.remove_some_tags = True  # As we lack a better settings name

        self.merge_internal_css = False
        self.merge_internal_javascript = False  # Not always recommended...
        # An error will be raised when a block has been defined, which is not present in the parent.
        self.disallow_orphan_blocks = False
        self.disallow_block_level_elements_in_inline_level_elements = False

    def change(self, value, node=None):
        """
        Change an option. Called when the template contains a {% ! ... %} option tag.
        """
        actions = {
            'disallow-orphan-blocks': ('disallow_orphan_blocks', True),
            'merge-internal-css': ('merge_internal_css', True),
            'merge-internal-javascript': ('merge_internal_javascript', True),
            'no-disallow-orphan-blocks': ('disallow_orphan_blocks', False),
            'no-macro-preprocessing': ('preprocess_macros', False),
            'no-block-level-elements-in-inline-level-elements': (
                'disallow_block_level_elements_in_inline_level_elements', True),
        }

        if value in actions:
            setattr(self, actions[value][0], actions[value][1])
        else:
            if node:
                raise CompileException(node, 'No such template preprocessor option: %s' % value)
            else:
                raise CompileException('No such template preprocessor option: %s (in settings.py)' % value)
