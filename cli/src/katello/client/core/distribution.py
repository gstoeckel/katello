#
# Katello Repos actions
# Copyright (c) 2012 Red Hat, Inc.
#
# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.
#
# Red Hat trademarks are not licensed under GPLv2. No permission is
# granted to use or replicate Red Hat trademarks that are incorporated
# in this software or its documentation.
#

import os

from katello.client.api.distribution import DistributionAPI
from katello.client.core.base import BaseAction, Command
from katello.client.api.utils import get_repo
from katello.client.utils import printer
from katello.client.cli.base import opt_parser_add_product, opt_parser_add_org, \
    opt_parser_add_environment, opt_parser_add_environment


# base action ----------------------------------------------------------------

class DistributionAction(BaseAction):

    def __init__(self):
        super(DistributionAction, self).__init__()
        self.api = DistributionAPI()


# actions --------------------------------------------------------------------

class List(DistributionAction):

    description = _('list distributions in a repository')

    def setup_parser(self, parser):
        parser.add_option('--repo_id', dest='repo_id',
                      help=_("repository ID"))
        parser.add_option('--repo', dest='repo',
                      help=_("repository name"))
        opt_parser_add_org(parser)
        opt_parser_add_environment(parser, default=_("Library"))
        opt_parser_add_product(parser)

    def check_options(self, validator):
        if not validator.exists('repo_id'):
            validator.require(('repo', 'org', 'product'))

    def run(self):
        repoId   = self.get_option('repo_id')
        repoName = self.get_option('repo')
        orgName  = self.get_option('org')
        envName  = self.get_option('environment')
        prodName = self.get_option('product')

        self.printer.add_column('id')
        self.printer.add_column('description')
        self.printer.add_column('files', multiline=True, show_with=printer.VerboseStrategy)

        if not repoId:
            repo = get_repo(orgName, prodName, repoName, envName)
            repoId = repo["id"]

        self.printer.set_header(_("Distribution List For Repo %s") % repoId)

        distributions = self.api.distributions_by_repo(repoId)

        self.printer.print_items(distributions)
        return os.EX_OK


# ------------------------------------------------------------------------------

class Info(DistributionAction):

    description = _('list information about a distribution')

    def setup_parser(self, parser):
        # always provide --id option for create, even on registered clients
        parser.add_option('--repo_id', dest='repo_id',
                      help=_("repository ID (required)"))
        parser.add_option('--id', dest='id',
                               help=_("distribution ID eg: ks-rh-noarch (required)"))

    def check_options(self, validator):
        validator.require(('repo_id', 'id'))

    def run(self):
        repoId  = self.get_option('repo_id')
        dist_id = self.get_option('id')

        data = self.api.distribution(repoId, dist_id)

        self.printer.add_column('id')
        self.printer.add_column('description')
        self.printer.add_column('family')
        self.printer.add_column('variant')
        self.printer.add_column('version')
        self.printer.add_column('files', multiline=True, show_with=printer.VerboseStrategy)

        self.printer.set_header(_("Distribution Information"))

        self.printer.print_item(data)
        return os.EX_OK


# command --------------------------------------------------------------------

class Distribution(Command):

    description = _('repo specific actions in the katello server')
