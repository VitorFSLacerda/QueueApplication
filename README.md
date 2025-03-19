QueueApplication - Como usar (PT) / How to use (EN)
===================================================

# Em português (PT):

1. Certifique-se de ter o Docker instalado e estar logado no Docker Hub.

2. Crie a rede compartilhada:
   docker network create callcenter-net

3. Execute o container do servidor (Com acesso SSH):
   docker run -d --name server-container --network callcenter-net -p 5678:5678 -p 2222:22 vitorfslacerda/callcenter-server

4. Execute o container do cliente (Com acesso SSH):
   docker run -it --name client-container --network callcenter-net -p 2223:22 vitorfslacerda/callcenter-client

5. No terminal do cliente, você poderá digitar comandos como:
   - call <id> — Inicia uma chamada com o ID especificado.
   - answer <operator_id> — O operador atende a chamada.
   - reject <operator_id> — O operador rejeita a chamada.
   - hangup <call_id> — Encerra a chamada.

6. Para acessar via SSH:
   - Servidor: ssh root@localhost -p 2222.
   - Cliente: ssh root@localhost -p 2223.

Pronto! O servidor e o cliente estarão conectados e acessíveis via terminal e SSH.


# In English (EN):

1. Make sure Docker is installed and you are logged into Docker Hub.

2. Create the shared network:
   docker network create callcenter-net

3. Run the server container (With SSH access):
   docker run -d --name server-container --network callcenter-net -p 5678:5678 -p 2222:22 vitorfslacerda/callcenter-server

4. Run the client container (With SSH access):
   docker run -it --name client-container --network callcenter-net -p 2223:22 vitorfslacerda/callcenter-client

5. In the client terminal, you can type commands like:
   - call <id> — Start a call with the specified ID.
   - answer <operator_id> — The operator answers the call.
   - reject <operator_id> — The operator rejects the call.
   - hangup <call_id> — Ends the call.

6. To access via SSH:
   - Server: ssh root@localhost -p 2222.
   - Client: ssh root@localhost -p 2223.

That's it! The server and client will be connected, functional, and accessible via terminal and SSH.

