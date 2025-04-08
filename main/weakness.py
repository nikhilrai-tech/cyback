
weaknesses = [
        {
            "id": 120,
            "name": "Allocation of Resources Without Limits or Throttling",
            "description": "The software allocates a reusable resource or group of resources on behalf of an actor without imposing any restrictions on how many resources can be allocated, in violation of the intended security policy for that actor.",
            "external_id": "cwe-770",
            "cluster_ids": [],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 12,
            "name": "Array Index Underflow",
            "description": "The product uses untrusted input when calculating or using an array index, but the product does not validate or incorrectly validates the index to ensure the index references a valid position within the array.",
            "external_id": "cwe-129",
            "cluster_ids": [
                7
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 142,
            "name": "Authentication Bypass Using an Alternate Path or Channel",
            "description": "A product requires authentication, but the product has an alternate path or channel that does not require authentication.",
            "external_id": "cwe-288",
            "cluster_ids": [
                5
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 31,
            "name": "Brute Force",
            "description": "The software does not implement sufficient measures to prevent multiple failed authentication attempts within in a short time frame, making it more susceptible to brute force attacks.",
            "external_id": "cwe-307",
            "cluster_ids": [
                5,
                43,
                45,
                32,
                36,
                38
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 9,
            "name": "Buffer Over-read",
            "description": "The software reads from a buffer using buffer access mechanisms such as indexes or pointers that reference memory locations after the targeted buffer.",
            "external_id": "cwe-126",
            "cluster_ids": [
                7
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 7,
            "name": "Buffer Underflow",
            "description": "The software writes to a buffer using an index or pointer that references a memory location prior to the beginning of the buffer.",
            "external_id": "cwe-124",
            "cluster_ids": [
                7
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 10,
            "name": "Buffer Under-read",
            "description": "The software reads from a buffer using buffer access mechanisms such as indexes or pointers that reference memory locations prior to the targeted buffer.",
            "external_id": "cwe-127",
            "cluster_ids": [
                7
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 65,
            "name": "Business Logic Errors",
            "description": "Weaknesses in this category identify some of the underlying problems that commonly allow attackers to manipulate the business logic of an application.",
            "external_id": "cwe-840",
            "cluster_ids": [
                8
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 3,
            "name": "Classic Buffer Overflow",
            "description": "The program copies an input buffer to an output buffer without verifying that the size of the input buffer is less than the size of the output buffer, leading to a buffer overflow.",
            "external_id": "cwe-120",
            "cluster_ids": [
                7
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 33,
            "name": "Cleartext Storage of Sensitive Information",
            "description": "The application stores sensitive information in cleartext within a resource that might be accessible to another control sphere.",
            "external_id": "cwe-312",
            "cluster_ids": [
                10,
                16,
                43,
                46,
                8
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 34,
            "name": "Cleartext Transmission of Sensitive Information",
            "description": "The software transmits sensitive or security-critical data in cleartext in a communication channel that can be sniffed by unauthorized actors.",
            "external_id": "cwe-319",
            "cluster_ids": [
                10,
                16,
                43,
                46,
                32,
                35,
                8
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 102,
            "name": "Client-Side Enforcement of Server-Side Security",
            "description": "The software is composed of a server that relies on the client to implement a mechanism that is intended to protect the server.",
            "external_id": "cwe-602",
            "cluster_ids": [
                32,
                40
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 70,
            "name": "Code Injection",
            "description": "The software constructs all or part of a code segment using externally-influenced input from an upstream component, but it does not neutralize or incorrectly neutralizes special elements that could modify the syntax or behavior of the intended code segment.",
            "external_id": "cwe-94",
            "cluster_ids": [
                43,
                44,
                9
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 58,
            "name": "Command Injection - Generic",
            "description": "The software constructs all or part of a command using externally-influenced input from an upstream component, but it does not neutralize or incorrectly neutralizes special elements that could modify the intended command when it is sent to a downstream component.",
            "external_id": "cwe-77",
            "cluster_ids": [
                10,
                11,
                43,
                44,
                32,
                33,
                9
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 140,
            "name": "Concurrent Execution using Shared Resource with Improper Synchronization ('Race Condition')",
            "description": "The program contains a code sequence that can run concurrently with other code, and the code sequence requires temporary, exclusive access to a shared resource, but a timing window exists in which the shared resource can be modified by another code sequence that is operating concurrently.",
            "external_id": "cwe-362",
            "cluster_ids": [],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 69,
            "name": "CRLF Injection",
            "description": "The software uses CRLF (carriage return line feeds) as a special element, e.g. to separate lines or records, but it does not neutralize or incorrectly neutralizes CRLF sequences from inputs.",
            "external_id": "cwe-93",
            "cluster_ids": [
                9
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 45,
            "name": "Cross-Site Request Forgery (CSRF)",
            "description": "The web application does not, or can not, sufficiently verify whether a well-formed, valid, consistent request was intentionally provided by the user who submitted the request.",
            "external_id": "cwe-352",
            "cluster_ids": [
                10,
                18,
                32,
                33
            ],
            "state": "enabled",
            "context_type": "CsrfContext"
        },
        {
            "id": 63,
            "name": "Cross-site Scripting (XSS) - DOM",
            "description": "In DOM-based XSS, the client performs the injection of XSS into the page; in the other types, the server performs the injection. DOM-based XSS generally involves server-controlled, trusted script that is sent to the client, such as Javascript that performs sanity checks on a form before the user submits it. If the server-supplied script processes user-supplied data and then injects it back into the web page (such as with dynamic HTML), then DOM-based XSS is possible.",
            "external_id": "cwe-79",
            "cluster_ids": [
                10,
                13,
                43,
                50,
                32,
                33,
                9
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 60,
            "name": "Cross-site Scripting (XSS) - Generic",
            "description": "The software does not neutralize or incorrectly neutralizes user-controllable input before it is placed in output that is used as a web page that is served to other users.",
            "external_id": "cwe-79",
            "cluster_ids": [
                10,
                13,
                43,
                50,
                32,
                33,
                9
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 61,
            "name": "Cross-site Scripting (XSS) - Reflected",
            "description": "The server reads data directly from the HTTP request and reflects it back in the HTTP response. Reflected XSS exploits occur when an attacker causes a victim to supply dangerous content to a vulnerable web application, which is then reflected back to the victim and executed by the web browser. The most common mechanism for delivering malicious content is to include it as a parameter in a URL that is posted publicly or e-mailed directly to the victim. URLs constructed in this manner constitute the core of many phishing schemes, whereby an attacker convinces a victim to visit a URL that refers to a vulnerable site. After the site reflects the attacker's content back to the victim, the content is executed by the victim's browser.",
            "external_id": "cwe-79",
            "cluster_ids": [
                10,
                13,
                43,
                50,
                32,
                33,
                9
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 62,
            "name": "Cross-site Scripting (XSS) - Stored",
            "description": "The application stores dangerous data in a database, message forum, visitor log, or other trusted data store. At a later time, the dangerous data is subsequently read back into the application and included in dynamic content. From an attacker's perspective, the optimal place to inject malicious content is in an area that is displayed to either many users or particularly interesting users. Interesting users typically have elevated privileges in the application or interact with sensitive data that is valuable to the attacker. If one of these users executes malicious content, the attacker may be able to perform privileged operations on behalf of the user or gain access to sensitive data belonging to the user. For example, the attacker might inject XSS into a log message, which might not be handled properly when an administrator views the logs.",
            "external_id": "cwe-79",
            "cluster_ids": [
                10,
                13,
                43,
                50,
                32,
                33,
                9
            ],
            "state": "enabled",
            "context_type": "XssStoredContext"
        },
        {
            "id": 32,
            "name": "Cryptographic Issues - Generic",
            "description": "Weaknesses in this category are related to the use of cryptography.",
            "external_id": "cwe-310",
            "cluster_ids": [
                6,
                10,
                16,
                43,
                46,
                32,
                37
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 48,
            "name": "Denial of Service",
            "description": "The software does not properly restrict the size or amount of resources that are requested or influenced by an actor, which can be used to consume more resources than intended.",
            "external_id": "cwe-400",
            "cluster_ids": [
                8
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 52,
            "name": "Deserialization of Untrusted Data",
            "description": "The application deserializes untrusted data without sufficiently verifying that the resulting data will be valid.",
            "external_id": "cwe-502",
            "cluster_ids": [
                43,
                51,
                8,
                9
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 49,
            "name": "Double Free",
            "description": "The product calls free() twice on the same memory address, potentially leading to modification of unexpected memory locations.",
            "external_id": "cwe-415",
            "cluster_ids": [
                7
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 149,
            "name": "Download of Code Without Integrity Check",
            "description": "The product downloads source code or an executable from a remote location and executes the code without sufficiently verifying the origin and integrity of the code.",
            "external_id": "cwe-494",
            "cluster_ids": [
                55
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 108,
            "name": "Embedded Malicious Code",
            "description": "The application contains code that appears to be malicious in nature.",
            "external_id": "cwe-506",
            "cluster_ids": [],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 146,
            "name": "Execution with Unnecessary Privileges",
            "description": "The software performs an operation at a privilege level that is higher than the minimum level required, which creates new weaknesses or amplifies the consequences of other weaknesses.",
            "external_id": "cwe-250",
            "cluster_ids": [
                54
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 137,
            "name": "Exposed Dangerous Method or Function",
            "description": "The software provides an Applications Programming Interface (API) or similar interface for interaction with external actors, but the interface includes a dangerous method or function that is not properly restricted.",
            "external_id": "cwe-749",
            "cluster_ids": [],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 123,
            "name": "External Control of Critical State Data",
            "description": "The software stores security-critical state information about its users, or the software itself, in a location that is accessible to unauthorized actors.",
            "external_id": "cwe-642",
            "cluster_ids": [],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 111,
            "name": "Externally Controlled Reference to a Resource in Another Sphere",
            "description": "The product uses an externally controlled name or reference that resolves to a resource that is outside of the intended control sphere.",
            "external_id": "cwe-610",
            "cluster_ids": [],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 136,
            "name": "Failure to Sanitize Special Elements into a Different Plane (Special Element Injection)",
            "description": "The software does not adequately filter user-controlled input for special elements with control implications.",
            "external_id": "cwe-75",
            "cluster_ids": [],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 126,
            "name": "File and Directory Information Exposure",
            "description": "The product stores sensitive information in files or directories that are accessible to actors outside of the intended control sphere.",
            "external_id": "cwe-538",
            "cluster_ids": [],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 85,
            "name": "Forced Browsing",
            "description": "The web application does not adequately enforce appropriate authorization on all restricted URLs, scripts, or files.",
            "external_id": "cwe-425",
            "cluster_ids": [
                5,
                43,
                48,
                32,
                36,
                38
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 5,
            "name": "Heap Overflow",
            "description": "A heap overflow condition is a buffer overflow, where the buffer that can be overwritten is allocated in the heap portion of memory, generally meaning that the buffer was allocated using a routine such as malloc().",
            "external_id": "cwe-122",
            "cluster_ids": [
                7
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 86,
            "name": "HTTP Request Smuggling",
            "description": "When malformed or abnormal HTTP requests are interpreted by one or more entities in the data flow between the user and the web server, such as a proxy or firewall, they can be interpreted inconsistently, allowing the attacker to \"smuggle\" a request to one device without the other device being aware of it.",
            "external_id": "cwe-444",
            "cluster_ids": [
                9
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 1,
            "name": "HTTP Response Splitting",
            "description": "The software receives data from an upstream component, but does not neutralize or incorrectly neutralizes CR and LF characters before the data is included in outgoing HTTP headers.",
            "external_id": "cwe-113",
            "cluster_ids": [
                9
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 26,
            "name": "Improper Access Control - Generic",
            "description": "The software does not restrict or incorrectly restricts access to a resource from an unauthorized actor.",
            "external_id": "cwe-284",
            "cluster_ids": [
                5,
                10,
                17,
                43,
                48,
                32,
                36,
                38
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 27,
            "name": "Improper Authentication - Generic",
            "description": "When an actor claims to have a given identity, the software does not prove or insufficiently proves that the claim is correct.",
            "external_id": "cwe-287",
            "cluster_ids": [
                5,
                10,
                12,
                17,
                43,
                45,
                48,
                32,
                33,
                36,
                38
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 124,
            "name": "Improper Authorization",
            "description": "The software does not perform or incorrectly performs an authorization check when an actor attempts to access a resource or perform an action.",
            "external_id": "cwe-285",
            "cluster_ids": [
                43,
                48
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 28,
            "name": "Improper Certificate Validation",
            "description": "The software does not validate, or incorrectly validates, a certificate.",
            "external_id": "cwe-295",
            "cluster_ids": [
                6,
                43,
                46,
                32,
                35,
                37
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 115,
            "name": "Improper Check or Handling of Exceptional Conditions",
            "description": "The software does not properly anticipate or handle exceptional conditions that rarely occur during normal operation of the software.",
            "external_id": "cwe-703",
            "cluster_ids": [],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 158,
            "name": "Improper Control of Interaction Frequency",
            "description": "The software does not properly limit the number or frequency of interactions that it has with an actor, such as the number of incoming requests.",
            "external_id": "cwe-799",
            "cluster_ids": [
                55
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 141,
            "name": "Improper Export of Android Application Components",
            "description": "The Android application exports a component for use by other applications, but does not properly restrict which applications can launch the component or access the data it contains.",
            "external_id": "cwe-926",
            "cluster_ids": [
                8
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 29,
            "name": "Improper Following of a Certificate's Chain of Trust",
            "description": "The software does not follow, or incorrectly follows, the chain of trust for a certificate back to a trusted root certificate, resulting in incorrect trust of any resource that is associated with that certificate.",
            "external_id": "cwe-296",
            "cluster_ids": [
                6,
                32,
                35,
                37
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 109,
            "name": "Improper Handling of Highly Compressed Data (Data Amplification)",
            "description": "The software does not handle or incorrectly handles a compressed input with a very high compression ratio that produces a large output.",
            "external_id": "cwe-409",
            "cluster_ids": [],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 135,
            "name": "Improper Handling of Insufficient Permissions or Privileges",
            "description": "The application does not handle or incorrectly handles when it has insufficient privileges to access resources or functionality as specified by their permissions. This may cause it to follow unexpected code paths that may leave the application in an invalid state.",
            "external_id": "cwe-280",
            "cluster_ids": [],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 121,
            "name": "Improper Handling of URL Encoding (Hex Encoding)",
            "description": "The software does not properly handle when all or part of an input has been URL encoded.",
            "external_id": "cwe-177",
            "cluster_ids": [],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 107,
            "name": "Improper Input Validation",
            "description": "The product does not validate or incorrectly validates input that can affect the control flow or data flow of a program.",
            "external_id": "cwe-20",
            "cluster_ids": [],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 131,
            "name": "Improper Neutralization of Escape, Meta, or Control Sequences",
            "description": "The software receives input from an upstream component, but it does not neutralize or incorrectly neutralizes special elements that could be interpreted as escape, meta, or control character sequences when they are sent to a downstream component.",
            "external_id": "cwe-150",
            "cluster_ids": [],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 93,
            "name": "Improper Neutralization of HTTP Headers for Scripting Syntax",
            "description": "The application does not neutralize or incorrectly neutralizes web scripting syntax in HTTP headers that can be used by web browser components that can process raw headers, such as Flash.",
            "external_id": "cwe-644",
            "cluster_ids": [
                9
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 112,
            "name": "Improper Neutralization of Script-Related HTML Tags in a Web Page (Basic XSS)",
            "description": "The software receives input from an upstream component, but it does not neutralize or incorrectly neutralizes special characters such as \"<\", \">\", and \"&\" that could be interpreted as web-scripting elements when they are sent to a downstream component that processes web pages.",
            "external_id": "cwe-80",
            "cluster_ids": [],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 160,
            "name": "Improper Neutralization of Special Elements",
            "description": "The software receives input from an upstream component, but it does not neutralize or incorrectly neutralizes special elements that could be interpreted as control elements or syntactic markers when they are sent to a downstream component.",
            "external_id": "cwe-138",
            "cluster_ids": [
                9
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 14,
            "name": "Improper None Termination",
            "description": "The software does not terminate or incorrectly terminates a string or array with a None character or equivalent terminator.",
            "external_id": "cwe-170",
            "cluster_ids": [
                7
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 122,
            "name": "Improper Privilege Management",
            "description": "The software does not properly assign, modify, track, or check privileges for an actor, creating an unintended sphere of control for that actor.",
            "external_id": "cwe-269",
            "cluster_ids": [],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 40,
            "name": "Inadequate Encryption Strength",
            "description": "The software stores or transmits sensitive data using an encryption scheme that is theoretically sound, but is not strong enough for the level of protection required.",
            "external_id": "cwe-326",
            "cluster_ids": [
                6,
                10,
                16,
                43,
                46,
                32,
                37
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 151,
            "name": "Inclusion of Functionality from Untrusted Control Sphere",
            "description": "The software imports, requires, or includes executable functionality (such as a library) from a source that is outside of the intended control sphere.",
            "external_id": "cwe-829",
            "cluster_ids": [
                55
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 129,
            "name": "Incomplete Blacklist",
            "description": "An application uses a \"blacklist\" of prohibited values, but the blacklist is incomplete.",
            "external_id": "cwe-184",
            "cluster_ids": [],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 128,
            "name": "Incorrect Authorization",
            "description": "The software performs an authorization check when an actor attempts to access a resource or perform an action, but it does not correctly perform the check. This allows attackers to bypass intended access restrictions.",
            "external_id": "cwe-863",
            "cluster_ids": [
                43,
                45
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 13,
            "name": "Incorrect Calculation of Buffer Size",
            "description": "The software does not correctly calculate the size to be used when allocating a buffer, which could lead to a buffer overflow.",
            "external_id": "cwe-131",
            "cluster_ids": [
                7
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 118,
            "name": "Incorrect Comparison",
            "description": "The software compares two entities in a security-relevant context, but the comparison is incorrect, which may lead to resultant weaknesses.",
            "external_id": "cwe-697",
            "cluster_ids": [],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 162,
            "name": "Incorrectly Specified Destination in a Communication Channel",
            "description": "The software creates a communication channel to initiate an outgoing request to an actor, but it does not correctly specify the intended destination for that actor.",
            "external_id": "cwe-941",
            "cluster_ids": [
                56
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 150,
            "name": "Incorrect Permission Assignment for Critical Resource",
            "description": "The software specifies permissions for a security-critical resource in a way that allows that resource to be read or modified by unintended actors.",
            "external_id": "cwe-732",
            "cluster_ids": [
                54
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 18,
            "name": "Information Disclosure",
            "description": "An information disclosure is the intentional or unintentional disclosure of information to an actor that is not explicitly authorized to have access to that information.",
            "external_id": "cwe-200",
            "cluster_ids": [
                5,
                32,
                36,
                38,
                8
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 82,
            "name": "Information Exposure Through an Error Message",
            "description": "The software generates an error message that includes sensitive information about its environment, users, or associated data.",
            "external_id": "cwe-209",
            "cluster_ids": [
                5,
                10,
                15,
                43,
                49,
                32,
                33,
                36,
                38,
                8
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 83,
            "name": "Information Exposure Through Debug Information",
            "description": "The application contains debugging code that can expose sensitive information to untrusted parties.",
            "external_id": "cwe-215",
            "cluster_ids": [
                5,
                10,
                15,
                32,
                33,
                36,
                38,
                8
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 89,
            "name": "Information Exposure Through Directory Listing",
            "description": "A directory listing is inappropriately exposed, yielding potentially sensitive information to attackers.",
            "external_id": "cwe-548",
            "cluster_ids": [
                5,
                10,
                15,
                43,
                49,
                32,
                33,
                36,
                38,
                8
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 139,
            "name": "Information Exposure Through Discrepancy",
            "description": "The product behaves differently or sends different responses in a way that exposes security-relevant information about the state of the product, such as whether a particular operation was successful or not.",
            "external_id": "cwe-203",
            "cluster_ids": [],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 113,
            "name": "Information Exposure Through Sent Data",
            "description": "The accidental exposure of sensitive information through sent data refers to the transmission of data which are either sensitive in and of itself or useful in the further exploitation of the system through standard data channels.",
            "external_id": "cwe-201",
            "cluster_ids": [],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 116,
            "name": "Information Exposure Through Timing Discrepancy",
            "description": "Two separate operations in a product require different amounts of time to complete, in a way that is observable to an actor and reveals security-relevant information about the state of the product, such as whether a particular operation was successful or not.",
            "external_id": "cwe-208",
            "cluster_ids": [],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 55,
            "name": "Insecure Direct Object Reference (IDOR)",
            "description": "The system's authorization functionality does not prevent one user from gaining access to another user's data or record by modifying the key value identifying the data.",
            "external_id": "cwe-639",
            "cluster_ids": [
                5,
                10,
                14,
                43,
                48,
                32,
                33,
                36,
                38,
                9
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 101,
            "name": "Insecure Storage of Sensitive Information",
            "description": "The software stores sensitive information without properly limiting read or write access by unauthorized actors.",
            "external_id": "cwe-922",
            "cluster_ids": [
                10,
                16,
                43,
                46,
                32,
                34,
                8
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 114,
            "name": "Insecure Temporary File",
            "description": "Creating and using insecure temporary files can leave application and system data vulnerable to attack.",
            "external_id": "cwe-377",
            "cluster_ids": [],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 87,
            "name": "Insufficiently Protected Credentials",
            "description": "This weakness occurs when the application transmits or stores authentication credentials and uses an insecure method that is susceptible to unauthorized interception and/or retrieval.",
            "external_id": "cwe-522",
            "cluster_ids": [
                10,
                12,
                43,
                45,
                32,
                33,
                8
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 90,
            "name": "Insufficient Session Expiration",
            "description": "According to WASC, \"Insufficient Session Expiration is when a web site permits an attacker to reuse old session credentials or session IDs for authorization.\"",
            "external_id": "cwe-613",
            "cluster_ids": [
                5,
                10,
                12,
                43,
                45,
                32,
                33,
                36,
                38,
                8
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 157,
            "name": "Insufficient Verification of Data Authenticity",
            "description": "The software does not sufficiently verify the origin or authenticity of data, in a way that causes it to accept invalid data.",
            "external_id": "cwe-345",
            "cluster_ids": [
                54
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 15,
            "name": "Integer Overflow",
            "description": "The software performs a calculation that can produce an integer overflow or wraparound, when the logic assumes that the resulting value will always be larger than the original value. This can introduce other weaknesses when the calculation is used for resource management or execution control.",
            "external_id": "cwe-190",
            "cluster_ids": [
                7,
                43,
                52
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 16,
            "name": "Integer Underflow",
            "description": "The product subtracts one value from another, such that the result is less than the minimum allowable integer value, which produces a value that is not equal to the correct result.",
            "external_id": "cwe-191",
            "cluster_ids": [
                7
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 36,
            "name": "Key Exchange without Entity Authentication",
            "description": "The software performs a key exchange with an actor without verifying the identity of that actor.",
            "external_id": "cwe-322",
            "cluster_ids": [
                5,
                6,
                32,
                36,
                37,
                38
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 99,
            "name": "LDAP Injection",
            "description": "The software constructs all or part of an LDAP query using externally-influenced input from an upstream component, but it does not neutralize or incorrectly neutralizes special elements that could modify the intended LDAP query when it is sent to a downstream component.",
            "external_id": "cwe-90",
            "cluster_ids": [
                10,
                11,
                43,
                44,
                32,
                33,
                9
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 103,
            "name": "Leftover Debug Code (Backdoor)",
            "description": "The application was deployed with active debugging code that can create unintended entry points.",
            "external_id": "cwe-489",
            "cluster_ids": [
                32,
                42
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 76,
            "name": "Malware",
            "description": "An adversary installs and executes malicious code on the target system in an effort to achieve a negative technical impact.",
            "external_id": "capec-549",
            "cluster_ids": [],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 30,
            "name": "Man-in-the-Middle",
            "description": "The product does not adequately verify the identity of actors at both ends of a communication channel, or does not adequately ensure the integrity of the channel, in a way that allows the channel to be accessed or influenced by an actor that is not an endpoint.",
            "external_id": "cwe-300",
            "cluster_ids": [
                32,
                35,
                8
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 2,
            "name": "Memory Corruption - Generic",
            "description": "The software performs operations on a memory buffer, but it can read from or write to a memory location that is outside of the intended boundary of the buffer.",
            "external_id": "cwe-119",
            "cluster_ids": [
                7
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 145,
            "name": "Misconfiguration",
            "description": "Weakness typically introduced during the configuration of the software.",
            "external_id": "cwe-16",
            "cluster_ids": [
                49
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 147,
            "name": "Missing Authentication for Critical Function",
            "description": "The software does not perform any authentication for functionality that requires a provable user identity or consumes a significant amount of resources.",
            "external_id": "cwe-306",
            "cluster_ids": [
                54
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 152,
            "name": "Missing Authorization",
            "description": "The software does not perform an authorization check when an actor attempts to access a resource or perform an action.",
            "external_id": "cwe-862",
            "cluster_ids": [
                54
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 159,
            "name": "Missing Critical Step in Authentication",
            "description": "The software implements an authentication technique, but it skips a step that weakens the technique.",
            "external_id": "cwe-304",
            "cluster_ids": [
                8
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 84,
            "name": "Missing Encryption of Sensitive Data",
            "description": "The software does not encrypt sensitive or critical information before storage or transmission.",
            "external_id": "cwe-311",
            "cluster_ids": [
                10,
                12,
                16,
                43,
                46,
                32,
                33,
                8
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 39,
            "name": "Missing Required Cryptographic Step",
            "description": "The software does not implement a required step in a cryptographic algorithm, resulting in weaker encryption than advertised by that algorithm.",
            "external_id": "cwe-325",
            "cluster_ids": [
                6,
                10,
                16,
                43,
                46,
                32,
                37
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 106,
            "name": "Modification of Assumed-Immutable Data (MAID)",
            "description": "The software does not properly protect an assumed-immutable element from being modified by an attacker.",
            "external_id": "cwe-471",
            "cluster_ids": [
                5,
                9
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 51,
            "name": "None Pointer Dereference",
            "description": "A None pointer dereference occurs when the application dereferences a pointer that it expects to be valid, but is None, typically causing a crash or exit.",
            "external_id": "cwe-476",
            "cluster_ids": [
                7
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 17,
            "name": "Off-by-one Error",
            "description": "A product calculates or uses an incorrect maximum or minimum value that is 1 more, or 1 less, than the correct value.",
            "external_id": "cwe-193",
            "cluster_ids": [
                7
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 53,
            "name": "Open Redirect",
            "description": "A web application accepts a user-controlled input that specifies a link to an external site, and uses that link in a Redirect. This simplifies phishing attacks.",
            "external_id": "cwe-601",
            "cluster_ids": [
                10,
                20,
                32,
                33,
                8
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 59,
            "name": "OS Command Injection",
            "description": "The software constructs all or part of an OS command using externally-influenced input from an upstream component, but it does not neutralize or incorrectly neutralizes special elements that could modify the intended OS command when it is sent to a downstream component.",
            "external_id": "cwe-78",
            "cluster_ids": [
                10,
                11,
                43,
                44,
                32,
                33,
                9
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 8,
            "name": "Out-of-bounds Read",
            "description": "The software reads data past the end, or before the beginning, of the intended buffer.",
            "external_id": "cwe-125",
            "cluster_ids": [
                7
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 24,
            "name": "Password in Configuration File",
            "description": "The software stores a password in a configuration file that might be accessible to actors who do not know the password.",
            "external_id": "cwe-260",
            "cluster_ids": [
                8
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 19,
            "name": "Path Traversal",
            "description": "The software uses external input to construct a pathname that is intended to identify a file or directory that is located underneath a restricted parent directory, but the software does not properly neutralize special elements within the pathname that can cause the pathname to resolve to a location that is outside of the restricted directory.",
            "external_id": "cwe-22",
            "cluster_ids": [
                5,
                10,
                14,
                43,
                48,
                32,
                33,
                36,
                38,
                9
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 119,
            "name": "Path Traversal: '.../...//'",
            "description": "The software uses external input to construct a pathname that should be within a restricted directory, but it does not properly neutralize '.../...//' (doubled triple dot slash) sequences that can resolve to a location that is outside of that directory.",
            "external_id": "cwe-35",
            "cluster_ids": [],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 73,
            "name": "Phishing",
            "description": "Phishing is a social engineering technique where an attacker masquerades as a legitimate entity with which the victim might do business in order to prompt the user to reveal some confidential information (very frequently authentication credentials) that can later be used by an attacker. Phishing is essentially a form of information gathering or \"fishing\" for information.",
            "external_id": "capec-98",
            "cluster_ids": [],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 21,
            "name": "Plaintext Storage of a Password",
            "description": "Storing a password in plaintext may result in a system compromise.",
            "external_id": "cwe-256",
            "cluster_ids": [
                10,
                12,
                43,
                45,
                32,
                33,
                8
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 46,
            "name": "Privacy Violation",
            "description": "The software does not properly prevent private data (such as credit card numbers) from being accessed by actors who either (1) are not explicitly authorized to access the data or (2) do not have the implicit consent of the people to which the data is related.",
            "external_id": "cwe-359",
            "cluster_ids": [
                5,
                43,
                46,
                32,
                36,
                38,
                8
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 75,
            "name": "Privilege Escalation",
            "description": "An adversary exploits a weakness enabling them to elevate their privilege and perform an action that they are not supposed to be authorized to perform.",
            "external_id": "capec-233",
            "cluster_ids": [
                5,
                43,
                48,
                32,
                36,
                38
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 125,
            "name": "Relative Path Traversal",
            "description": "The software uses external input to construct a pathname that should be within a restricted directory, but it does not properly neutralize sequences such as \"..\" that can resolve to a location that is outside of that directory.",
            "external_id": "cwe-23",
            "cluster_ids": [],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 97,
            "name": "Reliance on Cookies without Validation and Integrity Checking in a Security Decision",
            "description": "The application uses a protection mechanism that relies on the existence or values of a cookie, but it does not properly ensure that the cookie is valid for the associated user.",
            "external_id": "cwe-784",
            "cluster_ids": [
                8
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 130,
            "name": "Reliance on Reverse DNS Resolution for a Security-Critical Action",
            "description": "The software performs reverse DNS resolution on an IP address to obtain the hostname and make a security decision, but it does not properly ensure that the IP address is truly associated with the hostname.",
            "external_id": "cwe-350",
            "cluster_ids": [],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 133,
            "name": "Reliance on Untrusted Inputs in a Security Decision",
            "description": "The application uses a protection mechanism that relies on the existence or values of an input, but the input can be modified by an untrusted actor in a way that bypasses the protection mechanism.",
            "external_id": "cwe-807",
            "cluster_ids": [
                43,
                46
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 71,
            "name": "Remote File Inclusion",
            "description": "The PHP application receives input from an upstream component, but it does not restrict or incorrectly restricts the input before its usage in \"require,\" \"include,\" or similar functions.",
            "external_id": "cwe-98",
            "cluster_ids": [
                9
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 110,
            "name": "Replicating Malicious Code (Virus or Worm)",
            "description": "Replicating malicious code, including viruses and worms, will attempt to attack other systems once it has successfully compromised the target system or software.",
            "external_id": "cwe-509",
            "cluster_ids": [],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 72,
            "name": "Resource Injection",
            "description": "The software receives input from an upstream component, but it does not restrict or incorrectly restricts the input before it is used as an identifier for a resource that may be outside the intended sphere of control.",
            "external_id": "cwe-99",
            "cluster_ids": [
                10,
                14,
                32,
                33,
                9
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 37,
            "name": "Reusing a Nonce, Key Pair in Encryption",
            "description": "Nonces should be used for the present occasion and only once.",
            "external_id": "cwe-323",
            "cluster_ids": [
                6,
                32,
                37
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 42,
            "name": "Reversible One-Way Hash",
            "description": "The product uses a hashing algorithm that produces a hash value that can be used to determine the original input, or to find an input that can produce the same hash, more efficiently than brute force techniques.",
            "external_id": "cwe-328",
            "cluster_ids": [
                6,
                10,
                16,
                43,
                46,
                32,
                37
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 56,
            "name": "Security Through Obscurity",
            "description": "The software uses a protection mechanism whose strength depends heavily on its obscurity, such that knowledge of its algorithms or key data is sufficient to defeat the mechanism.",
            "external_id": "cwe-656",
            "cluster_ids": [
                32,
                41
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 68,
            "name": "Server-Side Request Forgery (SSRF)",
            "description": "The web server receives a URL or similar request from an upstream component and retrieves the contents of this URL, but it does not sufficiently ensure that the request is being sent to the expected destination.",
            "external_id": "cwe-918",
            "cluster_ids": [
                9
            ],
            "state": "enabled",
            "context_type": "SsrfContext"
        },
        {
            "id": 47,
            "name": "Session Fixation",
            "description": "Authenticating a user, or otherwise establishing a new user session, without invalidating any existing session identifier gives an attacker the opportunity to steal authenticated sessions.",
            "external_id": "cwe-384",
            "cluster_ids": [
                10,
                12,
                43,
                45,
                32,
                33
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 67,
            "name": "SQL Injection",
            "description": "The software constructs all or part of an SQL command using externally-influenced input from an upstream component, but it does not neutralize or incorrectly neutralizes special elements that could modify the intended SQL command when it is sent to a downstream component.",
            "external_id": "cwe-89",
            "cluster_ids": [
                10,
                11,
                43,
                44,
                32,
                33,
                9
            ],
            "state": "enabled",
            "context_type": "SqlInjectionContext"
        },
        {
            "id": 4,
            "name": "Stack Overflow",
            "description": "A stack-based buffer overflow condition is a condition where the buffer being overwritten is allocated on the stack (i.e., is a local variable or, rarely, a parameter to a function).",
            "external_id": "cwe-121",
            "cluster_ids": [
                7
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 22,
            "name": "Storing Passwords in a Recoverable Format",
            "description": "The storage of passwords in a recoverable format makes them subject to password reuse attacks by malicious users. In fact, it should be noted that recoverable encrypted passwords provide no significant benefit over plaintext passwords since they are subject not only to reuse by malicious attackers but also by malicious insiders. If a system administrator can recover a password directly, or use a brute force search on the available information, the administrator can use the password on other accounts.",
            "external_id": "cwe-257",
            "cluster_ids": [
                6,
                32,
                37,
                8
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 105,
            "name": "Time-of-check Time-of-use (TOCTOU) Race Condition",
            "description": "The software checks the state of a resource before using that resource, but the resource's state can change between the check and the use in a way that invalidates the results of the check. This can cause the software to perform invalid actions when the resource is in an unexpected state.",
            "external_id": "cwe-367",
            "cluster_ids": [
                8
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 127,
            "name": "Trust of System Event Data",
            "description": "Security based on event locations are insecure and can be spoofed.",
            "external_id": "cwe-360",
            "cluster_ids": [],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 66,
            "name": "Type Confusion",
            "description": "The program allocates or initializes a resource such as a pointer, object, or variable using one type, but it later accesses that resource using a type that is incompatible with the original type.",
            "external_id": "cwe-843",
            "cluster_ids": [
                7
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 74,
            "name": "UI Redressing (Clickjacking)",
            "description": "In a clickjacking attack the victim is tricked into unknowingly initiating some action in one system while interacting with the UI from seemingly completely different system.",
            "external_id": "capec-103",
            "cluster_ids": [
                8
            ],
            "state": "enabled",
            "context_type": "ClickJackingContext"
        },
        {
            "id": 117,
            "name": "Unchecked Error Condition",
            "description": "Ignoring exceptions and other error conditions may allow an attacker to induce unexpected behavior unnoticed.",
            "external_id": "cwe-391",
            "cluster_ids": [],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 134,
            "name": "Uncontrolled Recursion",
            "description": "The product does not properly control the amount of recursion that takes place, which consumes excessive resources, such as allocated memory or the program stack.",
            "external_id": "cwe-674",
            "cluster_ids": [],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 88,
            "name": "Unprotected Transport of Credentials",
            "description": "Login pages not using adequate measures to protect the user name and password while they are in transit from the client to the server.",
            "external_id": "cwe-523",
            "cluster_ids": [
                10,
                12,
                43,
                45,
                32,
                33,
                35,
                8
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 148,
            "name": "Unrestricted Upload of File with Dangerous Type",
            "description": "The software allows the attacker to upload or transfer files of dangerous types that can be automatically processed within the product's environment.",
            "external_id": "cwe-434",
            "cluster_ids": [
                56
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 144,
            "name": "Untrusted Search Path",
            "description": "The application searches for critical resources using an externally-supplied search path that can point to resources that are not under the application's direct control.",
            "external_id": "cwe-426",
            "cluster_ids": [],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 91,
            "name": "Unverified Password Change",
            "description": "When setting a new password for a user, the product does not require knowledge of the original password, or using another form of authentication.",
            "external_id": "cwe-620",
            "cluster_ids": [
                10,
                12,
                43,
                45,
                32,
                33,
                8
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 50,
            "name": "Use After Free",
            "description": "Referencing memory after it has been freed can cause a program to crash, use unexpected values, or execute code.",
            "external_id": "cwe-416",
            "cluster_ids": [
                7
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 41,
            "name": "Use of a Broken or Risky Cryptographic Algorithm",
            "description": "The use of a broken or risky cryptographic algorithm is an unnecessary risk that may result in the exposure of sensitive information.",
            "external_id": "cwe-327",
            "cluster_ids": [
                6,
                10,
                16,
                43,
                46,
                52,
                32,
                37
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 38,
            "name": "Use of a Key Past its Expiration Date",
            "description": "The product uses a cryptographic key or password past its expiration date, which diminishes its safety significantly by increasing the timing window for cracking attacks against that key.",
            "external_id": "cwe-324",
            "cluster_ids": [
                6,
                10,
                16,
                43,
                46,
                32,
                37
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 44,
            "name": "Use of Cryptographically Weak Pseudo-Random Number Generator (PRNG)",
            "description": "The product uses a Pseudo-Random Number Generator (PRNG) in a security context, but the PRNG is not cryptographically strong.",
            "external_id": "cwe-338",
            "cluster_ids": [
                6,
                32,
                37
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 81,
            "name": "Use of Externally-Controlled Format String",
            "description": "The software uses a function that accepts a format string as an argument, but the format string originates from an external source.",
            "external_id": "cwe-134",
            "cluster_ids": [
                7,
                43,
                51
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 64,
            "name": "Use of Hard-coded Credentials",
            "description": "The software contains hard-coded credentials, such as a password or cryptographic key, which it uses for its own inbound authentication, outbound communication to external components, or encryption of internal data.",
            "external_id": "cwe-798",
            "cluster_ids": [
                43,
                45,
                8
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 35,
            "name": "Use of Hard-coded Cryptographic Key",
            "description": "The use of a hard-coded cryptographic key significantly increases the possibility that encrypted data may be recovered.",
            "external_id": "cwe-321",
            "cluster_ids": [
                6,
                32,
                37
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 23,
            "name": "Use of Hard-coded Password",
            "description": "The software contains a hard-coded password, which it uses for its own inbound authentication or for outbound communication to external components.",
            "external_id": "cwe-259",
            "cluster_ids": [
                8
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 161,
            "name": "Use of Incorrectly-Resolved Name or Reference",
            "description": "The software uses a name or reference to access a resource, but the name/reference resolves to a resource that is outside of the intended control sphere.",
            "external_id": "cwe-706",
            "cluster_ids": [
                9
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 20,
            "name": "Use of Inherently Dangerous Function",
            "description": "The program calls a function that can never be guaranteed to work safely.",
            "external_id": "cwe-242",
            "cluster_ids": [
                32,
                39
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 43,
            "name": "Use of Insufficiently Random Values",
            "description": "The software may use insufficiently random numbers or values in a security context that depends on unpredictable numbers.",
            "external_id": "cwe-330",
            "cluster_ids": [
                6,
                32,
                37
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 132,
            "name": "User Interface (UI) Misrepresentation of Critical Information",
            "description": "The user interface (UI) does not properly represent critical information to the user, allowing the information - or its source - to be obscured or spoofed. This is often a component in phishing attacks.",
            "external_id": "cwe-451",
            "cluster_ids": [],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 156,
            "name": "Using Components with Known Vulnerabilities",
            "description": "Use of components with known vulnerabilities and lack of version upgrades or other mitigations in place. This is an unusual category. CWE does not cover the limitations of human processes and procedures that cannot be described in terms of a specific technical weakness as resident in the code, architecture, or configuration of the software. Since `known vulnerabilities` can arise from any kind of weakness, it is not possible to map this OWASP category to other CWE entries, since it would effectively require mapping this category to ALL weaknesses.",
            "external_id": "cwe-1035",
            "cluster_ids": [
                56
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 57,
            "name": "Violation of Secure Design Principles",
            "description": "The product violates well-established principles for secure design.",
            "external_id": "cwe-657",
            "cluster_ids": [
                10,
                19,
                43,
                52,
                32,
                39,
                8
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 25,
            "name": "Weak Cryptography for Passwords",
            "description": "Obscuring a password with a trivial encoding does not protect the password.",
            "external_id": "cwe-261",
            "cluster_ids": [
                6,
                32,
                37,
                8
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 92,
            "name": "Weak Password Recovery Mechanism for Forgotten Password",
            "description": "The software contains a mechanism for users to recover or change their passwords without knowing the original password, but the mechanism is weak.",
            "external_id": "cwe-640",
            "cluster_ids": [
                10,
                12,
                43,
                45,
                32,
                33,
                8
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 11,
            "name": "Wrap-around Error",
            "description": "Wrap around errors occur whenever a value is incremented past the maximum value for its type and therefore \"wraps around\" to a very small, negative, or undefined value.",
            "external_id": "cwe-128",
            "cluster_ids": [
                7
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 6,
            "name": "Write-what-where Condition",
            "description": "Any condition where the attacker has the ability to write an arbitrary value to an arbitrary location, often as the result of a buffer overflow.",
            "external_id": "cwe-123",
            "cluster_ids": [
                7
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 96,
            "name": "XML Entity Expansion",
            "description": "The software uses XML documents and allows their structure to be defined with a Document Type Definition (DTD), but it does not properly control the number of recursive definitions of entities.",
            "external_id": "cwe-776",
            "cluster_ids": [
                43,
                47,
                8,
                9
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 54,
            "name": "XML External Entities (XXE)",
            "description": "The software processes an XML document that can contain XML entities with URIs that resolve to documents outside of the intended sphere of control, causing the product to embed incorrect documents into its output.",
            "external_id": "cwe-611",
            "cluster_ids": [
                43,
                47,
                9
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 100,
            "name": "XML Injection",
            "description": "The software does not properly neutralize special elements that are used in XML, allowing attackers to modify the syntax, content, or commands of the XML before it is processed by an end system.",
            "external_id": "cwe-91",
            "cluster_ids": [
                10,
                11,
                43,
                44,
                32,
                33,
                9
            ],
            "state": "enabled",
            "context_type": None
        },
        {
            "id": 138,
            "name": "XSS Using MIME Type Mismatch",
            "description": "An adversary creates a file with scripting content but where the specified MIME type of the file is such that scripting is not expected. The adversary tricks the victim into accessing a URL that responds with the script file. Some browsers will detect that the specified MIME type of the file does not match the actual type of its content and will automatically switch to using an interpreter for the real content type. If the browser does not invoke script filters before doing this, the adversary's script may run on the target unsanitized, possibly revealing the victim's cookies or executing arbitrary script in their browser.",
            "external_id": "capec-209",
            "cluster_ids": [
                9
            ],
            "state": "enabled",
            "context_type": None
        }
    ]