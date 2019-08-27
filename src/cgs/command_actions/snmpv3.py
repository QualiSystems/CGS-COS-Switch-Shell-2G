import re

from cloudshell.cli.command_template.command_template_executor import CommandTemplateExecutor
from cloudshell.snmp.snmp_parameters import SNMPV3Parameters

from cgs.command_templates import snmpv3


class SnmpV3Actions(object):
    AUTH_COMMAND_MAP = {
        SNMPV3Parameters.AUTH_NO_AUTH: "none",
        SNMPV3Parameters.AUTH_MD5: "MD5",
        SNMPV3Parameters.AUTH_SHA: "SHA"
    }

    PRIV_COMMAND_MAP = {
        SNMPV3Parameters.PRIV_NO_PRIV: "none",
        SNMPV3Parameters.PRIV_DES: "DES",
        SNMPV3Parameters.PRIV_AES128: "AES-128",
        # SNMPV3Parameters.PRIV_3DES: "",  # not supported by device
        # SNMPV3Parameters.PRIV_AES192: "",  # not supported by device
        # SNMPV3Parameters.PRIV_AES256: ""   # not supported by device
    }

    def __init__(self, cli_service, logger):
        """

        :param cli_service:
        :param logger:
        """
        self._cli_service = cli_service
        self._logger = logger

    # todo: rework !!!
    def is_snmp_running(self, action_map=None, error_map=None):
        """

        :return:
        """
        snmp_status = CommandTemplateExecutor(cli_service=self._cli_service,
                                              command_template=snmpv3.SHOW_SNMP_STATUS,
                                              action_map=action_map,
                                              error_map=error_map).execute_command()
        return False
        # return bool(re.search(r"current[\s]+status[\s]+active", snmp_status, flags=re.IGNORECASE | re.MULTILINE))

    def enable_snmp(self, action_map=None, error_map=None):
        """

        :param action_map:
        :param error_map:
        :return:
        """
        return CommandTemplateExecutor(cli_service=self._cli_service,
                                       command_template=snmpv3.ENABLE_SNMP,
                                       action_map=action_map,
                                       error_map=error_map).execute_command()

    def add_snmp_user(self, snmp_user, snmp_password, snmp_priv_key, snmp_auth_proto, snmp_priv_proto,
                      action_map=None, error_map=None):
        """

        :param snmp_user:
        :param snmp_password:
        :param snmp_priv_key:
        :param snmp_auth_proto:
        :param snmp_priv_proto:
        :param action_map:
        :param error_map:
        :return:
        """
        try:
            auth_command_template = self.AUTH_COMMAND_MAP[snmp_auth_proto]
        except KeyError:
            raise Exception("Authentication protocol {} is not supported".format(snmp_auth_proto))

        try:
            priv_command_template = self.PRIV_COMMAND_MAP[snmp_priv_proto]
        except KeyError:
            raise Exception("Privacy Protocol {} is not supported".format(snmp_priv_proto))

        return CommandTemplateExecutor(cli_service=self._cli_service,
                                       command_template=snmpv3.ADD_SNMP_USER,
                                       action_map=action_map,
                                       error_map=error_map).execute_command(snmp_user=snmp_user,
                                                                            snmp_auth_proto=auth_command_template,
                                                                            snmp_password=snmp_password,
                                                                            snmp_priv_proto=priv_command_template,
                                                                            snmp_priv_key=snmp_priv_key)

    def remove_snmp_user(self, snmp_user, action_map=None, error_map=None):
        """

        :param snmp_user:
        :param action_map:
        :param error_map:
        :return:
        """
        return CommandTemplateExecutor(cli_service=self._cli_service,
                                       command_template=snmpv3.REMOVE_SNMP_USER,
                                       action_map=action_map,
                                       error_map=error_map).execute_command(snmp_user=snmp_user)

    def disable_snmp(self, action_map=None, error_map=None):
        """

        :param action_map:
        :param error_map:
        :return:
        """
        return CommandTemplateExecutor(cli_service=self._cli_service,
                                       command_template=snmpv3.DISABLE_SNMP_USER,
                                       action_map=action_map,
                                       error_map=error_map).execute_command()
