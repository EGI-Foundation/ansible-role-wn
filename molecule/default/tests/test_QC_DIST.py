import os
import testinfra.utils.ansible_runner
import pytest
# See http://egi-qc.github.io/#INSTALLATION
# Packages must install without issues in a machine configured without any
# external repositories (valid repositories are the standard OS repo, UMD repo
# and EPEL repo for RH based distros)
# Packages must follow the OS policies (name of packages, use of filesystem
# hierarchy, init scripts, ...). For any detected issue, open a ticket.
# Packages must be signed (or the repository where they are fetched from is
# signed for Debian-based distros)

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
  os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def packages(distro, release):
    listfile_name = "list-" + distro + '-' + release + ".txt"
    listfile = open(listfile_name, "r")
    packages = listfile.read().splitlines()
    return packages


@pytest.mark.parametrize("pkg", packages("redhat", "6"))
def test_packages6(host, pkg):
    if (host.system_info.distribution == 'redhat' and
            host.system_info.distribution.release.startswith(6)):
        assert host.package(pkg).is_installed


@pytest.mark.parametrize("pkg", packages("redhat", "7"))
def test_packages7(host, pkg):
    if (host.system_info.distribution == "redhat" and
            host.system_info.distribution.release.startswith(7)):
        assert host.package(pkg).is_installed
