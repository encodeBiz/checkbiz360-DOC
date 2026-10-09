# Exportar dados: assiduidade e tarefas

O CheckBiz360 extrai dados da plataforma através de **relatórios**: o de assiduidade, em **PDF ou Excel (XLSX)**, e o de tarefas, em **Excel (XLSX)**. Este artigo descreve ambos, os dados que incluem e as considerações práticas de utilização.

---

## Exportar o diretório de funcionários

> **Estado: Planeada**
> Esta funcionalidade faz parte do roadmap e ainda não está disponível na versão atual.

A listagem de **Funcionários** não gera hoje um ficheiro descarregável. O que funciona é o sentido contrário: a **importação** de funcionários a partir de um CSV, útil ao pôr a plataforma em marcha com um quadro de pessoal grande.

Se precisar de uma extração completa do diretório, solicite-a ao apoio em hola@encodebiz.com. Consulte [Exportar a lista de funcionários](../02-funcionarios/12-exportar-lista-de-funcionarios.md).

---

## Descarregar o relatório de assiduidade (PDF ou Excel)

O relatório de assiduidade é gerado a pedido a partir do backoffice e pode ser descarregado em **PDF** ou em **Excel (XLSX)**. Não existe geração automática nem programada; cada relatório é lançado pelo responsável quando precisa.

Escolha o formato consoante a utilização: **PDF** para apresentar ou arquivar —é o que convém perante uma inspeção— e **Excel** para trabalhar os dados numa folha de cálculo ou passá-los ao gabinete de contabilidade.

### Como gerar e descarregar o relatório de assiduidade

1. Aceda ao backoffice com um perfil de Owner ou Manager.
2. Vá à secção **Relatórios**.
3. Gere um relatório novo e selecione o tipo *Registo de jornada*.
4. Escolha o **formato**: PDF ou Excel (XLSX).
5. Configure o **período** e, se precisar, filtre por sucursal ou funcionário.
6. Gere o relatório. Aparecerá no histórico com o seu tipo e o seu formato.
7. Descarregue-o a partir do histórico, as vezes que forem necessárias.

### Campos incluídos no relatório de assiduidade

| Campo | Descrição |
|---|---|
| Nome | Nome completo do funcionário |
| Sucursal | Sucursal a que o funcionário está atribuído |
| Data | Data do registo (formato DD/MM/AAAA) |
| Hora de entrada | Timestamp do registo de entrada |
| Hora de saída | Timestamp do registo de saída |
| Horas trabalhadas | Total de horas e minutos da jornada registada |
| Estado | Completa, ausência justificada, ausência não justificada, jornada parcial |

O relatório inclui o pessoal da empresa e deixa de fora os funcionários marcados como colaboradores; os que não têm tipo de relação registado são incluídos.

---

## Descarregar o relatório de tarefas (Excel)

O relatório de tarefas é gerado da mesma forma que o de assiduidade, selecionando o tipo *Relatório de tarefas*. Só é produzido em **Excel (XLSX)**.

Admite filtros por **sucursal** e por **estado** da tarefa. O período aplica-se ao **prazo** de cada tarefa, e não à sua data de criação: um relatório de julho reúne as tarefas que venciam em julho, ainda que tenham sido criadas antes.

Além dos dados de cada tarefa, o Excel inclui as colunas **Tempo investido (h)**, **Em pausa (h)**, **N.º de pausas** e **Tempo investido sem pausas (h)**. O que mede cada uma explica-se em [Relatórios de tarefas](../06-tarefas/48-relatorios-de-tarefas.md#o-que-contém).

Se nenhuma tarefa cumprir os filtros, o sistema indica-o e não gera um ficheiro vazio.

---

## Exportação dos painéis de inteligência operacional

> **Estado: Planeada**
> Esta funcionalidade faz parte do roadmap e ainda não está disponível na versão atual.

A exportação direta dos dados dos painéis —custos, anomalias e comparações entre sucursais— para Excel ou CSV está planeada para uma versão futura. Hoje esses dados consultam-se no ecrã; o que se pode exportar são os relatórios de assiduidade e de tarefas descritos acima.

---

## Considerações RGPD ao exportar dados de funcionários

Os ficheiros exportados contêm dados pessoais dos funcionários no sentido do Regulamento Geral sobre a Proteção de Dados (RGPD). A empresa, como responsável pelo tratamento, deve ter em conta o seguinte ao gerir estes ficheiros:

- **Armazenamento seguro.** Os ficheiros exportados devem ser guardados em localizações com acesso restrito. Não devem ser armazenados em pastas partilhadas sem controlo de acesso nem em serviços de armazenamento na nuvem sem cifra ou sem gestão de permissões.
- **Transmissão protegida.** Se enviar o ficheiro por email ao seu gabinete de contabilidade ou a outros destinatários externos, utilize canais cifrados ou proteja o ficheiro com palavra-passe.
- **Minimização de dados.** Exporte apenas os campos e o período de dados necessários para cada finalidade concreta.
- **Registo de atividades.** Se a sua empresa estiver obrigada a manter um registo de atividades de tratamento nos termos do artigo 30.º do RGPD, a exportação e transmissão de dados de funcionários deve estar documentada nesse registo.
- **Período de conservação.** Os ficheiros exportados devem ser eliminados depois de cumprida a sua finalidade, salvo se existir uma obrigação legal de os conservar.

> **Aviso:** o CheckBiz360 mantém os dados originais armazenados na plataforma com as medidas de segurança exigidas pela regulamentação aplicável. Uma vez que os dados são exportados e saem da plataforma, a segurança desses ficheiros é da responsabilidade da sua empresa.

---

> **Nota:** o acesso às funções de exportação exige perfil de Owner ou Manager.

---

## Artigos relacionados

| Artigo | Descrição |
|---|---|
| [Tipos de relatório disponíveis](./76-tipos-de-relatorio.md) | O que contém cada tipo de relatório e quem lhe pode aceder |
| [Gerar e filtrar relatórios](./77-gerar-e-filtrar-relatorios.md) | Passos para gerar um relatório com filtros personalizados |
| [Relatório de conformidade legal](./79-relatorio-de-conformidade-legal.md) | O relatório para o RDL 8/2019 |
| [Conservação e proteção de dados](../12-conformidade-legal/83-conservacao-e-protecao-de-dados.md) | Base legal e direitos dos funcionários sobre os seus dados |
