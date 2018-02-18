#!Python3
#Justin Mason 18 FEB 2018
import re
import os
import time
import subprocess

#Functions
def backup():
    def backup_directories():
        if not os.path.exists('/root/backup/'):
            print('Creating /root/backup/ directory')
            os.mkdir('/root/backup')
        if not os.path.exists('/root/backup/fir/'):
            print('Creating /root/backup/fir/ directory')
            os.mkdir('/root/backup/fir')
        if not os.path.exists('/root/backup/mediawiki/'):
            print('Creating /root/backup/mediawiki/ directory')
            os.mkdir('/root/backup/mediawiki')
        if not os.path.exists('/root/backup/rocket/'):
            print('Creating /root/backup/rocket/ directory')
            os.mkdir('/root/backup/rocket')
        if not os.path.exists('/root/backup/rt/'):
            print('Creating /root/backup/rt/ directory')
            os.mkdir('/root/backup/rt')
    def fir():
        print('\nBacking up FIR')
        os.system('systemctl stop fir_uwsgi')
        print('MySQL Authentication')
        os.system('mysqldump -u root -p fir > /root/backup/fir/fir.sql.%s' % date)
        os.system('systemctl start fir_uwsgi')
        print('FIR Backup Complete. Note that attachments are located in /opt/FIR/uploads/')
    def mediawiki():
        print('\nBacking up Mediawiki')
        print('MySQL Authentication')
        os.system('mysqldump -u root -p mediawiki > /root/backup/mediawiki/mediawiki.sql.%s' % date)
        print('Mediawiki Backup Complete. Note that uploaded files are located in /var/www/mediawiki/images/')
    def rocket():
        print('Backing up Rocket Chat')
        os.system('systemctl stop rocketchat')
        os.system('mongodump --out /root/backup/rocket/rocketchat.dump.%s -db rocketchat' % date)
        os.system('systemctl start rocketchat')
        print('Rocket Backup Complete.')
    def rt():
        print('\nBacking up Request Tracker')
        print('MySQL Authentication')
        os.system('mysqldump -u root -p rt4 > /root/backup/rt/rt4.sql.%s' % date)
        print('RT Backup Complete.')
    def remote_backup():
        #/root/backup is hard coded as the source of the backups
        print('This will backup to ~/backup on the target.')
        print('Target IP?')
        target = str(input())
        print('User?')
        user = str(input())
        if not os.path.exists('/root/.ssh/id_rsa.pub'):
            print('\nGenerating key, accept all defaults with no passphrase\n')
            os.system('ssh-keygen')
        print('\nPlease wait and enter ssh password if prompted.')
        os.system('ssh-copy-id %s@%s' % (user, target))
        print('\nCreating directories if they do not exist:')
        os.system('ssh %s@%s \'mkdir ~/backup ~/backup/fir ~/backup/fir/uploads ~/backup/mediawiki ~/backup/mediawiki/images ~/backup/rocket ~/backup/rt\'' % (user, target))
        print('\nCopying FIR:')
        os.system('scp /root/backup/fir/fir.sql.%s %s@%s:~/backup/fir/' % (date, user, target))
        os.system('scp -r /opt/FIR/uploads/* %s@%s:~/backup/fir/uploads' % (user, target))
        print('\nCopying Mediawiki:')
        os.system('scp /root/backup/mediawiki/mediawiki.sql.%s %s@%s:~/backup/mediawiki/' % (date, user, target))
        os.system('scp -r /var/www/mediawiki/images/* %s@%s:~/backup/mediawiki/images/' % (user, target))
        print('\nCopying Rocket:')
        os.system('scp -r /root/backup/rocket/rocketchat.dump.%s %s@%s:~/backup/rocket/' % (date, user, target))
        print('\nCopying Request Tracker:')  
        os.system('scp /root/backup/rt/rt4.sql.%s %s@%s:~/backup/rt/' % (date, user, target))
    #Backup Main
    date = time.strftime('%Y-%m-%d')
    print('')
    backup_directories()
    print('\nOptions')
    print('1: Local Backup')
    print('2: Remote Backup')
    print('3: Local and Remote Backup')
    print('4: Exit') 
    print('\nChoice:', end='')
    backupSelection = int(input())                  
    if(backupSelection == 1):
        print('\nYou will need to enter the mysql database password 3 seperate times.\n')
        input('Press enter to continue:')
        os.system('apachectl stop')
        fir()
        mediawiki()
        rt()
        rocket()
        os.system('apachectl start')
        print('All Backups Complete.')  
    if(backupSelection == 2):
        print('\nThis will only copy database backups created today.\n')
        input('Press enter to continue:')
        remote_backup()
        print('SCP Complete')
    if(backupSelection == 3):
        print('\nYou will need to enter the mysql database password 3 seperate times.\n')
        input('Press enter to continue:')
        fir()
        mediawiki()
        rt()
        rocket()
        print('\n')
        remote_backup()
        print('Local and Remote Backup Complete.')
    if(backupSelection == 4):
        None
                  
def configure():
    shell = subprocess.Popen(["ip", "a"],shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout, stderr = shell.communicate()
    stdout = stdout.decode('utf-8')
    stderr = stderr.decode('utf-8')
    regex = re.compile('ens192:')
    if (regex.search(stdout)):
        print('\nThe default interface to configure is ens192.\nInput a different interface or press enter to continue: ', end='')
        interface = input() or "ens192"
    else:
        print('\n' + stdout)
        print('\nPlease choose an interface: ')
        interface = input()
    if os.path.exists('/etc/sysconfig/network-scripts/ifcfg-' + interface):
        file = open('/etc/sysconfig/network-scripts/ifcfg-' + interface)
        fileContent = file.read()
        file.close()
        regex = re.compile(r'IPADDR=[\'\"]?\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3}', re.IGNORECASE)
        regex2 = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3}')
        try:
            oldadd = str(regex2.search((regex.search(fileContent)).group()).group())
            print('\nThe current IP address is: ' + oldadd)
        except:
            pass
    print('\nEnter the IP address (required): ', end='')
    ipadd = str(input())
    print('Enter the network mask or press enter for 255.255.255.0: ', end='')
    netmask = str(input()) or '255.255.255.0'
    print('Gateway IP: ', end='')
    gateway = str(input())
    print('\nThe DNS will be set to localhost. Your clients can use either this machine to resolve DNS or another server such as pfSense (preferred for ease of administration).')
    dns = '127.0.0.1'
    print('\nEnter NTP source IP: ', end='')
    ntpadd = str(input())

    file = open('/etc/sysconfig/network-scripts/ifcfg-' + interface, 'w')
    file.write('TYPE="Ethernet"\n')
    file.write('BOOTPROTO="none"\n')
    file.write('DEFROUTE="yes"\n')
    file.write('PEERDNS="yes"\n')
    file.write('PEERROUTES="yes"\n')
    file.write('IPV4_FAILURE_FATAL="no"\n')
    file.write('NAME="%s"\n' % interface)
    file.write('DEVICE="%s"\n'% interface)
    file.write('ONBOOT="yes"\n')
    file.write('IPADDR="%s"\n' % ipadd)
    file.write('NETMASK="%s"\n' % netmask)
    file.write('GATEWAY="%s"\n' % gateway)
    file.write('DNS1="%s"\n' % dns)
    file.close()

    file = open('/var/named/soc.lan.zone', 'w')
    file.write('$TTL 86400\n')
    file.write('@\tIN\tSOA\tsoc.lan.\tadmin.soc.lan. (\n')
    file.write('\t1\t; Serial\n')
    file.write('\t21600\t; refresh after 6 hours\n')
    file.write('\t3600\t; retry after  hour\n')
    file.write('\t604800\t; expire after 1 week\n')
    file.write('\t86400\t; minimum TTL of 1 day\n')
    file.write(')\n')
    file.write('\tIN\tNS\tportal.soc.lan.\n')
    file.write('; Replace IP addresses with current IP address of this machine\n')
    file.write('fir\tIN\tA\t%s\n' % ipadd)
    file.write('mediawiki\tIN\tA\t%s\n' % ipadd)
    file.write('portal\tIN\tA\t%s\n' % ipadd)
    file.write('rocket\tIN\tA\t%s\n' % ipadd)
    file.write('rt\tIN\tA\t%s\n' % ipadd)
    file.close()

    file = open('/etc/chrony.conf', 'w')
    file.write('server %s iburst\n' % ntpadd)
    file.write('stratumweight 0\n')
    file.write('driftfile /var/lib/chrony/drift\n')
    file.write('rtcsync\n')
    file.write('makestep 10 3\n')
    file.write('bindcmdaddress 127.0.0.1\n')
    file.write('bindcmdaddress ::1\n')
    file.write('keyfile /etc/chrony.keys\n')
    file.write('commandkey 1\n')
    file.write('generatecommandkey\n')
    file.write('noclientlog\n')
    file.write('logchange 0.5\n')
    file.write('logdir /var/log/chrony\n')
    file.close()
    
    #Reboot rather than worrying about restarting services / flushing dns.
    print('\nSetup complete; press enter to reboot or type no.')
    if input(): 
        None
    else:
        os.system('reboot')
def restore():
    def fir():
        print('\nRestoring FIR\n')
        shell = subprocess.Popen(["ls", "/root/backup/fir/"],shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        stdout, stderr = shell.communicate()
        stdout = stdout.decode('utf-8')
        stderr = stderr.decode('utf-8')
        firBackup = stdout.split()
        count = 0
        for word in firBackup:
            print(str(count) + ': ' + word)
            count += 1
        print('\nWhich backup would you like to use?')
        selection = int(input())
        os.system('systemctl stop fir_uwsgi')
        print('\nMySQL Authentication')
        os.system('mysql -u root -p fir < /root/backup/fir/%s' % firBackup[selection])
        os.system('cp -r /root/backup/fir/uploads/* /opt/FIR/uploads/')
        os.system('chown -R apache:apache /opt/FIR/uploads/*')
        os.system('systemctl start fir_uwsgi')
        print('FIR Restoration Complete.')
    def mediawiki():
        print('\nRestoring Mediawiki\n')
        shell = subprocess.Popen(["ls", "/root/backup/mediawiki/"],shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        stdout, stderr = shell.communicate()
        stdout = stdout.decode('utf-8')
        stderr = stderr.decode('utf-8')
        mediawikiBackup = stdout.split()
        count = 0
        for word in mediawikiBackup:
            print(str(count) + ': ' + word)
            count += 1
        print('\nWhich backup would you like to use?')
        selection = int(input())
        print('\nMySQL Authentication')
        os.system('mysql -u root -p mediawiki < /root/backup/mediawiki/%s' % mediawikiBackup[selection])
        os.system('cp -r /root/backup/mediawiki/images/* /var/www/mediawiki/images/')
        os.system('chown -R apache:apache /var/www/mediawiki/images/*')
        print('Mediawiki Restoration Complete.')
    def rocket():
        print('\nRestoring Rocket\nThis will purge the existing databse.\n')
        shell = subprocess.Popen(["ls", "/root/backup/rocket/"],shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        stdout, stderr = shell.communicate()
        stdout = stdout.decode('utf-8')
        stderr = stderr.decode('utf-8')
        rocketBackup = stdout.split()
        count = 0
        for word in rocketBackup:
            print(str(count) + ': ' + word)
            count += 1
        print('\nWhich backup would you like to use?')
        selection = int(input())
        os.system('systemctl stop rocketchat')
        os.system('mongo rocketchat --eval "db.dropDatabase()"')
        os.system('mongorestore -d rocketchat /root/backup/rocket/%s/rocketchat' % rocketBackup[selection])
        os.system('systemctl start rocketchat')
        print('Rocket Restoration Complete.')
    def rt():
        print('\nRestoring Request Tracker\n')
        shell = subprocess.Popen(["ls", "/root/backup/rt/"],shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        stdout, stderr = shell.communicate()
        stdout = stdout.decode('utf-8')
        stderr = stderr.decode('utf-8')
        rtBackup = stdout.split()
        count = 0
        for word in rtBackup:
            print(str(count) + ': ' + word)
            count += 1
        print('\nWhich backup would you like to use?')
        selection = int(input())
        print('\nMySQL Authentication')
        os.system('mysql -u root -p rt4 < /root/backup/rt/%s' % rtBackup[selection])
        print('Request Tracker Restoration Complete.')

    #Main Restore
    print('')
    print('\nOptions')
    print('1: Restore FIR')
    print('2: Restore Mediawiki')
    print('3: Restore Rocket')
    print('4: Restore RT')
    print('5: Restore All')
    print('6: Exit')
    print('\nChoice:', end='')
    restoreSelection = int(input())                  
    if(restoreSelection == 1):
        os.system('apachectl stop')
        fir()
        os.system('apachectl start')
    if(restoreSelection == 2):
        os.system('apachectl stop')
        mediawiki()
        os.system('apachectl start')
    if(restoreSelection == 3):
        os.system('apachectl stop')
        rocket()
        os.system('apachectl start')
    if(restoreSelection == 4):
        os.system('apachectl stop')
        rt()
        os.system('apachectl start')
    if(restoreSelection == 5):
        print('\nYou will need to enter the mysql database password 3 seperate times.\n')
        input('Press enter to continue:')
        os.system('apachectl stop')
        fir()
        mediawiki()
        rocket()
        rt()
        os.system('apachectl start')
    if(restoreSelection == 6):
        None
def status():
    print('\nServices status:')
    #Apache
    shell = subprocess.Popen(["apachectl", "status"],shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout, stderr = shell.communicate()
    stdout = stdout.decode('utf-8')
    stderr = stderr.decode('utf-8')
    regex = re.compile('Active:.*\n')
    apache = regex.search(stdout).group()
    apache = apache.replace('Active:', 'Apache:')
    print(apache, end='')
    #Chrony
    shell = subprocess.Popen(["systemctl", "status", "chronyd"],shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout, stderr = shell.communicate()
    stdout = stdout.decode('utf-8')
    stderr = stderr.decode('utf-8')
    regex = re.compile('Active:.*\n')
    chrony = regex.search(stdout).group()
    chrony = chrony.replace('Active:', 'NTP:   ')
    print(chrony, end='')
    #Named
    shell = subprocess.Popen(["systemctl", "status", "named"],shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout, stderr = shell.communicate()
    stdout = stdout.decode('utf-8')
    stderr = stderr.decode('utf-8')
    regex = re.compile('Active:.*\n')
    named = regex.search(stdout).group()
    named = named.replace('Active:', 'DNS:   ')
    print(named, end='')
    #Fir
    shell = subprocess.Popen(["systemctl", "status", "fir_uwsgi"],shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout, stderr = shell.communicate()
    stdout = stdout.decode('utf-8')
    stderr = stderr.decode('utf-8')
    regex = re.compile('Active:.*\n')
    fir = regex.search(stdout).group()
    fir = fir.replace('Active:', 'FIR:   ')
    print(fir, end='')
    #Rocket
    shell = subprocess.Popen(["systemctl", "status", "rocketchat"],shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout, stderr = shell.communicate()
    stdout = stdout.decode('utf-8')
    stderr = stderr.decode('utf-8')
    regex = re.compile('Active:.*\n')
    rocket = regex.search(stdout).group()
    rocket = rocket.replace('Active:', 'Rocket:')
    print(rocket, end='')
    #SSHD
    shell = subprocess.Popen(["systemctl", "status", "sshd"],shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout, stderr = shell.communicate()
    stdout = stdout.decode('utf-8')
    stderr = stderr.decode('utf-8')
    regex = re.compile('Active:.*\n')
    sshd = regex.search(stdout).group()
    sshd = sshd.replace('Active:', 'SSHD:  ')
    print(sshd, end='')
    
    #Firewalld Check
    print('\nPorts Allowed:')
    #SSH
    print('22:  ', end='')
    shell = subprocess.Popen(["firewall-cmd", "--query-service=ssh"],shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout, stderr = shell.communicate()
    stdout = stdout.decode('utf-8')
    stderr = stderr.decode('utf-8')
    sshPort = stdout
    print(sshPort, end='')
    #DNS
    print('53:  ', end='')
    shell = subprocess.Popen(["firewall-cmd", "--query-service=dns"],shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout, stderr = shell.communicate()
    stdout = stdout.decode('utf-8')
    stderr = stderr.decode('utf-8')
    dnsPort = stdout
    print(dnsPort, end='')
    #HTTP
    print('80:  ', end='')
    shell = subprocess.Popen(["firewall-cmd", "--query-service=http"],shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout, stderr = shell.communicate()
    stdout = stdout.decode('utf-8')
    stderr = stderr.decode('utf-8')
    httpPort = stdout
    print(httpPort, end='')
    #HTTPS
    print('443: ', end='')
    shell = subprocess.Popen(["firewall-cmd", "--query-service=https"],shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout, stderr = shell.communicate()
    stdout = stdout.decode('utf-8')
    stderr = stderr.decode('utf-8')
    httpsPort = stdout
    print(httpsPort, end='')

    print('\nThis script will now attempt recovery if needed.\nShould that fail, please run the configuration again.')
    #Recovery
    regex = re.compile(r'\bactive\b')
    
    if not(regex.search(apache)):
        print('\nApache has failed, press enter to attempt restart.', end='')
        input()
        os.system('apachectl restart')
        os.system('systemctl enable httpd')
        print('Restart Attempted')
    if not(regex.search(chrony)):
        print('\nNTP client has failed, press enter to attempt restart.', end='')
        input()
        os.system('systemctl chronyd restart')
        os.system('systemctl enable chronyd')
        print('Restart Attempted')
    if not(regex.search(named)):
        print('\nDNS has failed, press enter to attempt restart.', end='')
        input()
        os.system('systemctl restart named')
        os.system('systemctl enable named')
        print('Restart Attempted')
    if not(regex.search(fir)):
        print('\nFIR has failed, press enter to attempt restart.', end='')
        input()
        os.system('systemctl restart fir_uwsgi')
        os.system('systemctl enable fir_uwsgi')
        print('Restart Attempted')
    if not(regex.search(rocket)):
        print('\nRocket has failed, press enter to attempt restart.', end='')
        input()
        os.system('systemctl restart rocketchat')
        os.system('systemctl enable rocketchat')
        print('Restart Attempted')
    if not(regex.search(sshd)):
        print('\nSSHD has failed, press enter to attempt restart.', end='')
        input()
        os.system('systemctl restart sshd')
        os.system('systemctl enable sshd')
        print('Restart Attempted')
    #Firewall Recovery
    regex = re.compile('yes')
    if not(regex.search(sshPort)):
        print('\nSSH rule not found, press enter to attempt fix.', end='')
        input()
        os.system('firewall-cmd --permanent --add-service=ssh')
        os.system('firewall-cmd --reload')
        print('Fix Attempted')
    if not(regex.search(dnsPort)):
        print('\nDNS rule not found, press enter to attempt fix.', end='')
        input()
        os.system('firewall-cmd --permanent --add-service=dns')
        os.system('firewall-cmd --reload')
        print('Fix Attempted')
    if not(regex.search(httpPort)):
        print('\nHTTP rule not found, press enter to attempt fix.', end='')
        input()
        os.system('firewall-cmd --permanent --add-service=http')
        os.system('firewall-cmd --reload')
        print('Fix Attempted')
    if not(regex.search(httpsPort)):
        print('\nHTTPS rule not found, press enter to attempt fix.', end='')
        input()
        os.system('firewall-cmd --permanent --add-service=https')
        os.system('firewall-cmd --reload')
        print('Fix Attempted')
            
#Menu
while True:
    os.system('clear')
    print('\nSecurity Farm Maintenance')
    print('1: System Status')
    print('2: Configure System')
    print('3: Backup')
    print('4: Restore')
    print('5: Exit')
    print('\nChoice:', end='')
    selection = int(input())
    if(selection == 1):
        status()
        input('\nPress enter to continue: ')
    if(selection == 2):
        configure()
    if(selection == 3):
        backup()
        input('\nPress enter to continue: ')
    if(selection == 4):
        restore()
        input('\nPress enter to continue: ')
    if(selection == 5):
        print('')
        exit()
    























