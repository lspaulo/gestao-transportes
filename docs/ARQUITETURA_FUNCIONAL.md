# Arquitetura Funcional

## Objetivo

Sistema para gerenciamento de adiantamentos e prestações de contas do setor de transportes.

O sistema controla desde a solicitação do adiantamento até sua eventual prestação de contas, respeitando a segregação por setor e empresa.

---

# Perfis

## Operador

- Cadastra adiantamentos.
- Edita adiantamentos em rascunho.
- Exclui adiantamentos em rascunho.
- Gera PDFs.
- Recebe os PDFs por e-mail.
- Visualiza apenas seu setor.

## Gestor

Possui as mesmas permissões do Operador.

## Administrador

Visualiza todos os setores.

Pode administrar qualquer cadastro.

---

# Fluxo do Adiantamento

Rascunho

↓

Gerar PDF

↓

Solicitado

↓

(opcional)

Prestado

ou

Cancelado

---

# Status

## Rascunho

Adiantamento em elaboração.

Pode ser editado ou excluído.

## Solicitado

PDF gerado.

E-mail enviado ao usuário.

Fim do processo para a maioria dos adiantamentos.

## Prestado

Adiantamento utilizado em uma prestação de contas.

## Cancelado

Solicitação cancelada.

---

# Geração de PDFs

O usuário seleciona um ou mais adiantamentos.

O sistema agrupa automaticamente por empresa.

Cada empresa gera um PDF independente.

Cada PDF é enviado ao e-mail do usuário logado.

O usuário revisa e encaminha manualmente ao Financeiro.

---

# Prestação de Contas

Ao selecionar um motorista, o sistema lista automaticamente todos os adiantamentos do motorista com status SOLICITADO.

Todos vêm marcados.

O usuário pode desmarcar aqueles que não pertencem à prestação.

---

# Modelos

O sistema permitirá criar modelos reutilizáveis.

Exemplo:

- Sexta-feira
- Segunda-feira
- Safra

Os modelos pertencem ao setor.

Nunca ao usuário.

---

# Lotes

O conceito de lote será interno ao sistema.

O usuário não visualizará os lotes.

Cada geração de PDF poderá originar um lote interno apenas para auditoria.

---

# Numeração

Adiantamentos terão numeração amigável.

Exemplo:

AD-2026-000001

Prestação de Contas terá numeração própria.

Exemplo:

PC-2026-000001

---

# Regras

Empresa será obtida automaticamente a partir do motorista.

Setor será obtido automaticamente a partir do usuário.

Conta bancária padrão será sugerida automaticamente.

Caso existam várias contas, o usuário poderá alterar.

Os operadores somente visualizarão adiantamentos do próprio setor.

Administradores visualizarão todos os setores.