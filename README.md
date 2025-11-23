# 🕹️ Platformer Game

**Um jogo de plataforma 2D criado em Pygame Zero**

Este repositório contém o código-fonte e os assets do **Platformer Game**, um protótipo funcional criado com **Pygame Zero**.
O objetivo é navegar pelas plataformas, evitar inimigos móveis e alcançar a plataforma final para vencer.

---

## 📌 Funcionalidades

* 🎮 **Movimentação completa do herói** (andar, pular, colisões e animações)
* ⚔️ **Inimigos com patrulha automática**
* 🧱 **Plataformas organizadas por níveis**
* 🎵 **Menu com controle de música**
* 🔄 **Estados de jogo completos**: Menu, Jogando, Game Over e Vitória
* 🧠 **Lógica de física integrada** (gravidade, pulo, queda)
* 💥 **Detecção de colisão baseada em distância (math.hypot)**

---

## 📂 Estrutura do Jogo

O protótipo segue a estrutura clássica de jogos em Pygame Zero:

```
main.py
assets/
    images/
    sounds/
README.md
```

---

## 🎮 Como Jogar

* **Seta Esquerda / Direita** → Move o herói
* **Clique do Mouse** → Faz o herói pular
* **Menu Inicial** → Botões de Start, Música e Sair
* **Tela Final** → Botão de Restart

**Objetivo:** Chegue até a plataforma mais alta sem encostar nos inimigos.

---

## 🧱 Plataformas

As plataformas são retângulos posicionados no cenário:

| Nº | Posição    | Tamanho  | Função                     |
| -- | ---------- | -------- | -------------------------- |
| 0  | (10, 490)  | (200×20) | Plataforma inicial         |
| 1  | (300, 360) | (200×20) | Plataforma intermediária 1 |
| 2  | (10, 230)  | (200×20) | Plataforma intermediária 2 |
| 3  | (300, 110) | (200×20) | Plataforma final (vitória) |

---

## 👤 Classe Hero (Jogador)

O herói possui:

* Física própria
* Animações de idle e corrida
* Sistema de pulo
* Sistema de invencibilidade temporária
* Colisão precisa com plataformas

---

## 👾 Classe Enemy (Inimigos)

Cada inimigo:

* Patrulha entre dois limites
* Alterna animações automaticamente
* Inverte o sprite ao mudar de direção

---

## ⚙️ Constantes Globais

| Variável          | Valor | Descrição               |
| ----------------- | ----- | ----------------------- |
| `GRAVITY`         | 0.5   | Puxa o herói para baixo |
| `JUMP_VELOCITY`   | -11   | Força inicial do pulo   |
| `MOVE_SPEED`      | 10    | Velocidade horizontal   |
| `ANIMATION_SPEED` | 10    | Velocidade da animação  |

---

## 🏆 Estados do Jogo

| Estado      | Função                                  |
| ----------- | --------------------------------------- |
| `MENU`      | Tela inicial com botões                 |
| `PLAYING`   | Gameplay                                |
| `GAME_OVER` | Derrota ao colidir com inimigos         |
| `WIN`       | Vitória ao alcançar a última plataforma |

---

## ▶️ Como Executar

### 1. Instale o Pygame Zero

```bash
pip install pygamezero
```

### 2. Execute o jogo

```bash
pgzrun main.py
```

---

## 📘 Baseado em…

Este README reflete diretamente o **GDD completo** criado para este projeto, incluindo lógica, arquitetura e mecânicas utilizadas.

---

## 📜 Licença

Licenciado sob MIT.
Sinta-se livre para estudar, modificar e distribuir este jogo.


Quer adicionar algo?

