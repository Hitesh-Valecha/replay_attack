# replay_attack
Networking project - Man in the middle attack

first create a job by running getsha.py 

from pc1 run master 
    - syntax : `python3 master.py [local ip addr] [port] [sha1 code]`
    - eg     : `python3 master.py 192.168.0.103 9987 e5acb1a96e34cd7f263aada0b69aa58bdd722a03`

from pc2..n run slave
   - syntax : `python3 slave.py [master ip addr] [master port]`
   - eg     : `python3 slave.py 192.168.0.103 9987`

attacker snoops the ip of slave and the port from the network and sends bogus jobs
  - syntax : `python3 attack.py salve-ip port job:adkfljahdlfha:ahfkdshhla no_of_jobs`
  - eg     : `python3 attack.py 192.168.0.104 56775 job:hakfdlska:hfjjakdhk 5`
  
  
Enjoy the Project

Make process in the Networking field and share around the globe open source

Please don't use the project for commercial purposes It is made open source for academic purposes only

Follow me at https://github.com/Hitesh-Valecha

Thank you
