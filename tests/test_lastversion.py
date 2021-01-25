import os

import subprocess
from packaging import version

from lastversion.ProjectHolder import ProjectHolder
from lastversion.lastversion import latest

# change dir to tests directory to make relative paths possible
os.chdir(os.path.dirname(os.path.realpath(__file__)))


def test_tdesktop():
    repo = "https://github.com/telegramdesktop/tdesktop/releases"

    output = latest(repo, 'version', False)

    assert output >= version.parse('1.8.1')


def test_mautic_pre():
    repo = "mautic/mautic"

    output = latest(repo, 'version', True)

    assert output >= version.parse("2.15.2")


def test_monit():
    repo = "https://mmonit.com/monit/dist/monit-5.26.0.tar.gz"

    output = latest(repo, 'version')

    assert output > version.parse("5.25.0")


def test_nginx():
    repo = "https://nginx.org/"

    output = latest(repo, 'version')

    assert output >= version.parse("1.18.0")


def test_gperftools():
    repo = "https://github.com/gperftools/gperftools/releases"

    output = latest(repo)

    assert output >= version.parse("2.7")


def test_symfony():
    repo = "https://github.com/symfony/symfony/releases"

    output = latest(repo)

    assert output >= version.parse("4.2.8")


def test_ngx_pagespeed():
    repo = "apache/incubator-pagespeed-ngx"

    output = latest(repo, output_format='version')

    assert output >= version.parse("1.13.35.2")


def test_wp_cli():
    repo = "wp-cli/wp-cli"

    output = latest(repo)

    assert output >= version.parse("2.2.0")


def test_libvmod_xcounter():
    repo = "https://github.com/xcir/libvmod-xcounter"

    output = latest(repo)

    assert output >= version.parse("62.3")


def test_datadog_agent():
    repo = "DataDog/datadog-agent"

    output = latest(repo)

    # TODO deal with projects like this (dca- and non-dca tags are different subprojects)
    assert output >= version.parse("1.7.0")


def test_grafana():
    repo = "grafana/grafana"

    output = latest(repo)

    assert output >= version.parse("6.2.2")


def test_roer():
    repo = "spinnaker/roer"

    output = latest(repo)

    assert output >= version.parse("0.11.3")


def test_ndk():
    repo = "https://github.com/simplresty/ngx_devel_kit"

    output = latest(repo)

    assert output <= version.parse("0.3.1")


def test_naxsi():
    repo = "https://github.com/nbs-system/naxsi/releases"

    output = latest(repo)

    assert output >= version.parse("1.1")


def test_brotli():
    repo = "https://github.com/eustas/ngx_brotli/releases"

    output = latest(repo)

    assert output == version.parse("0.1.2")


def test_changed_format():
    repo = "https://github.com/nginx-shib/nginx-http-shibboleth/releases"

    output = latest(repo)

    assert output == version.parse("2.0.1")


def test_major():
    repo = "https://github.com/SpiderLabs/ModSecurity"

    output = latest(repo, major='2.9')

    assert output == version.parse("2.9.3")


def test_version_parse_with_dot_x():
    v = '1.19.x'

    h = ProjectHolder()

    assert h.sanitize_version(v) is False


def test_version_parse_dev():
    v = '1.19rc1'

    h = ProjectHolder()

    v = h.sanitize_version(v, pre_ok=True)

    assert v.is_prerelease is True


def test_version_parse_dev2():
    v = '7.18.1-rc.2'

    h = ProjectHolder()

    v = h.sanitize_version(v, pre_ok=True)

    assert v.is_prerelease is True


def test_version_parse_dev3():
    v = '7.18.1'

    h = ProjectHolder()

    v = h.sanitize_version(v, pre_ok=True)

    assert v.is_prerelease is False


def test_contain_rpm_related_data():
    repo = 'dvershinin/lastversion'

    v = latest(repo, output_format='json')

    assert v['spec_tag'] == 'v%{version}'
    assert v['v_prefix'] is True
    assert v['tag_name'].startswith('v')
    assert v['readme']['path'] == 'README.md'
    assert v['license']['path'] == 'LICENSE'


def test_gitlab_1():
    repo = 'https://gitlab.com/ddcci-driver-linux/ddcci-driver-linux/-/tree/master'

    v = latest(repo)

    assert v == version.parse("0.3.3")


def test_merc_1():
    repo = 'https://hg.dillo.org/dillo/'

    v = latest(repo)

    assert v == version.parse('3.0.5')


def test_yml_input():
    repo = os.path.dirname(os.path.abspath(__file__)) + '/geoip2.yml'

    v = latest(repo, output_format='json')

    # should be upstream_version because .yml has "module_of" set
    # rest is repo-specific
    assert v['spec_tag'] == '%{upstream_version}'
    assert v['v_prefix'] is False
    assert not v['tag_name'].startswith('v')
    assert v['readme']['path'] == 'README.md'
    assert v['license']['path'] == 'LICENSE'


def test_magento2_major():
    repo = 'magento/magento2'

    v = latest(repo, major='2.3.4')

    assert v == version.parse('2.3.4.post2')


def test_magento2_major_tag():
    repo = 'magento/magento2'

    v = latest(repo, major='2.3.4', output_format='tag')

    assert v == '2.3.4-p2'


def test_sf_keepass():
    repo = 'https://sourceforge.net/projects/keepass'

    v = latest(repo)

    assert v >= version.parse('2.45')


def test_squid_underscore_lover():
    repo = 'https://github.com/squid-cache/squid/releases'

    v = latest(repo)

    assert v >= version.parse('5.0.1')


def test_patch_release_for_older_is_not_last():
    repo = 'https://github.com/lastversion-test-repos/magento2/releases'

    v = latest(repo)

    assert v == version.parse('2.4.0')


def test_with_search():
    repo = 'telize'

    v = latest(repo)

    assert v >= version.parse('3.0.0')


def test_homepage_github_link_discovery():
    repo = 'https://transmissionbt.com/'

    v = latest(repo)

    assert v >= version.parse('3.0')


def test_homepage_feed_discovery():
    repo = 'https://filezilla-project.org/'

    v = latest(repo, only='FileZilla Client')

    assert v >= version.parse('3.50.0')


def test_main_url():
    repo = 'https://github.com/apache/incubator-pagespeed-ngx'

    process = subprocess.Popen(
        ['lastversion', repo],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    out, err = process.communicate()

    assert version.parse(out.decode('utf-8').strip()) >= version.parse("1.13.35.2")


def test_main_assets():
    repo = 'mautic/mautic'

    process = subprocess.Popen(
        ['lastversion', repo, '--format', 'assets'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    out, err = process.communicate()

    assert "update.zip" in str(out)


def test_pypi_full_url():
    repo = 'https://pypi.org/project/pylockfile/'
    v = latest(repo)

    assert v == version.parse('0.0.3.3')


def test_project_at_pypi():
    repo = 'pylockfile'
    v = latest(repo, at='pip')

    assert v == version.parse('0.0.3.3')


def test_tag_mess():
    repo = 'lastversion-test-repos/rhino'
    v = latest(repo)

    assert v == version.parse('1.7.13')


def test_dict_output():
    """Test dict output."""
    repo = 'SiliconLabs/uC-OS2'
    v = latest(repo, output_format='dict')

    assert v['version'] >= version.parse('2.93.0')
