#  Copyright (c) 2015-2018 Cisco Systems, Inc.
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.

import os

import click

from molecule import config
from molecule import logger
from molecule import util
from molecule.command import base as command_base
from molecule.command.init import base

LOG = logger.get_logger(__name__)


class Collection(base.Base):
    """
    .. program:: molecule init collection --collection-namespace foo --collection-name bar

    .. option:: molecule init collection --collection-namespace foo --collection-name bar

        Initialize a new collection.
    """

    def __init__(self, command_args):
        self._command_args = command_args

    def execute(self):
        """
        Execute the actions necessary to perform a `molecule init collection` and
        returns None.

        :return: None
        """

        collection_namespace = self._command_args['collection_namespace']
        collection_name = self._command_args['collection_name']
        collection_directory = os.getcwd()
        collection_path = collection_namespace + '.' + collection_name
        msg = 'Initializing new collection {}...'.format(collection_path)
        LOG.info(msg)

        if os.path.isdir(collection_path):
            msg = ('The directory {} exists. '
                   'Cannot create new collection.').format(collection_path)
            util.sysexit_with_message(msg)

        self._process_templates('collection', self._command_args, collection_directory)
        msg = 'Initialized colletion in {} successfully.'.format(collection_path)

        # create the default scenario
        scenario_base_directory = os.path.join(collection_directory, collection_name)

        '''
        templates = [
            'collection_scenario/driver/{driver_name}'.format(**self._command_args),
            'collection_scenario/verifier/{verifier_name}'.format(**self._command_args),
        ]

        for template in templates:
            LOG.info(template)
            self._process_templates(template, self._command_args,
                                    scenario_base_directory)

        # create the molecule directory
        self._process_templates('molecule', self._command_args, collection_directory)
        '''

        LOG.success(msg)


@click.command()
@click.pass_context
@click.option(
    '--collection-namespace', '-n', required=True, help='Namespace of the collection.')
@click.option(
    '--collection-name', '-c', required=True, help='Name of the collection.')
def collection(ctx, collection_namespace, collection_name): #pragma: no cover
    """ Initialize a new collection for use with Molecule. """
    command_args = {
        'collection_namespace': collection_namespace,
        'collection_name': collection_name,
    }

    col = Collection(command_args)
    col.execute()
