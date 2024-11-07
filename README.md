# Projeto Chat com Interface e Registro em Tempo Real

Este projeto implementa um servidor de chat com interface gráfica usando as bibliotecas `tkinter` e `socket` da linguagem Python.

## Funcionalidades

- **Interface gráfica com `Tkinter`**: Exibe um log de mensagens enviadas pelo servidor e registra os clientes conectados em tempo real.
- **Servidor com `socket`**: Configuração de um servidor TCP/IP que permite a conexão de múltiplos clientes simultaneamente.

## Arquivos

### `server.py`

Este arquivo configura o servidor, que:
- Define o `host` e a `porta` para criação do socket TCP com IPv4.
- Configura o servidor para escutar até cinco clientes simultaneamente.
- Possui listas para gerenciar os clientes conectados:
  - `clients`: armazena os sockets dos clientes conectados.
  - `names`: guarda os nomes dos clientes.
  - `connections`: lista de tuplas para exibir as conexões ativas.
- Chama a função `receive()` para iniciar a escuta de conexões.
