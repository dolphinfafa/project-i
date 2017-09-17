"""
Author: jmp0xf, Jonathan Slenders, City Live
"""
import codecs
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.template import TemplateDoesNotExist

from jingpai.template_prerender.core import render
from jingpai.template_prerender.core.lexer import CompileException
from jingpai.template_prerender.utils import get_options_for_path
from jingpai.template_prerender.utils import template_iterator, load_template_source, get_template_path


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        self.verbosity = 1
        self._errors = []
        BaseCommand.__init__(self, *args, **kwargs)

    def print_error(self, text):
        self._errors.append(text)
        print(text)

    def handle(self, *args, **options):
        # Default verbosity
        self.verbosity = int(options.get('verbosity', 1))

        # Build render queue
        queue = self._build_render_queue()

        # Compile queue
        for i in range(0, len(queue)):
            self._render_template(*queue[i])

        # # Show all errors once again.
        print(u'\n*** %i template files processed, %i render errors ***' % (len(queue), len(self._errors)))

        # Ring bell :)
        print('\x07')

    def _build_render_queue(self):
        """
        Build a list of all the templates to be rendered.
        """
        # Create render queue
        queue = set()  # Use a set, avoid duplication of records.

        if self.verbosity >= 2:
            print('Building queue')

        # Now render all templates to the cache directory
        for dir_path, t in template_iterator():
            input_path = os.path.normpath(os.path.join(dir_path, t))
            output_path = self._make_output_path(t)

            queue.add((t, input_path, output_path))

            # When this file has to be rendered, and other files depend
            # on this template also render the other templates.
            if os.path.exists(output_path + '-c-used-by'):
                for t2 in open(output_path + '-c-used-by', 'r').read().split('\n'):
                    if t2:
                        try:
                            queue.add((t2, get_template_path(t2), self._make_output_path(t2)))
                        except TemplateDoesNotExist:
                            pass  # Reference to non-existing template

        # Return ordered queue
        queue = list(queue)
        queue.sort()
        return queue

    @staticmethod
    def _make_output_path(template):
        return os.path.normpath(os.path.join(settings.TEMPLATE_CACHE_DIR, template))

    def _save_template_dependencies(self, template, dependency_list):
        """
        Store template dependencies into meta files.  (So that we know which
        templates need to be rerendered when one of the others has been
        changed.)
        """
        # Reverse dependencies
        for t in dependency_list:
            output_path = self._make_output_path(t) + '-c-used-by'
            self._create_dir(os.path.split(output_path)[0])

            # Append current template to this list if it doesn't appear yet
            deps = open(output_path, 'r').read().split('\n') if os.path.exists(output_path) else []

            if template not in deps:
                open(output_path, 'a').write(template + '\n')

        # Dependencies
        output_path = self._make_output_path(template) + '-c-depends-on'
        open(output_path, 'w').write('\n'.join(dependency_list) + '\n')

    def _save_first_level_template_dependencies(self, template, include_list, extends_list):
        """
        First level dependencies (used for generating dependecy graphs)
        (This doesn't contain the indirect dependencies.)
        """
        # {% include "..." %}
        output_path = self._make_output_path(template) + '-c-includes'
        open(output_path, 'w').write('\n'.join(include_list) + '\n')

        # {% extends "..." %}
        output_path = self._make_output_path(template) + '-c-extends'
        open(output_path, 'w').write('\n'.join(extends_list) + '\n')

    def _render_template(self, template, input_path, output_path):
        try:
            # Create output directory
            self._create_dir(os.path.split(output_path)[0])

            try:
                # Open input file
                code = codecs.open(input_path, 'r', 'utf-8').read()
            except UnicodeDecodeError as e:
                raise CompileException(0, 0, input_path, str(e))
            except IOError as e:
                raise CompileException(0, 0, input_path, str(e))

            # Compile
            output, context = render(
                code, path=input_path, loader=load_template_source,
                options=get_options_for_path(input_path),
            )

            # store dependencies
            self._save_template_dependencies(template, context.template_dependencies)
            self._save_first_level_template_dependencies(template, context.include_dependencies,
                                                         context.extends_dependencies)

            # Open output file
            codecs.open(output_path, 'w', 'utf-8').write(output)

            # Delete -c-rerender file (mark for rerender) if one such exist.
            if os.path.exists(output_path + '-c-rerender'):
                os.remove(output_path + '-c-rerender')

            return True

        except CompileException as e:
            # Print the error
            self.print_error(u'ERROR:  %s' % str(e))

            print('Failed')

            # Create rerender mark
            open(output_path + '-c-rerender', 'w').close()

        except TemplateDoesNotExist as e:
            if self.verbosity >= 2:
                print(u'WARNING: Template does not exist:  %s' % str(e))

    @staticmethod
    def _create_dir(newdir):
        if not os.path.isdir(newdir):
            os.makedirs(newdir)
