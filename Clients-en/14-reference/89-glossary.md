# CheckBiz360 glossary

This glossary gathers CheckBiz360's most relevant operational terms, in alphabetical order. Each definition includes the English name and a description of its meaning in the context of the system.

---

## A

### Absence
A day or range of days that are an employee's own non-working days: holidays, leave, days off. It is added to the public holidays of their organisation and their branch, blocks their clock-in on those days and can be marked as *paid*, *unpaid* or *not set*.

### AI assistant (Merlin)
Artificial intelligence component that interprets the operational data and presents it as an actionable narrative in the operations dashboard, in the branch detail and in the employee detail. It narrates and prioritises using the figures the screen already shows: it does not recalculate or generate data of its own, so its reading cannot contradict the dashboards. It also narrates the back office onboarding guide.

### Availability (board)
Tab in **Schedules** that shows, by branch and day, how many people are available out of the total, with their coverage percentage, and lets you see who is missing and why. It shows in grey the days on which nobody should be working (public holiday or closure) and in red the coverage gaps. See [Availability board](../04-calendar-and-schedules/98-availability-board.md).

---

## B

### Biometric verification required
Setting that obliges an employee to authenticate with a fingerprint or facial recognition before completing a clock-in from the mobile app. When it is active, the system does not accept the clock-in if the biometrics are not verified correctly on the device.

### Branch
Organisational unit within an organisation representing a workplace, a delegation or any geographical or functional grouping of employees. Each branch has its own coordinates, clocking radius, schedules, effective calendar and time control configuration.

### Break (`restin` / `restout`)
Record of the start (`restin`) and end (`restout`) of a break within the working day. Breaks are or are not deducted from time worked depending on the branch configuration. Like check-in and check-out, breaks require the employee to be within the geofence if it is configured that way. Not to be confused with a *task pause*.

---

## C

### Check-in / Check-out
Record of an employee's entry (check-in) and exit (check-out) time in their working day. They are the fundamental events of time control. A check-in with no corresponding check-out generates an incomplete workday. See also: Clock record / Checklog.

### Clock record / Checklog
Individual record of a time control action carried out by an employee. A checklog includes: event type (checkin, checkout, restin, restout), GPS coordinates, timestamp, device used and validation status. It is the smallest unit of data in the time control module.

### Collaborator (relationship type)
External person who works for the company without being part of the staff: a self-employed professional, a freelancer or a supplier. It is indicated on the employee's record, as opposed to *Staff*. Collaborators do not appear in the working-time record report. Not to be confused with the organisation's *collaborators*, who are the users with access to the back office.

### Configuration inheritance
Mechanism by which employees or branches automatically adopt the configuration defined at a higher level of the hierarchy (for example, from the organisation to the branch, or from the branch to the employee). If a parameter is not explicitly configured at the lower level, the system uses the higher level's value.

---

## D

### Dependency
Indicator measuring how much of a site's operation rests on a few people. It is read directly —*half the operation depends on 1 person*, *depends on 2 people*, *healthy distribution*— and is complemented by the cover-by-position view.

### Document module
Set of CheckBiz360 features allowing employment documents to be uploaded, organised and distributed (contracts, payslips, announcements, company policies, protocols and risk prevention), with visibility by role and a read receipt from the employee. It is included in the subscription, regardless of the plan. Advanced electronic signature is not part of the current version: what exists today is the read receipt.

---

## E

### Effective calendar
Configuration defining the working days and public holidays for a branch or for a particular employee. The effective calendar determines which days the system expects clock records and which days are considered free or holidays. It is configured from the back office in the calendars section.

### Employee
CheckBiz360 user with the Worker, Supervisor or Manager role who is part of an organisation's headcount. On the platform, the term "employee" refers to the data record of a person in the organisation, including their profile, assignments, clock records and documents.

### Error code
Alphanumeric identifier the system returns when an operation cannot be completed. Error codes follow the format `module/error_type` (for example, `checklog/out_of_radius`). They make it possible to identify the exact cause of a failure without having to interpret text messages. See the article [Complete error codes](./90-complete-error-codes.md).

### Evidence
Photo or video an employee attaches to a task to evidence the work carried out. If the task has the evidence requirement enabled, the system does not allow it to be completed without at least one attached file and returns the code `task/evidence_required`.

---

## G

### Geofence / Clocking radius
Circular geographic perimeter defined around a branch's coordinates. Only clock records made within that perimeter are accepted. The radius is measured in metres and is configured from each branch's record in the back office.

---

## I

### Incomplete workday (`incomplete_workday`)
Working day in which there is a check-in but no corresponding check-out, or vice versa. The system automatically marks it as incomplete and excludes it from the calculation of hours worked until it is completed through a manual workday.

---

## M

### Manager
User role able to manage employees, branches, documents, reports and incidents within the branches assigned to them. The Manager acts under the Owner's supervision and cannot modify the organisation's global configuration.

### Manual workday
Retroactive correction of a clock record made by an Owner or Manager from the back office. It is used when an employee forgot to clock in, when the system could not record the event because of a one-off technical failure or when historical attendance data needs adjusting. It is logged with the name of the user who made it and the date of the modification.

### Merlin
See *AI assistant (Merlin)*.

---

## O

### Operational efficiency index
Indicator measuring the balance between the real cost incurred and the expected cost according to the historical pattern. The reference is always the site's or person's own history, not a universal scale or a direct comparison between people.

### Operations dashboard
Back office screen consolidating the period's activity into three views: the comparison between branches, the detail by employee and the period analysis. It is the entry point to operational intelligence and where the AI assistant's narrative appears.

### Organisation / Entity
CheckBiz360's root organisational unit. It corresponds to a company or customer that has contracted the platform. Each organisation can have multiple branches, employees and its own configurations. The Owner is the organisation's ultimate authority.

### Owner
Role with complete access to all of an organisation's features in CheckBiz360. The Owner can manage employees, branches, global configuration, billing and every module available in the plan contracted. Each organisation has at least one Owner.

---

## P

### Pending (employee status)
Status of an employee record that is missing some detail needed to be able to work, usually the email address. It receives no access, is not billed and leaves that status when the detail is completed.

### Promotion score
Single index that would combine reliability, efficiency and ratings into one figure comparable between employees. **It does not exist in the current version**: what does exist is the *operational assessment of the employee*, a diagnosis of their pattern including the promotion-candidate signal. See [Operational assessment of the employee](../07-operational-intelligence/53-promotion-score.md).

### Push notification
Message sent directly to an employee's mobile device through the operating system's notification service (APNs on iOS, FCM on Android). CheckBiz360 uses push notifications to give notice of new tasks, documents pending a read receipt, workday alerts and system announcements.

---

## R

### RDL 8/2019
Royal Decree-Law 8/2019 of 8 March, establishing the working-time recording obligation for all workers in Spain. CheckBiz360 is designed to comply with the requirements of this decree, providing immutable records, with the exact time, available for labour inspection.

### Read receipt
Explicit confirmation that an employee has accessed a document that requires it. It is recorded with the date and the specific version of the document that was read, so that a later version does not inherit the previous one's receipt. It is not an electronic signature: signature with eIDAS validity is on the roadmap.

### Reliability index
Indicator of the quality of the behaviour observed, **separated from how long it has been measured**: somebody who has been with the company a short time does not carry a low reliability because of that. It is one of the three main indices of the Operations dashboard, alongside site effect and dependency.

### Responsibilities (`responsibilities`)
Employee configuration field defining the working areas or specific functions assigned to them within the organisation. Responsibilities can be used for task assignment and as a filtering criterion in reports.

### Role
A user's level of access and permissions within CheckBiz360. The roles available are: Owner, Manager, Supervisor and Worker. Each role has a defined set of actions it can carry out in the back office and in the mobile app.

---

## S

### Schedule adjustment
Concept that **does not apply** in the current version: the clock record always stores the real time and is not rounded. What decides whether time worked outside the official window counts is the calendar's *strict or flexible workday* mode.

### Schedule template
Saved copy of a weekly schedule that is then applied to another branch, to an employee or to the organisation, so as not to configure it day by day. It used to be called a *calendar preset*.

### Shift
Time window assigned to an employee for a particular workday, defining their expected start and finish times. Shifts are configured in the back office and associated with the employee's or the branch's effective calendar.

### Site effect
Indicator comparing each person's performance **at a particular site** with their own overall performance. The average of those differences across everyone who passes through there measures the effect the site exerts on people, with individual talent already discounted. It answers whether the problem is the person or the place.

### Strict / flexible workday
Calendar counting mode. With a **strict workday** the official schedule governs: what is worked before or after is not counted, and delays and early exits are deducted. With a **flexible workday** the real time governs: what is worked outside the window is added as extra. The same distinction exists for breaks.

### Subscription plan
CheckBiz360's contracting mode. There are two: **Bronze**, €5 per employee per month (2026 rate of €2 when subscribing up to and including 31 December 2026), and **Enterprise**, with bespoke pricing, which adds priority support and integrations. Both give access to every module on the platform. See [Plans, prices and features](./91-plans-and-features.md).

### Supervisor
Intermediate role between Manager and Worker. The Supervisor can review the clock records and tasks of the employees on their direct team if the Manager has granted them that capability, but has no access to the branch's global configuration or to cost or anomaly reports.

---

## T

### Task
Unit of work assigned to one or several employees at a branch, with a deadline and, optionally, an expected start date and its own work site. It runs through seven statuses —draft, assigned, in progress, completed, validated, rejected and cancelled—, can be paused while it is in progress and carries a time-compliance indicator independent of the status.

### Task pause
Interruption of a task in progress, which is paused and resumed as many times as needed. It is not a status: the task remains *in progress* and shows the *Paused* label. Time paused is added up separately in the task report. See [Tracking and updates](../06-tasks/43-tracking-and-updates.md#pausing-and-resuming-a-task).

### Team
Template of people who work together, each with their responsibility, job and hourly rate, but no branch. Applying it to a branch adds all its members at once and skips anyone who was already there. Changing the team does not modify the branches where it was already applied. See [Teams](../02-employees/99-teams.md).

### Time compliance
Indicator accompanying each task and reflecting its situation against the deadline, independently of its status. Its values are: not started, on time, at risk, overdue, completed on time and completed late. An overdue task remains in its work status (for example, "in progress"); the overrun is reflected in this indicator, not in the status.

### Trusted device
Mobile device explicitly authorised by the Owner or the Manager so that a particular employee can make clock records from it. The platform can be configured to reject clock records coming from devices not registered as trusted.

---

## V

### Validation token
Temporary code generated by the system to verify a user's identity in sensitive operations, such as the first sign-in, a password reset or the authorisation of a new device. Validation tokens expire after a given time; the employee's one, after 30 days.

---

## W

### Work site (of a task)
A task's own address, with a margin in metres, for jobs that are not done at the branch. Starting or resuming it requires being within the margin, and starting, resuming or completing it can only be done from the app. See [Create a task](../06-tasks/40-create-a-task.md#own-work-site).

### Worker
Base user role in CheckBiz360, corresponding to an operational employee. Workers can clock in from the app, consult their own attendance data, see their documents and manage their tasks. They have no access to the back office unless they are granted a higher role.

### Working off-site
Setting that allows an employee to make clock records from a location other than their branch's geofence. When it is active, the system accepts clock records outside the usual radius without generating the error `checklog/out_of_radius`. It has to be enabled explicitly by the Owner or Manager. It used to be called *Remote work*.

### Working-time record
The set of all the clocking events (checkin, restin, restout, checkout) that make up an employee's complete working day. The working-time record is the unit of analysis for calculating hours, regulatory compliance and report generation.

---

## Role note

This article is freely available to all platform roles: Owner, Manager, Supervisor and Worker.

---

## Related articles

| Article | Description |
|---|---|
| [Complete error codes](./90-complete-error-codes.md) | Reference for every system error code |
| [Plans, prices and features](./91-plans-and-features.md) | Price of each plan, trial period and included modules |
| [Frequently asked questions](./92-frequently-asked-questions.md) | Answers to the most common questions about CheckBiz360 |
| [Time tracking: basic concepts](../03-time-tracking/13-how-clocking-in-works.md) | Introduction to the time control module |
