# Sistema de Perspectivas Compartilhadas

## Visão Geral
O sistema de perspectivas permite que os usuários compartilhem suas opiniões e comentários sobre um projeto. As perspectivas são armazenadas no localStorage do navegador e são sincronizadas entre diferentes abas e janelas do navegador usando o evento 'storage'.

## Como Funciona
1. Quando um usuário adiciona, atualiza ou exclui uma perspectiva, a alteração é salva no localStorage.
2. O evento 'storage' é disparado em outras abas/janelas abertas do mesmo navegador.
3. Os componentes de perspectiva em outras abas/janelas detectam a alteração e atualizam sua visualização.

## Limitações
- As perspectivas são compartilhadas apenas entre abas/janelas do mesmo navegador e mesmo computador.
- Para compartilhamento completo entre diferentes dispositivos e navegadores, seria necessário implementar um backend com banco de dados.

## Uso
Para usar o sistema de perspectivas:
1. Navegue até a página de perspectivas de um projeto.
2. Use o formulário para adicionar uma nova perspectiva.
3. As perspectivas adicionadas serão visíveis para todos os usuários que acessarem a mesma página no mesmo navegador.