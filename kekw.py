#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:+:                                         _____ _           _   _           :+:
#:+:    KeKW - Website Scanner Recon        |   __| |_ _ _ _ _| |_|_|          :+:
#:+:    By Shyybi                           |__   |   | | | | | . | |          :+:
#:+:                                        |_____|_|_|_  |_  |___|_|          :+:
#:+:                                                  |___|___|                :+:
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

import requests
import time
from colorama import Fore
import os
import sys
paths = [
    'admin', 'login', 'dashboard', 'index.php', 'config.php', 'public_html', 'uploads', '../../public_html', 'backup',
    'wp-admin', 'wp-content', 'wp-includes', 'wp-config.php', 'wp-login.php', 'wp-content/themes', 'wp-content/plugins',
    'wp-content/uploads', 'wp-content/cache', 'wp-content/languages', 'wp-content/upgrade', 'wp-content/backup-db',
    'cgi-bin', 'images', 'css', 'js', 'assets', 'media', 'includes', 'lib', 'modules', 'themes', 'plugins',
    'vendor', 'node_modules', 'composer.json', 'package.json', 'README.md', 'LICENSE', 'robots.txt', 'sitemap.xml',
    'error_log', 'logs', 'tmp', 'temp', 'cache', 'sessions', 'config', 'settings', 'database', 'db', 'sql',
    'backup.sql', 'dump.sql', 'data', 'files', 'docs', 'documentation', 'examples', 'tests', 'test', 'scripts',
    'bin', 'src', 'source', 'app', 'application', 'core', 'system', 'framework', 'public', 'private', 'protected',
    'resources', 'static', 'templates', 'views', 'controllers', 'models', 'migrations', 'seeds', 'factories',
    'storage', 'logs', 'env', '.env', '.htaccess', '.git', '.gitignore', '.svn', '.hg', '.bzr', '.idea', '.vscode',
    'private_key.pem', 'id_rsa', 'id_rsa.pub', 'ssh_config', 'authorized_keys', 'known_hosts', 'passwd', 'shadow',
    'group', 'hosts', 'hostname', 'network', 'resolv.conf', 'httpd.conf', 'nginx.conf', 'php.ini', 'my.cnf',
    'docker-compose.yml', 'Dockerfile', 'Makefile', 'Vagrantfile', 'Procfile', 'Jenkinsfile', 'build.gradle',
    'pom.xml', 'Gemfile', 'requirements.txt', 'Pipfile', 'yarn.lock', 'package-lock.json', 'bower.json', 'gulpfile.js',
    'Gruntfile.js', 'webpack.config.js', 'tsconfig.json', 'babel.config.js', 'eslint.json', 'prettier.config.js',
    'karma.conf.js', 'protractor.conf.js', 'jest.config.js', 'mocha.opts', 'travis.yml', 'circle.yml', 'appveyor.yml',
    'codecov.yml', 'coveralls.yml', 'sonar-project.properties', 'tox.ini', 'pytest.ini', 'setup.py', 'setup.cfg',
    'MANIFEST.in', 'pyproject.toml', 'Cargo.toml', 'Cargo.lock', 'build.rs', 'CMakeLists.txt', 'Makefile.am',
    'Makefile.in', 'configure.ac', 'configure.in', 'autogen.sh', 'bootstrap.sh', 'install.sh', 'uninstall.sh',
    'README', 'CHANGELOG', 'CONTRIBUTING', 'CODE_OF_CONDUCT', 'SECURITY', 'SUPPORT', 'ISSUE_TEMPLATE', 'PULL_REQUEST_TEMPLATE'
]

def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.CYAN + """     __    __            __    __  __       __ 
    /  |  /  |          /  |  /  |/  |  _  /  |
    $$ | /$$/   ______  $$ | /$$/ $$ | / \ $$ |
    $$ |/$$/   /      \ $$ |/$$/  $$ |/$  \$$ |
    $$  $$<   /$$$$$$  |$$  $$<   $$ /$$$  $$ |
    $$$$$  \  $$    $$ |$$$$$  \  $$ $$/$$ $$ |
    $$ |$$  \ $$$$$$$$/ $$ |$$  \ $$$$/  $$$$ |
    $$ | $$  |$$       |$$ | $$  |$$$/    $$$ |
    $$/   $$/  $$$$$$$/ $$/   $$/ $$/      $$/
    """) 
    print(f'{Fore.RED}            https://github.com/shyybi{Fore.RESET}')
    base_url = input(f'{Fore.RESET} URL you wanna scan: ')
    print(f'{Fore.MAGENTA}[i] Base URL: {base_url}{Fore.RESET}')
    return base_url

def detect_cms(url):
    try:
        response = requests.get(url, timeout=5)
        if 'wp-content' in response.text or 'wp-includes' in response.text:
            print(f'{Fore.YELLOW}[i] WordPress CMS detected.{Fore.RESET}')
            return 'WordPress'
        elif 'Joomla!' in response.text:
            print(f'{Fore.YELLOW}[i] Joomla CMS detected.{Fore.RESET}')
            return 'Joomla'
        elif 'Drupal' in response.text:
            print(f'{Fore.YELLOW}[i] Drupal CMS detected.{Fore.RESET}')
            return 'Drupal'
        else:
            print(f'{Fore.YELLOW}[i] CMS not detected.{Fore.RESET}')
            return 'Unknown'
    except requests.exceptions.Timeout:
        print(f'{Fore.YELLOW}[!] Timeout while detecting CMS for {url}{Fore.RESET}')
        return 'Unknown'
    except requests.exceptions.RequestException as e:
        print(f'{Fore.YELLOW}[!] Error while detecting CMS: {e}{Fore.RESET}')
        return 'Unknown'

def detect_waf(url):
    wafs = {
        'cloudflare': 'Cloudflare',
        'sucuri': 'Sucuri',
        'incapsula': 'Incapsula',
        'mod_security': 'ModSecurity',
        'f5': 'F5 BIG-IP',
        'imperva': 'Imperva SecureSphere',
        'barracuda': 'Barracuda',
        'citrix': 'Citrix NetScaler',
        'akamai': 'Akamai',
        'fortinet': 'Fortinet FortiWeb',
        'radware': 'Radware AppWall',
        'sitelock': 'SiteLock TrueShield',
        'stackpath': 'StackPath',
        'aws': 'AWS WAF',
        'azure': 'Azure WAF',
        'bitninja': 'BitNinja',
        'denyall': 'DenyAll',
        'dotdefender': 'dotDefender',
        'edgecast': 'EdgeCast',
        'eisoo': 'Eisoo CloudWAF',
        'ericom': 'Ericom Shield',
        'fortiguard': 'FortiGuard',
        'greywizard': 'Grey Wizard',
        'hyperguard': 'HyperGuard',
        'imunify360': 'Imunify360',
        'nsfocus': 'NSFocus',
        'penta': 'Penta Security',
        'profense': 'Profense',
        'secupress': 'SecuPress',
        'sophos': 'Sophos UTM',
        'squid': 'Squid Proxy',
        'stackpath': 'StackPath',
        'wallarm': 'Wallarm',
        'watchguard': 'WatchGuard',
        'yundun': 'Yundun',
        'yunsuo': 'Yunsuo',
        'zenedge': 'Zenedge'
    }
    
    try:
        response = requests.get(url, timeout=5)
        server_header = response.headers.get('Server', '').lower()
        for key, waf_name in wafs.items():
            if key in server_header:
                print(f'[!] Firewall detected: {waf_name}')
                return waf_name
        print('[i] No firewall detected in the header.')
        return 'None'
    except requests.exceptions.Timeout:
        print(f'[!] Timeout while detecting WAF for {url}')
        return 'Timeout'
    except requests.exceptions.RequestException as e:
        print(f'[!] Error while detecting WAF: {e}')
        return 'Error'

def scan_paths(base_url, paths):
    for path in paths:
        url = base_url + path
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f'{Fore.GREEN}[+] Found: {Fore.RESET}{url}')
            elif response.status_code == 403:
                print(f'{Fore.RED}[-] Access forbidden: {Fore.RESET} {url}')
            else:
                print(f'{Fore.BLUE}[i] {response.status_code}: {Fore.RESET} {url}')
        except requests.exceptions.Timeout:
            print(f'[!] Timeout for {url}')
        except requests.exceptions.RequestException as e:
            print(f'[!] Error while requesting {url}: {e}')

base_url = banner()
cms = detect_cms(base_url)
waf = detect_waf(base_url)
scan_paths(base_url, paths)
