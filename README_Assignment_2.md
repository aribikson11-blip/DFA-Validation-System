# Assignment 2: Designing Automata for Real-Time Applications

**Course:** 21CSC301T -- Formal Language and Automata\
**Assessment:** Continuous Learning Assessment 2 -- Task 2

This project demonstrates finite-automata-based validation for three
real-time applications:

1.  Password Verification System
2.  Email Format Validator
3.  ATM PIN Verification System

The Python program checks input formats using deterministic state-based
validation. These checks validate syntax and format; they do not
authenticate a real user or contact an email server or bank.

------------------------------------------------------------------------

## 1. Password Verification System

### Validation Rules

A password is accepted if it:

-   Contains between 8 and 16 characters.
-   Contains at least one uppercase letter.
-   Contains at least one lowercase letter.
-   Contains at least one digit.
-   Contains at least one special character from `@#$%&*!?`.
-   Contains no characters outside the permitted categories.

### Formal Language Description

Let the input alphabet be divided into four character categories:

``` text
U = uppercase letters (A-Z)
L = lowercase letters (a-z)
D = digits (0-9)
S = special characters (@ # $ % & * ! ?)
```

The accepted language consists of strings of length 8 to 16 that contain
at least one symbol from each of U, L, D and S.

A compact state representation is:

``` text
State = (length, category_mask)

Category bits:
U = 0001
L = 0010
D = 0100
S = 1000

Accepting category mask = 1111
Accepting length = 8 to 16
```

The category mask is updated by setting the bit corresponding to each
character category. A dead state is entered for any unsupported
character or when the length exceeds 16.

### DFA State Diagram (Conceptual)

The following diagram shows the four required category flags. The
complete DFA also tracks the length counter from 0 to 16.

``` mermaid
flowchart TD
    A(["Start: mask 0000, length 0"]) --> B["Read next character"]
    B --> C{"Character category?"}
    C -->|Uppercase| U["Set U bit"]
    C -->|Lowercase| L["Set L bit"]
    C -->|Digit| D["Set D bit"]
    C -->|Allowed special| S["Set S bit"]
    C -->|Other character| X(["Reject / dead state"])
    U --> N["Increase length"]
    L --> N
    D --> N
    S --> N
    N --> O{"Length exceeds 16?"}
    O -->|Yes| X
    O -->|No| P{"More input?"}
    P -->|Yes| B
    P -->|No| Q{"Length 8-16 and mask 1111?"}
    Q -->|Yes| R(["ACCEPT"])
    Q -->|No| X
```

### Examples

Accepted:

``` text
Hello@123
Ribik@2026
Abcd#1234
Pass!word9
Test@123A
```

Rejected:

``` text
hello123       (no uppercase or special character)
HELLO@123      (no lowercase character)
HelloWorld@    (no digit)
Hello1234      (no special character)
Hi@12          (fewer than 8 characters)
```

------------------------------------------------------------------------

## 2. Email Format Validator

### Validation Rules

The simplified validator accepts an email address if:

-   It contains exactly one `@` symbol.
-   The local part is not empty and does not start or end with a dot.
-   The local part does not contain consecutive dots.
-   The local part contains only letters, digits, `.`, `_`, `%`, `+` or
    `-`.
-   The domain contains at least one dot.
-   Each domain label is non-empty and does not start or end with a
    hyphen.
-   Domain labels contain only letters, digits or hyphens.
-   The final domain label contains at least two letters.

### Formal Language Description

The validator separates the input into a local part and a domain part
using the single `@` symbol.

``` text
Email = LocalPart @ Domain

LocalPart:
- Letters, digits, dot, underscore, percent, plus and hyphen
- Must not start or end with a dot
- Must not contain consecutive dots

Domain:
- One or more non-empty labels separated by dots
- Labels may contain letters, digits and internal hyphens
- Final label must contain at least two letters
```

This is a simplified email-format rule set for the assignment, not a
complete implementation of every email-address standard.

### DFA State Diagram (Conceptual)

``` mermaid
flowchart TD
    A(["Start"]) --> B["Read local part"]
    B --> C{"Valid local character?"}
    C -->|Yes| B
    C -->|No: @| D["Move to domain"]
    C -->|Other| X(["REJECT"])
    D --> E["Read domain label"]
    E --> F{"Valid domain character?"}
    F -->|Letter or digit| E
    F -->|Hyphen| G["Check hyphen is internal"]
    G --> E
    F -->|Dot| H["Finish non-empty label"]
    H --> I["Read next domain label"]
    I --> J{"Another dot or @ invalid?"}
    J -->|Invalid structure| X
    J -->|Continue| E
    E --> K["Check final TLD: at least 2 letters"]
    K --> L{"All format conditions satisfied?"}
    L -->|Yes| M(["ACCEPT"])
    L -->|No| X
```

### Examples

Accepted:

``` text
user@gmail.com
ribikson123@yahoo.com
student.srm@outlook.com
name_123@example.org
first-last@mail.co
```

Rejected:

``` text
user@gmail          (no dot in domain)
@gmail.com          (empty local part)
user@@gmail.com     (more than one @)
user..name@mail.com (consecutive dots in local part)
user@-mail.com      (domain label starts with hyphen)
```

------------------------------------------------------------------------

## 3. ATM PIN Verification System

### Validation Rules

The ATM PIN format is accepted if:

-   It contains only digits from 0 to 9.
-   It contains exactly 4 or exactly 6 digits.
-   No letters or special characters are allowed.

### Formal Language Description

Let:

``` text
Σ = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
```

The accepted language is:

``` text
L = { w ∈ Σ* | length(w) = 4 or length(w) = 6 }
```

The DFA counts the number of digits read. Any non-digit leads to a dead
state.

### DFA State Diagram

``` mermaid
flowchart LR
    A(["Start q0"]) -->|"digit"| B["q1"]
    B -->|"digit"| C["q2"]
    C -->|"digit"| D["q3"]
    D -->|"digit"| E(["q4: ACCEPT"])
    E -->|"digit"| F["q5"]
    F -->|"digit"| G(["q6: ACCEPT"])
    A -->|"non-digit"| X(["Dead state"])
    B -->|"non-digit"| X
    C -->|"non-digit"| X
    D -->|"non-digit"| X
    E -->|"non-digit"| X
    F -->|"non-digit"| X
    G -->|"any extra input"| X
```

For a complete DFA, every digit transition from `q4` continues to `q5`,
every digit transition from `q5` goes to `q6`, and every further input
from `q6` goes to the dead state. All non-digit transitions go to the
dead state.

### Examples

Accepted:

``` text
1234
0000
123456
908172
```

Rejected:

``` text
123          (only 3 digits)
12345        (5 digits)
1234567      (7 digits)
12AB         (contains letters)
12@4         (contains a special character)
```

------------------------------------------------------------------------

## 4. Why Finite Automata Are Suitable

Finite automata are suitable for these examples because the validation
rules depend on a finite amount of information:

-   **Password verification:** The DFA can track the length and whether
    each required character category has appeared.
-   **Email format validation:** The simplified format rules can be
    checked by a finite-state scanner that tracks the current part and
    relevant local/domain conditions.
-   **ATM PIN verification:** The DFA only needs to count digits up to
    the required lengths and reject invalid characters.

A DFA is sufficient for syntax and format validation. Additional
application logic is needed for semantic or business checks, such as
checking a password against a stored hash, confirming that an email
address exists, or verifying a PIN with a bank.

------------------------------------------------------------------------

## 5. Limitations

1.  The password validator checks character requirements only; it does
    not measure password strength or authenticate a user.
2.  The email validator checks a simplified syntax and does not prove
    that the mailbox or domain exists.
3.  The ATM PIN validator checks only the number and type of characters;
    it does not verify the PIN against a bank account.
4.  The diagrams are conceptual summaries. A fully expanded DFA would
    show every combination of length and category flags for the password
    validator, and detailed intermediate states for the email validator.

------------------------------------------------------------------------

## 6. Conclusion

This assignment demonstrates how finite automata can be applied to
real-time input-format validation. The password validator tracks
required character categories and length, the email validator checks a
simplified email structure, and the ATM PIN validator counts numeric
characters. These examples show how DFA-based validation can identify
accepted and rejected strings before additional application-level
processing is performed.
