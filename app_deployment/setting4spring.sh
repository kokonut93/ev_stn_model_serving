# Install Java
sudo yum update -y
sudo yum install java-11-amazon-corretto.x86_64 -y
sudo yum install git -y

git clone https://github.com/hwangpeng-sam/Back-End.git
cd Back-End

# Install Maven
sudo chmod +x gradlew
./gradlew clean build -x test

# Run
find ./* -name "*jar"
java -jar ./build/libs/plugissue-0.0.1-SNAPSHOT.jar &

#DNS Forwarding
sudo amazon-linux-extras install nginx1 -y
sudo vi /etc/nginx/nginx.conf

'''
location / {
            proxy_pass http://localhost:8080;
            proxy_set_header X-Real_IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header Host $http_host;
    }
'''

sudo systemctl start nginx

# Encrypt (https)
sudo yum install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm -y
sudo yum-config-manager --enable epel
sudo yum install certbot python-certbot-nginx -y

sudo cerbot --nginx


# restart
java -jar ./build/libs/plugissue-0.0.1-SNAPSHOT.jar &
sudo systemctl start nginx