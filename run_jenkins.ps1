docker run -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts
ssh -R 80:192.168.99.100:8080 serveo.net