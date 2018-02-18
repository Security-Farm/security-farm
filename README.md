www.securityfarm.net


Someday I'd like to have security farm set up as an installer. For now though it is a VM built in ESXi 6.0u2


Run 'security_farm' as root after deployment. Use this to change the IP address.


v1.00 includes draft documentation in /root and on the wiki. Also available on GitHub.


http://securityfarm.net/files/security_farm_v1.00.zip


All passwords (root, the database passwords, the web interface passwords, etc) NEED TO BE CHANGED if you're going to use this in production.


---
Setting up any aliases for root could interfere with the maintenance script.


This is not a battle-tested product. You will probably encounter oddities. This is built for ESXi 6.0u2. Use the VMware standalone converter for other infrastructure.


You MUST use DNS in one way or another. All 5 domains must have entries pointing to the ip of the box. If you choose to use a domain other then soc.lan you will need to hunt down all refrences to it in apache as well as the individual services. The security_farm script will set up the bind dns server automatically so you can just point your dns at the security_farm vm.


It is only provisioned to 100Gb; use the included LVM resizing instructions to adjust accordingly.


---
portal.soc.lan


/var/www/portal/


-Related files are (for apache): httpd.conf, ssl.conf


-Edit this page to your needs


---
rt.soc.lan


/opt/rt4/


root/password


-Related files are: RT_SiteConfig.pm


-See main documentation for more information


-See enable_rtir.txt for directions on how to enable RTIR


---
rocket.soc.lan


/opt/Rocket.Chat/


root/password


-Made some changes that are pretty easy to figure out 


---
fir.soc.lan


fir.soc.lan/admin


/opt/FIR/


root/password


-Related files are: production.py, installed_apps.txt


-You will have to learn as you go. When you create a user you will have to seperately create a "profile" for that user or they won't be able to see tickets. Business lines can be used at your discretion (eg Network Ops / Host Ops). We're still figuring out the rest of it, documentation is scarce


---
mediawiki.soc.lan


/var/www/mediawiki/


root/password


-Related files are: LocalSettings.php


-If you need to upload files larger then 20mb you will need to look into /etc/php.ini


-LocalSettings.php controls the mime types that are allowed to be uploaded to the wiki


-Wikiformatting is the main thing everyone will need to learn so pages don't look terrible. We use certain pages to create subdirectories to keep stuff organized rather then relying on search


---

For other questions: justin@securityfarm.net. Depending on how busy I am I may not respond; don't take it personally
