# Gluon.public
인증/실시간전송/쿼리전송 지원 

# Gluon
- Gluon : 끊임없고 강력한 분석력의 결합을 통해 수익을 창출하는 시스템

# build image  
- docker build -t gluon -f Gluon.dockerfile .  

# build and run opensearch
- docker-compose -f Gluon.yml up -d

# after build first run  
- docker run -d -p 22:22/tcp -p 3000:80/tcp -p 3001:81/udp -it --shm-size=2G --name=gluon_instance gluon
- docker start gluon_instance  
- docker attach gluon_instance 

# export and import instance image to disk
- docker export gluon_instance > gluon_instance.tar
- docker import gluon_instance.tar gluon
- docker commit gluon_instance gluon_i

# examine oauth2(-k for https self-signed certificate)
- curl -k -XPOST https://localhost:3000/auth/signup -F grant_type=password -F uid=fury8208 -F password=fury8208 -F scope=user
- curl -k -XPOST https://localhost:3000/auth/signin -F uid=fury8208 -F password=fury8208 -c cookies.txt
- curl -k -XPOST https://localhost:3000/auth/register_sso -F name=OMS -F scope=profile -b cookies.txt
- curl -k -XPOST https://localhost:3000/auth/list_sso -F name="Order Management System" -b cookies.txt
- curl -k -u ${client_id}:${client_secret} -XPOST https://localhost:3000/auth/token -F grant_type=password -F username=fury8208 -F password=fury8208 -F scope=user -b cookies.txt
- curl -k -H "Authorization: Bearer ${access_token}" https://localhost:3000/api/me