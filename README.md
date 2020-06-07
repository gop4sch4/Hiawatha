hiawatha rpm
========

Steps for rpm creating:

    install rpm-build libxslt-devel wget
    
    cd /tmp
    
    ### '6' for centos 6 and change '5' for centos 5
    ### 'x86_64' for 64bit and change to 'i386' for centos 5
    wget http://centos6.ecualinux.com/x86_64/cmake-2.8.4-1.el6.x86_64.rpm
    rpm -ivh cmake-2.8.4-1.el6.x86_64.rpm
    
    wget https://github.com/Hiawatha/raw/patch/hiawatha-9.6-1.mr.src.rpm --no-check-certificate
    rpm -ivh hiawatha-9.6-1.mr.src.rpm
    
    ### for centos 5
    cd /usr/src/redhat/SPECS
    ### for centos 6
    cd /root/rpmbuild/SPECS
    
    ### 'el6' for centos 6 snd change to 'el5' for centos 5
    rpmbuild -bb --define 'dist .mr.el6' hiawatha.spec
    
    
