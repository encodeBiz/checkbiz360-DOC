# Document access permissions

The CheckBiz360 document module applies a role-based permission model that determines which actions each user can perform on documents. Understanding this structure is essential to configuring access correctly, protecting sensitive documentation and guaranteeing that each person in the organisation sees only what concerns them.

## Roles and general permissions

CheckBiz360 defines four main roles with different levels of access to the document module:

| Action | Worker | Supervisor | Manager | Owner |
|---|---|---|---|---|
| View own documents | Yes (public) | Yes (public) | Yes (all) | Yes (all) |
| View other employees' documents | No | Their team only (if permitted) | Yes (their organisation) | Yes (whole organisation) |
| Upload documents | No | Subject to delegation | Yes | Yes |
| Edit documents | No | Subject to delegation | Yes | Yes |
| Delete documents | No | No | Yes | Yes |
| Request a signature | No | No | Yes | Yes |
| Acknowledge receipt | Yes (their own) | Yes (their own) | Not applicable | Not applicable |
| View private documents | No | Subject to delegation | Yes | Yes |
| Export documents | No | No | Yes | Yes |

> **Note:** This table reflects each role's default permissions. Supervisors' specific permissions can be extended or restricted through the delegation configured by the manager. The Owner's permissions cannot be modified.

## Visibility of payslips and contracts

Payslips and contracts are the most common document types and also the ones that most frequently raise questions about who can access them.

### Payslips

- **Owner and Manager**: can see the payslips of every employee in the organisation, regardless of whether they are marked as private or not.
- **Supervisor**: can see the payslips of the employees on their team only if the manager has granted them explicit access to that team's documents. By default, the supervisor has no access to payslips.
- **Worker**: can see their own payslips if they are not marked as private. They cannot see any other employee's payslips.

### Contracts

The same rules apply to contracts. An employee can see their own contract if it is published and not private. They cannot see their colleagues' contracts.

## Restrictions through the private field

When a document has the `private` field enabled, visibility restrictions apply as follows:

- The document is invisible to the employee (Worker) regardless of whether it is published.
- The supervisor can only see the document if they have delegated permissions to manage the affected team's documents and if the manager has expressly granted them access to private documents.
- The Manager and the Owner can always see every document, including private ones.

This hierarchy guarantees that sensitive information —such as disciplinary notes, appraisals or reprimand letters— stays protected from unauthorised access.

## Delegating permissions from Manager to Supervisor

The manager can extend a supervisor's permissions to include document management for their team. This lets the supervisor take on responsibility for uploading and organising documents without needing to be given full manager access.

Delegation can cover:

- **Uploading documents**: the supervisor can create and publish documents for the employees on their team.
- **Editing documents**: the supervisor can modify the metadata of existing documents for their team.
- **Visibility of private documents**: the supervisor can see documents marked as private for the employees on their team.

> **Important:** Delegating permissions does not turn the supervisor into a manager. A supervisor with extended document permissions can only act on the employees of their assigned team. They have no access to the module's global configuration, to other teams' documents or to bulk export of the archive.

To configure permission delegation:

1. Sign in to the back office as Manager or Owner.
2. Navigate to the **Employee management** or **Team configuration** section.
3. Select the supervisor you want to delegate permissions to.
4. In the supervisor's permissions section, enable the corresponding document options.
5. Save the changes.

## Deletion permissions

Deleting documents is an irreversible action that only users with the Manager or Owner role can perform. Before deleting a document, check:

- If the document has a registered signature, deletion will also erase the signature traceability record.
- If the document forms part of a file that has to be retained by legal obligation, do not delete it even if its immediate operational usefulness has ended.

Marking obsolete documents as private rather than deleting them is recommended, especially for documents with a signature or with employment relevance, so as to preserve the history without exposing the document to the employee.

## Related articles

- [What the document module is](30-what-is-the-document-module.md)
- [Private documents](33-private-documents.md)
- [Read receipt](35-electronic-signature.md)
- [Export documents](38-export-documents.md)
- [Upload and organise documents](31-upload-and-organise-documents.md)
