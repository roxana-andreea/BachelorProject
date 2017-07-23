# Raspberry Installation Procedure
## Initial Setup
### Update Firmware
>rpi-update
>reboot
### Install Packages
>apt-get install -y ansible git  
git clone https://gitlab.com/licenta2016/backend.git /root/backend  
mv /etc/ansible /etc/ansible.bk  
ln -s /root/backend/ansible /etc/ansible  
vi /etc/ansible/group_vars/all.yml
vi /etc/ansible/host_vars/rpi3.yml
ansible-playbook rpi.yml -l rpi3

