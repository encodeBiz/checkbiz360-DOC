# Multi-organisation employees

CheckBiz360 allows the same person to be linked to several companies within the platform using a single login. This model, known as multi-organisation, is common in business groups, organisations with several legal entities or service providers that work simultaneously for different customers of the platform.

The multi-organisation design guarantees that each company keeps its information completely isolated from the others, while the employee can switch working context easily from the same application.

---

## How the multi-organisation model works

In CheckBiz360, a user's identity is based on their email address and their unique identifier (UID). When that email is added as an employee in more than one organisation (company), the system recognises it as a single user with multiple working contexts.

Each organisation the user is registered in has its own independent space:

- Its own schedules and shifts.
- Different branches.
- Separate documents, contracts and payslips.
- Specific tasks and incidents.
- Roles and access levels that may differ between organisations.

An employee can be a worker at one company and a supervisor at another, without the permissions of one carrying over to the other.

---

## Access flow with multiple organisations

When a user with access to several organisations signs in to CheckBiz360, the process is as follows:

1. The user enters their email and password on the sign-in screen.
2. If they have 2FA enabled, they complete the verification with the code from their authenticator application.
3. After authentication, the platform detects that the user belongs to more than one organisation and shows an **organisation picker**.
4. The user selects the company they want to work with in that session.
5. The application loads the full context of the selected organisation: branches, schedules, tasks, documents and its own configuration.

If the user belongs to only one organisation, the picker does not appear and access is direct.

---

## Organisation-specific session token

Every time the user selects an organisation, the system generates a session token linked exclusively to that company. This design guarantees that:

- The operations the user carries out (clock records, approvals, viewing documents) correspond only to the active organisation.
- It is not possible to accidentally access another company's data without explicitly switching context.
- Access audits and activity trails stay properly separated by organisation.

To switch organisation during the same day, the user has to close the active session and sign in again, repeating the organisation selection process.

---

## Common use cases

### External service providers

A consultant, maintenance technician or freelance professional may provide services to several customers who use CheckBiz360. Each customer has its own organisation on the platform, and the provider appears as a contractor in each of them. From a single app, the provider can clock in at company A in the morning and at company B in the afternoon, with completely independent records.

### Business groups with several legal entities

A corporation may manage several companies under different legal names, each one a separate organisation in CheckBiz360. A corporate HR director can be registered as a manager in all of them, accessing each company's context to review clock records, manage employees or generate reports, without mixing the data of the different organisations.

### Employees with a dual contract

In some cases, an employee may hold simultaneous contracts with two companies in the same group. The multi-organisation model lets them record their activity at each company separately, with independent time records and documentation for each employment relationship.

---

## Registering an employee in several organisations

For a user to appear in several organisations, the process is independent at each company:

1. The manager or owner of each organisation has to create the employee's profile separately in their own company, using the user's same email address.
2. The platform automatically links the profiles to the same UID when it detects that the email already exists in the system.
3. Each organisation can assign the user whatever role and branches it considers appropriate, independently of what has been configured in other organisations.

> **Note:** The fact that a user is registered in several organisations does not mean they can see the information of the others. Each organisation is a completely isolated space. The user only sees the data of the organisation whose session is active at that moment.

---

## Who can manage these configurations

Creating and managing employee profiles at each organisation is the responsibility of the **manager** (level 3) or the **owner** (level 4) of that specific organisation. It is not possible for the manager of one company to manage employees at another company, even if they share users.

---

## Related articles

- [Create and manage employees](06-create-and-manage-employees.md)
- [Roles and responsibility levels](07-roles-and-responsibility-levels.md)
- [Two-factor authentication](09-two-factor-authentication.md)
- [Biometrics and trusted devices](10-biometrics-and-trusted-devices.md)
