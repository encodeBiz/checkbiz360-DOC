# Gerar e filtrar relatórios

O módulo de relatórios do backoffice do CheckBiz360 permite obter documentos detalhados sobre a atividade da sua equipa em qualquer período. Este guia explica o processo completo para gerar um relatório, os filtros disponíveis, como pré-visualizar o resultado antes de exportar e como guardar configurações frequentes para as reutilizar.

---

## Aceder ao módulo de relatórios

Para gerar um relatório tem de aceder ao backoffice do CheckBiz360 com um perfil de Owner, Manager ou, se o manager o tiver ativado, Supervisor.

1. Inicie sessão no backoffice a partir do seu navegador.
2. No menu lateral esquerdo, selecione a secção **Relatórios**.
3. Verá o painel de relatórios com os cinco tipos disponíveis: Assiduidade, Pontualidade, Custos, Anomalias e Tarefas.
4. Selecione o tipo de relatório que pretende gerar.

---

## Filtros disponíveis

Antes de gerar o relatório pode ajustar os parâmetros de filtragem. Quanto mais específicos forem os filtros, mais focado será o resultado e menor será o tempo de geração.

### Intervalo de datas

O filtro de datas é obrigatório. Dispõe das seguintes opções predefinidas:

- **Hoje:** apenas o dia em curso.
- **Esta semana:** de segunda a domingo da semana em curso.
- **Este mês:** mês civil em curso.
- **Intervalo personalizado:** selecione uma data de início e uma data de fim no calendário. Pode abranger até 12 meses consecutivos numa única consulta.

> **Aviso:** os períodos superiores a três meses podem demorar vários minutos a processar, dependendo da dimensão do seu quadro de pessoal e do número de registos acumulados. Ser-lhe-á mostrada uma barra de progresso durante a geração.

### Funcionário

Pode filtrar por um funcionário concreto ou incluir todos os funcionários do âmbito que gere. Se selecionar um funcionário específico, o relatório mostrará apenas os seus registos.

### Sucursal

Se a sua entidade tiver mais do que uma sucursal, pode selecionar uma sucursal concreta ou incluir todas. Os owners e managers com acesso multilocal veem todas as sucursais; os managers com acesso restrito só veem as suas.

### Tipo de evento

Disponível no relatório de assiduidade. Permite filtrar por categoria de registo:

- Apenas entradas e saídas.
- Ausências (justificadas, não justificadas ou ambas).
- Correções manuais efetuadas por um responsável.
- Todos os eventos do período.

---

## Pré-visualização antes de exportar

Depois de configurados os filtros, prima **Pré-visualizar** para ver o relatório no ecrã antes de o descarregar. A pré-visualização mostra os mesmos dados que o ficheiro exportado conterá e permite detetar possíveis erros na seleção de filtros sem necessidade de descarregar o documento.

Na pré-visualização pode:

- Navegar pelas páginas do relatório.
- Verificar que os funcionários e as datas incluídos estão corretos.
- Conferir totais e subtotais.

Se detetar que os filtros não são os adequados, prima **Voltar aos filtros** e ajuste-os sem perder a configuração parcial.

---

## Guardar configurações de relatório frequentes

Se gera habitualmente o mesmo tipo de relatório com os mesmos parâmetros (por exemplo, o relatório de assiduidade mensal de uma sucursal concreta), pode guardar essa configuração para a reutilizar.

1. Configure os filtros pretendidos.
2. Prima **Guardar configuração**.
3. Atribua um nome descritivo, por exemplo: «Assiduidade mensal — Sucursal Centro».
4. A configuração ficará disponível na secção **Os meus relatórios guardados**, acessível a partir do painel principal do módulo.

Para executar uma configuração guardada, selecione-a na lista e prima **Gerar**. Só terá de ajustar o intervalo de datas se a configuração usava um intervalo relativo como «este mês».

> **Nota:** as configurações guardadas são pessoais de cada utilizador do backoffice e não são partilhadas entre contas.

---

## Tempo de geração

O tempo de geração depende de três fatores: o número de funcionários incluídos, o intervalo de datas selecionado e o tipo de relatório.

| Cenário | Tempo estimado |
|---|---|
| Até 20 funcionários, 1 mês | Menos de 10 segundos |
| Até 20 funcionários, 6 meses | 10 a 30 segundos |
| Mais de 100 funcionários, 12 meses | 1 a 5 minutos |

Para períodos longos com quadros de pessoal grandes, recomendamos iniciar a geração do relatório e manter o separador aberto. O sistema notificá-lo-á quando o relatório estiver pronto a descarregar.

---

> **Nota:** o perfil Supervisor só pode gerar relatórios se o manager tiver ativado essa permissão específica na sua configuração de acesso. Se não visualizar a secção de relatórios no backoffice, contacte o manager da sua entidade.

---

## Artigos relacionados

| Artigo | Descrição |
|---|---|
| [Tipos de relatório disponíveis](./76-tipos-de-relatorio.md) | Descrição de cada tipo de relatório e acesso por perfil |
| [Exportar dados](./78-exportar-para-excel-e-csv.md) | Formatos de exportação e campos incluídos |
| [Relatório de conformidade legal](./79-relatorio-de-conformidade-legal.md) | O relatório específico para o RDL 8/2019 |
| [Relatórios automáticos](./80-relatorios-automaticos.md) | Envio periódico de relatórios por email |
