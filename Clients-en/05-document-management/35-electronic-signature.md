# Read receipt and electronic signature

A document can ask the employee to confirm that they received it. That confirmation is given from the app and, since October 2026, **it is signed with the phone**: the employee confirms with their fingerprint, face or unlock code, and the platform keeps an electronic signature that can be checked outside CheckBiz360. For documents addressed to a single person, such as a payslip or a written warning, the signature **is embedded in the PDF itself**.

---

## What the employee sees

When a document asks for a read receipt, the employee opens it in the app, reads it and taps **Confirm**. The app asks for their fingerprint or face; if the phone has no biometrics, the unlock code; and if it has no screen lock, the account password. Nothing to draw, nothing to install.

If the document is a PDF addressed only to them, on confirming they receive the **signed PDF**, which replaces the previous one in their list. It carries, in the bottom margin of every page in small print, who signed, when and the references to verify it.

> **Note:** if the employee closes the document without confirming, it stays in their pending list.

## What the company sees

On the document page, in the read-receipt section, each confirmation says how it was made:

| Mark | Meaning |
|---|---|
| **Signed and verified (fingerprint or face)** | the employee confirmed with biometrics and the platform verified the signature with their phone's key |
| **Signed and verified (phone unlock)** | the same, with the phone's code, pattern or PIN |
| **Confirmed with password** | the phone has no screen lock; they confirmed by typing their password again |
| **Confirmed by tapping** | confirmations made before signatures existed, or from an app that is not updated |

Next to each signed confirmation there is **Download the signature record**: a one-page PDF with who signed, when, from which phone, which document and which version, the signature, the key used to verify it and the instructions to repeat the check with a standard tool. It is what you hand to an inspection or an expert.

If the document was a PDF for one person, downloading the document already gives you the **signed PDF**. The original is kept on the platform.

## Which documents are signed inside the PDF

Only those addressed to **a single employee**: payslips, written warnings, individual communications. A document for a whole branch or the whole company, such as an internal policy, is confirmed by many people: each confirmation is signed and has its record, but the file is not modified. The same applies to a document that is not a PDF.

## What this signature is worth

It is an **advanced electronic signature** under the eIDAS Regulation: linked to the signer, under their control and bound to the exact content they signed. It is not a qualified signature, which requires a certificate issued by a recognised provider; if a procedure demands one, use an external service.

Two things the company must do for the signature to have full value:

- **Collect the worker's consent.** For confirming with a fingerprint to count as their signature, the employee has to have accepted that means. It is the company's responsibility, not the platform's; how to do it with the platform itself is in the next section.
- **Install the CheckBiz360 certificate**, if you want PDF readers to show the signature in green. Without it, the reader will say the signature is valid but of unknown trust; the check is the same. The certificate is downloaded in the back office, on the company page, **Workspace** tab, **Electronic signature** section, which also gives the steps to install it in Acrobat Reader.

## Checking a signature without the platform (for experts)

The signature record carries everything needed to repeat the check with OpenSSL, a standard tool that ships with any Linux or Mac and installs on Windows. No need to trust CheckBiz360 or any certificate: just maths.

Copy three things from the record: the **signed string** (the "as is" block in section 2), the **signature** in base64 (section 3) and the **public key** in PEM (section 3). Then, in an empty folder:

1. Save the signed string in a file `payload.txt`, exactly as shown, without adding a trailing newline.
2. Save the signature in `sig.b64` and decode it: `base64 -d sig.b64 > sig.der`
3. Save the public key, with its `BEGIN PUBLIC KEY` and `END PUBLIC KEY` lines, in `key.pem`.
4. Check the signature: `openssl dgst -sha256 -verify key.pem -signature sig.der payload.txt` → it must answer **Verified OK**.
5. Check that the key is the one in the record: `openssl pkey -pubin -in key.pem -outform DER | openssl dgst -sha256` → it must match the **public key fingerprint (keyId)** in the record.

That proves **this key signed exactly this string**, and the string contains the document, its version and the hash of its content (or the handover and its documents). To tie the key to the person, the record says when it was registered and from which phone, and the worker's consent closes the loop.

If the expert prefers the original evidence file in JSON, with the same data and its own SHA-256, support can provide it from the record number.

## Collecting consent with the platform itself

Consent needs no paper: it is collected like any other read receipt, so it is dated, signed and has its record.

1. Write a short document, **"Electronic signature terms"**, stating: that confirming a document or a handover from the CheckBiz360 app with a fingerprint, face or phone code is the worker's electronic signature and has the same value as their handwritten signature for internal purposes; that the key is created on their phone and never leaves it; that if their phone has no screen lock they will confirm with their account password; that they can ask at any time for a copy of what they signed and its record; and whom to contact with questions. Have your legal adviser review it.
2. Upload it **to each branch** with **Requires read confirmation** enabled, visible to all roles. Read receipts are requested per branch or per employee, not for the whole company at once.
3. Each worker confirms it from the app. That confirmation is the consent record: who, when and on which text, with its signature record if done from the updated app.
4. For those who join later, include it in the contract or upload it to them individually when you set them up.

Until a worker has confirmed it, treat them as confirming by tapping: the platform records the same, but the company will not hold the consent that backs the signature.

## Downloading and installing the CheckBiz360 certificate

Only needed if you want Acrobat Reader to show signatures **in green**. Without it, the reader says the document has not been modified and the signature is valid, but that the signer's identity is "unknown" because CheckBiz360 is not in its trust list. The check is the same either way.

**Download:** in the back office, open the company page, **Workspace** tab, **Electronic signature** section, and click **Download the certificate (.zip)**. Unzip it: it holds the same certificate in two formats, **checkbiz360-firma-ca.cer** for Acrobat and Windows and **checkbiz360-firma-ca.crt** as text for the Mac keychain or Linux, plus a file with these instructions.

**Install in Acrobat Reader:**

1. Open **Edit → Preferences → Signatures**.
2. Under **Identities & Trusted Certificates**, click **More**.
3. Go to **Trusted Certificates** and click **Import**.
4. Choose the **.cer** file and, in the certificate options, tick **Use this certificate as a trusted root**. Confirm.
5. Close the signed PDF and reopen it: the signature now shows in green.

**If the company has several computers (Windows):** IT can install it once per machine, or by policy, in the Windows certificate store under **Trusted Root Certification Authorities**, and in Acrobat, under **Preferences → Signatures → Verification → More**, tick trusting the root certificates in the Windows store.

> **Note:** on Mac, Preview does not check signatures; use Acrobat Reader, where the steps are the same.

**Other readers and validators.** Acrobat is not mandatory: the signature is PAdES, the European standard, and Foxit, PDF-XChange or LibreOffice validate it too, each with its own way of importing the certificate. AutoFirma is a tool for signing with recognised certificates, not for validating; the Spanish public validator, VALIDe, will confirm the document has not been modified but will flag the signer's certificate as not recognised, because CheckBiz360 is not a qualified provider. To prove the signature before an expert, the signature record is enough: it is checked without any trust list.

## How to enable the read receipt

1. When uploading or editing the document, enable **Requires read confirmation**.
2. For a payslip or a written warning, upload the document **to the employee** (employee scope): that is what allows it to be signed inside the PDF.
3. Check that the document is visible to its recipient.

If document notifications are enabled, the employee gets a notification with the pending document.

---

## Related articles

- [What is the document module](30-what-is-the-document-module.md)
- [Upload and organise documents](31-upload-and-organise-documents.md)
- [Payslips and contracts](32-payslips-and-contracts.md)
- [Private documents](33-private-documents.md)
- [Document notifications](34-document-notifications.md)
- [First sign-in to the app](../10-mobile-app/70-first-sign-in.md)
