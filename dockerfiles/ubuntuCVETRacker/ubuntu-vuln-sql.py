import os
import glob
import sys
import json

supported_releases = {'xenial': {'desc': '16.04 LTS',
                                 'kernel': '^4\.4\.',
                                 'id': 10
                                 },
                      'trusty': {'desc': '14.04 LTS',
                                 'kernel': '^3\.13\.',
                                 'id': 10
                                 },
                      }

# For now, all EOL, ppa overlays and non-LTS releases
ignored_releases = ['dapper', 'edgy', 'feisty', 'gutsy', 'hardy', 'intrepid',
                    'jaunty', 'karmic', 'maverick', 'natty', 'oneiric',
                    'precise', 'precise/esm', 'quantal', 'lucid', 'raring',
                    'saucy', 'utopic', 'vivid', 'vivid/stable-phone-overlay',
                    'vivid/ubuntu-core', 'wily', 'yakkety', 'zesty', 'artful']

all_releases = list(supported_releases.keys()) + ignored_releases

ignored_package_fields = ['Patches', 'devel', 'upstream', 'Assigned-to',
                          'product']
ignore_indented_package_lines = True

default_cves_to_process = ['/opt/bzr-pulls/ubuntu-cve-tracker/active/CVE-*', '/opt/bzr-pulls/ubuntu-cve-tracker/retired/CVE-*']

CVEs={}
packages={}


def main():
    files = []
    pathnames = default_cves_to_process
    for pathname in pathnames:
        files = files + glob.glob(pathname)
    files.sort()

    files_count = len(files)
    for i_file, filepath in enumerate(files):
        cve_data = parse_cve_file(filepath)
	if cve_data['header']['Candidate'] not in CVEs:
		#print cve_data
		CVEs[cve_data['header']['Candidate']] = cve_data
	for package_name, package in cve_data['packages'].iteritems():
		if package_name not in packages:
			packages[package_name] = {}
		for release_name, release in package['Releases'].iteritems():
			if release_name not in packages[package_name]:
				packages[package_name][release_name] = {"fixed":{}, "unknown":[],"vulnerable":[], "not-vulnerable":[]}
			if release['status'] == "fixed":
				int_version = convert_version_to_int(release['fix-version'])
				if release['fix-version'] not in packages[package_name][release_name]['fixed']:
					packages[package_name][release_name]['fixed']["%s-%s" % (release['fix-version'], int_version)] = [cve_data['header']['Candidate']]
				else:
					packages[package_name][release_name]['fixed']["%s-%s" % (release['fix-version'], int_version)].append(cve_data['header']['Candidate'])
                        if release['status'] == "vulnerable":
                                packages[package_name][release_name]['vulnerable'].append(cve_data['header']['Candidate'])
			if release['status'] == "unkown":
				packages[package_name][release_name]['unkown'].append(cve_data['header']['Candidate'])
			if release['status'] == "not-vulnerable":
				packages[package_name][release_name]['not-vulnerable'].append(cve_data['header']['Candidate'])


    write_output_json(packages, '/mnt/data/ubuntu-packages.json')
    write_output_json(CVEs, '/mnt/data/ubuntu-cves.json')


def write_output_json(json_obj, file):
    with open(file, 'w') as fh:
        fh.write(json.dumps(json_obj))
    print "File written to %s" % file

def convert_version_to_int(version):
	int_version=0
	for char in version:
		int_version = int_version +ord(char)
	return int_version

#def add(CVEs):
#	for cve in CVEs:

def parse_package_status(release, package, status_text, filepath):
    """ parse ubuntu package status string format:
          <status code> (<version/notes>)
        outputs dictionary: {
          'status'        : '<not-applicable | unknown | vulnerable | fixed>',
          'note'          : '<description of the status>',
          'fix-version'   : '<version with issue fixed, if applicable>'
        } """

    # break out status code and detail
    status_sections = status_text.strip().split(' ', 1)
    code = status_sections[0].strip().lower()
    detail = status_sections[1].strip('()') if len(status_sections) > 1 else ''

    if code == 'released' and not detail:
        warn('Missing fix version note in {0}_{1} in "{2}". Changing to "unknown".'.format(release, package, filepath))
        code = 'unknown-fix-version'

    status = {}
    note_end = " (note: '{0}').".format(detail) if detail else '.'
    if code == 'dne':
        status['status'] = 'not-applicable'
        status['note'] = \
            "The '{0}' package does not exist in {1}{2}".format(package,
                                                                release,
                                                                note_end)
    elif code == 'ignored':
        status['status'] = 'vulnerable'
        status['note'] = "While related to the CVE in some way, a decision has been made to ignore it{2}".format(package, release, note_end)
    elif code == 'not-affected':
        status['status'] = 'not-vulnerable'
        status['note'] = "While related to the CVE in some way, the '{0}' package in {1} is not affected{2}".format(package, release, note_end)
    elif code == 'needed':
        status['status'] = 'vulnerable'
        status['note'] = \
            "The '{0}' package in {1} is affected and needs fixing{2}".format(
                package, release, note_end)
    elif code == 'active':
        status['status'] = 'vulnerable'
        status['note'] = "The '{0}' package in {1} is affected, needs fixing and is actively being worked on{2}".format(package, release, note_end)
    elif code == 'pending':
        status['status'] = 'vulnerable'
        status['note'] = "The '{0}' package in {1} is affected. An update containing the fix has been completed and is pending publication{2}".format(package, release, note_end)
    elif code == 'deferred':
        status['status'] = 'vulnerable'
        status['note'] = "The '{0}' package in {1} is affected, but a decision has been made to defer addressing it{2}".format(package, release, note_end)
    elif code == 'released':
        status['status'] = 'fixed'
        status['note'] = "The '{0}' package in {1} was vulnerable but has been fixed{2}".format(package, release, note_end)
        status['fix-version'] = detail
    else:
        if code != 'needs-triage' and code != 'unknown-fix-version':
            warn('Unsupported status "{0}" in {1}_{2} in "{3}". Setting to "unknown".'.format(code, release, package, filepath))
        status['status'] = 'unknown'
        status['note'] = "The vulnerability of the '{0}' package in {1} is not known (status: '{2}'). It is pending evaluation{3}".format(package, release, code, note_end)

    return status


def parse_cve_file(filepath):
    """ parse CVE data file into a dictionary """

    cve_header_data = {
        'Candidate': '',
        'CRD': '',
        'PublicDate': '',
        'PublicDateAtUSN': '',
        'References': [get_cve_url(filepath)],
        'Description': '',
        'Ubuntu-Description': '',
        'Notes': '',
        'Bugs': [],
        'Priority': '',
        'Discovered-by': '',
        'Assigned-to': '',
        'Unknown-Fields': [],
        'Source-note': filepath
    }

    f = open(filepath, 'r')
    key = ''
    values = []
    in_header = True
    packages = {}
    current_package = ''
    packages_section_keys = all_releases + ['Patches', 'Tags', 'upstream']

    for line in f:
        if line.strip().startswith('#') or line.strip().startswith('--'):
            continue

        if in_header and line.split('_', 1)[0] in packages_section_keys:
            in_header = False

        # Note: some older cves include Priority_package in header section
        if in_header and not line.startswith('Priority_'):
            if line.startswith(' '):
                values.append(line.strip())
            else:
                if key and key in cve_header_data and \
                        type(cve_header_data[key]) is str:
                    if cve_header_data[key]:
                        cve_header_data[key] = cve_header_data[key] + ' ' + \
                            ' '.join(values)
                    else:
                        cve_header_data[key] = ' '.join(values)
                elif key and key in cve_header_data and \
                        type(cve_header_data[key]) is list:
                    cve_header_data[key] = cve_header_data[key] + values
                elif key:
                    warn('Unknown header field "{0}" found in {1} '.format(key,
                         filepath))
                    cve_header_data['Unknown-Fields'].append(
                        {key: ' '.join(values)})

                if line.strip() == '':
                    continue

                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                values = [value] if value else []

        else:
            # we're in the packages section
            if ignore_indented_package_lines and line.startswith(' '):
                continue

            line = line.strip()
            if not line:
                current_package = ''
                continue

            keys, value = line.split(':', 1)
            value = value.strip()
            keys = keys.split('_', 1)
            key = keys[0]
            if len(keys) == 2:
                package = keys[1]
                current_package = package
            else:
                package = current_package

            if (package not in packages):
                packages[package] = {
                    'Priority': '',
                    'Tags': [],
                    'Releases': {}
                }

            if key in ignored_package_fields or key in ignored_releases:
                continue

            if key in supported_releases:
                if key in packages[package]['Releases']:
                    warn('Duplicate package field key "{0}" found in "{1}" package in {2}'.format(key, package, filepath))
                packages[package]['Releases'][key] = \
                    parse_package_status(key, package, value, filepath)
            elif key == 'Priority':
                if packages[package][key]:
                    warn('Duplicate package field key "{0}" found in "{1}" package in {2}'.format(key, package, filepath))
                packages[package][key] = value
            elif key == 'Tags':
                packages[package][key].append(value)
            else:
                warn('Unknown package field "{0}" in {0}_{1} in "{2}"'.format(key, package, filepath))

    f.close()

    # remove packages with no supported releases
    packages = {name: package for name, package in packages.items()
                if package['Releases']}

    return {'header': cve_header_data, 'packages': packages}


def warn(message):
    """ print a warning message """
    sys.stdout.write('\rWARNING: {0}\n'.format(message))

def get_cve_url(filepath):
    """ returns a url to CVE data from a filepath """
    path = os.path.realpath(filepath).split(os.sep)
    url = "http://people.canonical.com/~ubuntu-security/cve"
    cve = path[-1]
    year = cve.split('-')[1]
    return "%s/%s/%s.html" % (url, year, cve)

if __name__ == '__main__':
    main()
