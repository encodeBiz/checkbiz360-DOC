# What operational intelligence is

Operational intelligence is the most advanced module in CheckBiz360. Its function is not to record when an employee arrives and leaves, but to turn those records into information useful for making business decisions: spotting trends before they become problems, identifying the employees with the greatest potential, comparing real costs between branches and grounding HR decisions in objective data.

A traditional time control system answers the question "was the employee there?". Operational intelligence answers more relevant questions: "does this site bring out the best in its people or wear them down?", "how many people does it depend on for this to keep working?", "who covers this position if the person doing it is absent tomorrow?", "are there clock records whose pattern suggests irregularities?".

That difference rests on three principles worth knowing before interpreting any indicator:

1. **The unit of measurement is the workday, not the person.** Nothing is divided by headcount, everything comes out in proportion; that way a branch of 5 people and one of 40 really can be compared.
2. **Nothing is compared against a universal scale.** Each figure is compared against its own history, against those holding the same position or against the other sites in the same organisation.
3. **Absence of evidence is never negative evidence.** When data is missing, the system says "gathering data"; it never concludes that something is wrong because it cannot measure it.

All of this is consulted in the **Operations dashboard**, described in [The Operations dashboard](./56-dashboards.md), and is accompanied by the **AI assistant's** narrative, which prioritises what to look at first using the same figures the screen displays.

## What data the module analyses

Operational intelligence cross-references information from three different sources that already exist on the platform:

**Attendance and punctuality.** Every clock record is stored with a timestamp and coordinates. The system analyses the real entry and exit time against the planned one, unjustified absences and schedule deviations accumulated over time.

**Tasks and ratings.** The tasks completed by each employee, together with the ratings the manager assigns, feed the performance analysis. An employee who is present is not necessarily a productive employee; the module takes that into account.

**Costs.** Each employee has their hourly rate configured. The system calculates the real cost of each workday by multiplying the hours actually worked by that rate and compares it with the planned cost.

## The EmployeePattern concept

The analysis engine builds for each employee an object called EmployeePattern: a behaviour profile that is updated continuously as new records accumulate. This profile is not a snapshot of the last month; it is a history that captures trends, improvements, deteriorations and anomalies over time.

The employee pattern is the basis on which all the module's indicators are calculated: reliability, operational efficiency, cost, confidence level and the anomaly signals. Without accumulated data there is no pattern; that is why the module gains value with the passage of time.

## What management can do with this data

Before having operational intelligence, team leads depended on memory, subjective impression and manual reports that always arrived late. With the module active, management can:

- Detect early on employees whose reliability is declining, before the problem affects the team.
- Base promotion decisions on objective data rather than personal perceptions.
- Compare the real cost of operation between branches and take corrective measures.
- Identify suspicious clocking patterns that could indicate delegation or manipulation of records.
- Ground difficult conversations with employees in the behaviour history rather than in anecdotes.

## Tangible benefits

**Early detection.** A deterioration in attendance or punctuality rarely happens all at once. The system detects the trend while it is still correctable, not once it has already impacted operations.

**An objective basis for personnel decisions.** The operational assessment of the employee interprets their real pattern and flags, where appropriate, the candidates for promotion. And because the dashboard measures how much the site influences those who pass through it, it makes it possible to distinguish the person from the place before deciding.

**Reduction of hidden costs.** Cost analysis brings to light deviations that go unnoticed in a conventional system: unplanned overtime, incomplete shifts paid in full, productivity differences between sites.

**Fair, documented management.** When a decision is backed by historical data and not by a single manager's opinion, the process is fairer for the employee and more defensible for the company in the face of any claim.

## Limitations worth knowing

Operational intelligence offers indicators, not verdicts. The indices and flags are signals that direct the manager's attention, but they do not replace human judgement. A low score may have legitimate causes that the data does not capture: an employee's personal situation, a badly sized workload or a problem integrating with the team.

> **Important:** The data generated by the operational intelligence module is internal and supports management. It should not be used as the sole basis for disciplinary decisions without an accompanying evaluation process in line with the applicable collective agreement.

## Related articles

- [The employee's behaviour pattern](50-behaviour-pattern.md)
- [Reliability index](51-reliability-index.md)
- [Operational efficiency index](52-efficiency-index.md)
- [Operational assessment of the employee](53-promotion-score.md)
- [Cost analysis](54-cost-analysis.md)
- [Anomaly detection](55-anomaly-detection.md)
- [The Operations dashboard](56-dashboards.md)
