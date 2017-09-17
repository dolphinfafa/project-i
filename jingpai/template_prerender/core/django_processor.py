#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: skip-file

"""
Django template preprocessor.
Author: jmp0xf, Jonathan Slenders, City Live
"""
from copy import deepcopy

from django.template import TemplateDoesNotExist

from jingpai.template_prerender.core.lexer import Token, State, StartToken, Shift, StopToken, Push, Pop, Error, \
    Record, CompileException
from jingpai.template_prerender.core.lexer_engine import nest_block_level_elements, tokenize

"""
Django parser for a template preprocessor.
------------------------------------------------------------------
Parses django template tags.
"""

__DJANGO_STATES = {
    'root': State(
        # Start of django tag
        State.Transition(r'\{#', (StartToken('django-comment'), Shift(), Push('django-comment'))),
        State.Transition(r'\{%\s*comment\s*%\}',
                         (StartToken('django-multiline-comment'), Shift(), Push('django-multiline-comment'))),
        State.Transition(r'\{%\s*verbatim\s*%\}', (StartToken('django-verbatim'), Shift(), Push('django-verbatim'))),
        State.Transition(r'\{%\s*', (StartToken('django-tag'), Shift(), Push('django-tag'))),
        State.Transition(r'\{{\s*', (StartToken('django-variable'), Shift(), Push('django-variable'))),

        # Content
        State.Transition(r'([^{]|%|{(?![%#{]))+', (StartToken('content'), Record(), Shift(), StopToken())),

        State.Transition(r'.|\s', (Error('Error in parser'),)),
    ),
    # {# .... #}
    'django-comment': State(
        State.Transition(r'#\}', (StopToken(), Shift(), Pop())),
        State.Transition(r'[^\n#]+', (Record(), Shift())),
        State.Transition(r'\n', (Error('No newlines allowed in django single line comment'),)),
        State.Transition(r'#(?!\})', (Record(), Shift())),

        State.Transition(r'.|\s', (Error('Error in parser: comment'),)),
    ),
    'django-multiline-comment': State(
        State.Transition(r'\{%\s*endcomment\s*%\}', (StopToken(), Shift(), Pop())),  # {% endcomment %}
        # Nested single line comments are allowed
        State.Transition(r'\{#', (StartToken('django-comment'), Shift(), Push('django-comment'))),
        State.Transition(r'[^{]+', (Record(), Shift(),)),  # Everything except '{'
        State.Transition(r'\{(?!%\s*endcomment\s*%\}|#)', (Record(), Shift(),)),
        # '{' if not followed by '%endcomment%}'
    ),
    # {% tagname ... %}
    'django-tag': State(
        # State.Transition(r'([a-zA-Z0-9_\-\.|=:\[\]<>(),]+|"[^"]*"|\'[^\']*\')+', # Whole token as one
        State.Transition(r'([^\'"\s%}]+|"[^"]*"|\'[^\']*\')+',  # Whole token as one
                         (StartToken('django-tag-element'), Record(), Shift(), StopToken())),
        State.Transition(r'\s*%\}', (StopToken(), Shift(), Pop())),
        State.Transition(r'\s+', (Shift(),)),  # Skip whitespace

        State.Transition(r'.|\s', (Error('Error in parser: django-tag'),)),
    ),
    # {{ variable }}
    'django-variable': State(
        # State.Transition(r'([a-zA-Z0-9_\-\.|=:\[\]<>(),]+|"[^"]*"|\'[^\']*\')+',
        State.Transition(r'([^\'"\s%}]+|"[^"]*"|\'[^\']*\')+',
                         (StartToken('django-variable-part'), Record(), Shift(), StopToken())),
        State.Transition(r'\s*\}\}', (StopToken(), Shift(), Pop())),
        State.Transition(r'\s+', (Shift(),)),

        State.Transition(r'.|\s', (Error('Error in parser: django-variable'),)),
    ),

    # {% verbatim %} ... {% endverbatim %}
    'django-verbatim': State(
        State.Transition(r'\{%\s*endverbatim\s*%\}', (Shift(), StopToken(), Pop())),  # {% endverbatim %}
        State.Transition(r'[^{]+', (Record(), Shift(),)),  # Everything except '{'
        State.Transition(r'\{(?!%\s*endverbatim\s*%\})', (Record(), Shift(),)),
        # '{' if not followed by '%endverbatim%}'
    ),
}


class DjangoContainer(Token):
    """
    Any node which can contain both other Django nodes and DjangoContent.
    """
    pass


class DjangoContent(Token):
    """
    Any literal string to output. (html, javascript, ...)
    """
    pass


# ====================================[ Parser classes ]=====================================


class DjangoRootNode(DjangoContainer):
    """
    Root node of the parse tree.
    """
    pass


class DjangoComment(Token):
    """
    {# ... #}
    """

    def output(self, handler):
        # Don't output anything. :)
        pass


class DjangoMultilineComment(Token):
    """
    {% comment %} ... {% endcomment %}
    """

    def output(self, handler):
        # Don't output anything.
        pass


class DjangoVerbatim(Token):
    """
    {% verbatim %} ... {% endverbatim %}
    """

    # This tag is transparent, things that look like template tags, variables
    # and other stuff inside this tag is not interpreted in any way, but send to the
    # output straight away.
    #
    # A {% load verbatim %} may be required in order to get the Django
    # template engine support it. See this template tag:
    # https://gist.github.com/629508
    #
    # Verbatim is still an open discussion:
    # http://groups.google.com/group/django-developers/browse_thread/thread/eda0e9187adcbe36/abfb48648c80a9c7?lnk=gst&q=verbatim#abfb48648c80a9c7

    def output(self, handler):
        handler('{% verbatim %}')
        list(map(handler, self.children))
        handler('{% endverbatim %}')


class DjangoTag(Token):
    @property
    def tagname(self):
        """
        return the tagname in: {% tagname option option|filter ... %}
        """
        # This is the first django-tag-element child
        for c in self.children:
            if c.name == 'django-tag-element':
                return c.output_as_string()

    @property
    def args(self):
        iterator = (c for c in self.children if c.name == 'django-tag-element')
        next(iterator)  # Skip first tag-element
        return list(i.output_as_string() for i in iterator)

    def output(self, handler):
        handler('{%')
        for c in self.children:
            handler(c)
            handler(' ')
        handler('%}')


class DjangoVariable(Token):
    def init_extension(self):
        self.__varname = Token.output_as_string(self, True)

    @property
    def varname(self):
        return self.__varname

    def output(self, handler):
        handler('{{')
        handler(self.__varname)
        handler('}}')


class DjangoPreprocessorConfigTag(Token):
    """
    {% ! config-option-1 cofig-option-2 %}
    """

    def process_params(self, params):
        self.preprocessor_options = [p.output_as_string() for p in params[1:]]

    def output(self, handler):
        # Should output nothing.
        pass


class DjangoRawOutput(Token):
    """
    {% !raw %} ... {% !endraw %}
    This section contains code which should not be validated or interpreted
    (Because is would cause trigger a false-positive "invalid HTML" or similar.)
    """

    # Note that this class does not inherit from DjangoContainer, this makes
    # sure that the html processor won't enter this class.
    def process_params(self, params):
        pass

    def output(self, handler):
        # Do not output the '{% !raw %}'-tags
        list(map(handler, self.children))


class DjangoExtendsTag(Token):
    """
    {% extends varname_or_template %}
    """

    def process_params(self, params):
        param = params[1].output_as_string()

        if param[0] == '"' and param[-1] == '"':
            self.template_name = param[1:-1]
            self.template_name_is_variable = False
        elif param[0] == "'" and param[-1] == "'":
            self.template_name = param[1:-1]
            self.template_name_is_variable = False
        else:
            raise CompileException(self, 'Preprocessor does not support variable {% extends %} nodes')

            self.template_name = param
            self.template_name_is_variable = True

    def output(self, handler):
        if self.template_name_is_variable:
            handler('{%extends ')
            handler(self.template_name)
            handler('%}')
        else:
            handler('{%extends "')
            handler(self.template_name)
            handler('"%}')


class DjangoIncludeTag(Token):
    """
    {% include varname_or_template %}

    Support for with-parameters:
    {% include "name_snippet.html" with person="Jane" greeting="Hello" %}
    """

    def process_params(self, params):
        include_param = params[1].output_as_string()

        # Include path
        if include_param[0] in ('"', "'") and include_param[-1] in ('"', "'"):
            self.template_name = include_param[1:-1]
            self.template_name_is_variable = False
        else:
            self.template_name = include_param
            self.template_name_is_variable = True

        # With parameters
        if len(params) > 2 and params[2].output_as_string() == 'with':
            self.with_params = params[3:]
        else:
            self.with_params = []

    def output(self, handler):
        if self.with_params:
            handler('{%with')
            for c in self.with_params:
                handler(' ')
                handler(c)
            handler('%}')

        if self.template_name_is_variable:
            handler('{%include ')
            handler(self.template_name)
            handler('%}')
        else:
            handler('{%include "')
            handler(self.template_name)
            handler('"%}')

        if self.with_params:
            handler('{%endwith%}')


class DjangoDecorateTag(DjangoContainer):
    """
    {% decorate "template.html" %}
        things to place in '{{ content }}' of template.html
    {% enddecorate %}
    """

    def process_params(self, params):
        param = params[1].output_as_string()

        # Template name should not be variable
        if param[0] in ('"', "'") and param[-1] in ('"', "'"):
            self.template_name = param[1:-1]
        else:
            raise CompileException(self, 'Do not use variable template names in {% decorate %}')

    def output(self, handler):
        handler('{%decorate "%s" %}' % self.template_name)
        handler(self.children)
        handler('{%enddecorate%}')


class NoLiteraleException(Exception):
    def __init__(self):
        Exception.__init__(self, 'Not a variable')


def _variable_to_literal(variable):
    """
    if the string 'variable' represents a variable, return it
    without the surrounding quotes, otherwise raise exception.
    """
    if variable[0] in ('"', "'") and variable[-1] in ('"', "'"):
        return variable[1:-1]
    else:
        raise NoLiteraleException()


class DjangoLoadTag(Token):
    """
    {% load module1 module2 ... %}
    """

    def process_params(self, params):
        self.modules = [p.output_as_string() for p in params[1:]]

    def output(self, handler):
        handler('{% load ')
        handler(' '.join(self.modules))
        handler('%}')


class DjangoMacroTag(DjangoContainer):  # TODO: not standard Django -> should be removed
    def process_params(self, params):
        assert len(params) == 2
        name = params[1].output_as_string()
        assert name[0] in ('"', "'") and name[0] == name[-1]
        self.macro_name = name[1:-1]

    def output(self, handler):
        handler('{%macro "')
        handler(self.macro_name)
        handler('"%}')
        Token.output(self, handler)
        handler('{%endmacro%}')


class DjangoCallMacroTag(Token):  # TODO: not standard Django -> should be removed
    def process_params(self, params):
        assert len(params) == 2
        name = params[1].output_as_string()
        assert name[0] in ('"', "'") and name[0] == name[-1]
        self.macro_name = name[1:-1]

    def output(self, handler):
        handler('{%callmacro "')
        handler(self.macro_name)
        handler('"%}')


class DjangoIfTag(DjangoContainer):
    """
    {% if condition %}...{% else %}...{% endif %}
    """

    def process_params(self, params):
        self._params = params

    def output(self, handler):
        handler('{%if ')
        handler(' '.join(p.output_as_string() for p in self._params[1:]))
        handler('%}')

        list(map(handler, self.children))

        # Render {% else %} if this node had an else-block
        # NOTE: nest_block_level_elements will place the second part into
        # children2
        if hasattr(self, 'children2'):
            handler('{%else%}')
            list(map(handler, self.children2))

        handler('{%endif%}')


class DjangoIfEqualTag(DjangoContainer):
    """
    {% ifequal a b %}...{% else %}...{% endifequal %}
    """

    def process_params(self, params):
        self._params = params
        if not len(self._params) == 3:
            raise CompileException(self, '{% ifequal %} needs exactly two parameters')

    def output(self, handler):
        handler('{%ifequal ')
        handler(' '.join(p.output_as_string() for p in self._params[1:]))
        handler('%}')

        list(map(handler, self.children))

        # Render {% else %} if this node had an else-block
        if hasattr(self, 'children2'):
            handler('{%else%}')
            list(map(handler, self.children2))

        handler('{%endifequal%}')


class DjangoBlockTag(DjangoContainer):
    """
    Contains:
    {% block %} children {% endblock %}
    Note: this class should not inherit from DjangoTag, because it's .children are different...  XXX
    """

    def process_params(self, params):
        self.block_name = params[1].output_as_string()

    def output(self, handler):
        handler('{%block ')
        handler(self.block_name)
        handler('%}')
        Token.output(self, handler)
        handler('{%endblock%}')


# ====================================[ Parser extensions ]=====================================


# Mapping for turning the lex tree into a Django parse tree
_PARSER_MAPPING_DICT = {
    'content': DjangoContent,
    'django-tag': DjangoTag,
    'django-variable': DjangoVariable,
    'django-comment': DjangoComment,
    'django-multiline-comment': DjangoMultilineComment,
    'django-verbatim': DjangoVerbatim,
}


def _add_parser_extensions(tree):
    """
    Turn the lex tree into a parse tree.
    Actually, nothing more than replacing the parser classes, as
    a wrapper around the lex tree.
    """
    tree.__class__ = DjangoRootNode

    def _add_parser_extensions2(node):
        if isinstance(node, Token):
            if node.name in _PARSER_MAPPING_DICT:
                node.__class__ = _PARSER_MAPPING_DICT[node.name]
                if hasattr(node, 'init_extension'):
                    node.init_extension()

            list(map(_add_parser_extensions2, node.all_children))

    _add_parser_extensions2(tree)


# Mapping for replacing the *inline* DjangoTag nodes into more specific nodes
_DJANGO_INLINE_ELEMENTS = {
    'extends': DjangoExtendsTag,
    'include': DjangoIncludeTag,
    'load': DjangoLoadTag,
    'callmacro': DjangoCallMacroTag,
    '!': DjangoPreprocessorConfigTag,
}


def _process_inline_tags(tree):
    """
    Replace DjangoTag elements by more specific elements.
    """
    for c in tree.all_children:
        if isinstance(c, DjangoTag) and c.tagname in _DJANGO_INLINE_ELEMENTS:
            # Patch class
            c.__class__ = _DJANGO_INLINE_ELEMENTS[c.tagname]

            # In-line tags don't have childnodes, but process what we had
            # as 'children' as parameters.
            c.process_params(list(c.get_childnodes_with_name('django-tag-element')))
            # TODO: for Jonathan -- we want to keep this tags API compatible with the DjangoTag object, so keep children
            # c.children = []

        elif isinstance(c, DjangoTag):
            _process_inline_tags(c)


# Mapping for replacing the *block* DjangoTag nodes into more specific nodes
__DJANGO_BLOCK_ELEMENTS = {
    'block': ('endblock', DjangoBlockTag),
    'macro': ('endmacro', DjangoMacroTag),
    'decorate': ('enddecorate', DjangoDecorateTag),
    '!raw': ('!endraw', DjangoRawOutput),

    'if': ('else', 'endif', DjangoIfTag),
    'ifequal': ('else', 'endifequal', DjangoIfEqualTag),
}


# ====================================[ Check parser settings in template {% ! ... %} ]================


def _update_preprocess_settings(tree, context):
    """
    Look for parser configuration tags in the template tree.
    Return a dictionary of the render options to use.
    """
    for c in tree.child_nodes_of_class(DjangoPreprocessorConfigTag):
        for o in c.preprocessor_options:
            context.options.change(o, c)


# ====================================[ 'Patched' class definitions ]=====================================


class DjangoPreprocessedInclude(DjangoContainer):
    def init(self, children, with_params=None):
        self.children = children
        self.with_params = with_params

    def output(self, handler):
        if self.with_params:
            handler('{%with')
            for c in self.with_params:
                handler(' ')
                handler(c)
            handler('%}')

        DjangoContainer.output(self, handler)

        if self.with_params:
            handler('{%endwith%}')


class DjangoPreprocessedCallMacro(DjangoContainer):
    def init(self, children):
        self.children = children


class DjangoPreprocessedVariable(DjangoContent):
    def init(self, var_value):
        self.children = var_value


# ====================================[ Parse tree manipulations ]=====================================

def apply_method_on_parse_tree(tree, class_, method, *args, **kwargs):
    for c in tree.all_children:
        if isinstance(c, class_):
            getattr(c, method)(*args, **kwargs)

        if isinstance(c, Token):
            apply_method_on_parse_tree(c, class_, method, *args, **kwargs)


def _find_first_level_dependencies(tree, context):
    for node in tree.child_nodes_of_class((DjangoIncludeTag, DjangoExtendsTag)):
        if isinstance(node, DjangoExtendsTag):
            context.remember_extends(node.template_name)

        elif isinstance(node, DjangoIncludeTag):
            context.remember_include(node.template_name)


def _process_extends(tree, context):
    """
    {% extends ... %}
    When this tree extends another template. Load the base template,
    render it, merge the trees, and return a new tree.
    """
    extends_tag = None

    try:
        base_tree = None

        for c in tree.all_children:
            if isinstance(c, DjangoExtendsTag) and not c.template_name_is_variable:
                extends_tag = c
                base_tree = context.load(c.template_name)
                break

        if base_tree:
            base_tree_blocks = list(base_tree.child_nodes_of_class(DjangoBlockTag))
            tree_blocks = list(tree.child_nodes_of_class(DjangoBlockTag))

            # Retreive list of block tags in the outer scope of the child template.
            # These are the blocks which at least have to exist in the parent.
            outer_tree_blocks = list([b for b in tree.children if isinstance(b, DjangoBlockTag)])

            # For every {% block %} in the base tree
            for base_block in base_tree_blocks:
                # Look for a block with the same name in the current tree
                for block in tree_blocks[:]:
                    if block.block_name == base_block.block_name:
                        # Replace {{ block.super }} variable by the parent's
                        # block node's children.
                        block_dot_super = base_block.children

                        for v in block.child_nodes_of_class(DjangoVariable):
                            if v.varname == 'block.super':
                                # Found a {{ block.super }} declaration, deep copy
                                # parent nodes in here
                                v.__class__ = DjangoPreprocessedVariable
                                v.init(deepcopy(block_dot_super[:]))

                        # Replace all nodes in the base tree block, with this nodes
                        base_block.children = block.children

                        # Remove block from list
                        if block in outer_tree_blocks:
                            outer_tree_blocks.remove(block)

            # We shouldn't have any blocks left (if so, they don't have a match in the parent)
            if outer_tree_blocks:
                warning = 'Found {%% block %s %%} which has not been found in the parent' % outer_tree_blocks[
                    0].block_name
                if context.options.disallow_orphan_blocks:
                    raise CompileException(outer_tree_blocks[0], warning)
                else:
                    context.raise_warning(outer_tree_blocks[0], warning)

            # Move every {% load %} and {% ! ... %} to the base tree
            for l in tree.child_nodes_of_class((DjangoLoadTag, DjangoPreprocessorConfigTag)):
                base_tree.children.insert(0, l)

            return base_tree

        else:
            return tree

    except TemplateDoesNotExist as e:
        # It is required that the base template exists.
        raise CompileException(extends_tag, 'Base template {%% extends "%s" %%} not found' %
                               (extends_tag.template_name if extends_tag else "..."))


def _preprocess_includes(tree, context):
    """
    Look for all the {% include ... %} tags and replace it by their include.
    """
    include_blocks = list(tree.child_nodes_of_class(DjangoIncludeTag))

    for block in include_blocks:
        if not block.template_name_is_variable:
            try:
                # Parse include
                include_tree = context.load(block.template_name)

                # Move tree from included file into {% include %}
                block.__class__ = DjangoPreprocessedInclude
                block.init([include_tree], block.with_params)

                block.path = include_tree.path
                block.line = include_tree.line
                block.column = include_tree.column

            except TemplateDoesNotExist as e:
                raise CompileException(block, 'Template in {%% include %%} tag not found (%s)' % block.template_name)


def _preprocess_decorate_tags(tree, context):
    """
    Replace {% decorate "template.html" %}...{% enddecorate %} by the include,
    and fill in {{ content }}
    """

    class DjangoPreprocessedDecorate(DjangoContent):
        def init(self, children):
            self.children = children

    for decorate_block in list(tree.child_nodes_of_class(DjangoDecorateTag)):
        # Content nodes
        content = decorate_block.children

        # Replace content
        try:
            include_tree = context.load(decorate_block.template_name)

            for content_var in include_tree.child_nodes_of_class(DjangoVariable):
                if content_var.varname == 'decorator.content':
                    content_var.__class__ = DjangoPreprocessedVariable
                    content_var.init(content)

            # Move tree
            decorate_block.__class__ = DjangoPreprocessedDecorate
            decorate_block.init([include_tree])

        except TemplateDoesNotExist as e:
            raise CompileException(decorate_block,
                                   'Template in {% decorate %} tag not found (%s)' % decorate_block.template_name)


def _group_all_loads(tree):
    """
    Look for all {% load %} tags, and group them to one, on top.
    """
    all_modules = set()
    first_load_tag = None
    to_remove = []

    # Collect all {% load %} nodes.
    for load_tag in tree.child_nodes_of_class(DjangoLoadTag):
        # Keeps tags like {% load ssi from future %} as they are.
        # Concatenating these is invalid.
        if not ('from' in load_tag.output_as_string() and 'future' in load_tag.output_as_string()):
            to_remove.append(load_tag)
            # First tag
            if not first_load_tag:
                first_load_tag = load_tag

            for l in load_tag.modules:
                all_modules.add(l)

    # Remove all {% load %} nodes except {% load ... from future %}
    tree.remove_child_nodes(to_remove)

    # Place all {% load %} in the first node of the tree
    if first_load_tag:
        first_load_tag.modules = list(all_modules)
        tree.children.insert(0, first_load_tag)

        # But {% extends %} really needs to be placed before everything else
        # NOTE: (Actually not necessary, because we don't support variable extends.)
        extends_tags = list(tree.child_nodes_of_class(DjangoExtendsTag))
        tree.remove_child_nodes_of_class(DjangoExtendsTag)

        for e in extends_tags:
            tree.children.insert(0, e)


def _preprocess_macros(tree):
    """
    Replace every {% callmacro "name" %} by the content of {% macro "name" %} ... {% endmacro %}
    NOTE: this will not work with recursive macro calls.
    """
    macros = {}
    for m in tree.child_nodes_of_class(DjangoMacroTag):
        macros[m.macro_name] = m

    for call in tree.child_nodes_of_class(DjangoCallMacroTag):
        if call.macro_name in macros:
            # Replace the call node by a deep-copy of the macro childnodes
            call.__class__ = DjangoPreprocessedCallMacro
            call.init(deepcopy(macros[call.macro_name].children[:]))

    # Remove all macro nodes
    tree.remove_child_nodes_of_class(DjangoMacroTag)


def parse(source_code, path, context, main_template=False):
    """
    Parse the code.
    - source_code: string
    - path: for attaching meta information to the tree.
    - context: preprocess context (holding the settings/dependecies/warnings, ...)
    - main_template: False for includes/extended templates. True for the
                     original path that was called.
    """
    # To start, create the root node of a tree.
    tree = Token(name='root', line=1, column=1, path=path)
    tree.children = [source_code]

    # Lex Django tags
    tokenize(tree, __DJANGO_STATES, Token)

    # Phase I: add parser extensions
    _add_parser_extensions(tree)

    # Phase II: process inline tags
    _process_inline_tags(tree)

    # Phase III: create recursive structure for block level tags.
    nest_block_level_elements(tree, __DJANGO_BLOCK_ELEMENTS, DjangoTag, lambda c: c.tagname)

    # === Actions ===

    if main_template:
        _find_first_level_dependencies(tree, context)

    # Extend parent template and process includes
    tree = _process_extends(tree, context)  # NOTE: this returns a new tree!
    _preprocess_includes(tree, context)
    _preprocess_decorate_tags(tree, context)

    # Following actions only need to be applied if this is the 'main' tree.
    # It does not make sense to apply it on every include, and then again
    # on the complete tree.
    if main_template:

        _update_preprocess_settings(tree, context)
        options = context.options

        # Don't output {% block %} tags in the rendered file.
        if options.remove_block_tags:
            tree.collapse_nodes_of_class(DjangoBlockTag)

        # Preprocess {% callmacro %} tags
        if options.preprocess_macros:
            _preprocess_macros(tree)

        # Group all {% load %} statements
        if options.merge_all_load_tags:
            _group_all_loads(tree)

    return tree
