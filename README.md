# SSL Swap via Rogue Access Point Attack

**Research Question (RQ):**  
*Are FIDO2 MFA mechanisms vulnerable to phishing and adversary-in-the-middle (AITM) attacks when rogue Wi-Fi access points and malicious Certificate Authorities are used?*

---

<br>

### **Overview**  

The *SSL Swap via Rogue Access Point Attack* exposes vulnerabilities in all forms of multi-factor authentication (MFA), including hardware-based mechanisms like FIDO2. Despite FIDO2’s reputation for phishing resistance, this attack demonstrates that its reliance on environmental components—such as the browser, root Certificate Authorities (CAs), and the operating system—can be exploited to compromise security.

<br>

## Deliverable:

![image](https://github.com/user-attachments/assets/d9f62d10-9de4-4fd6-9bec-e514407bb620)

<br>

#### **Lab Proof-of-Concept (L-PoC) Setup**

To validate the attack, we created a controlled Lab Proof-of-Concept (L-PoC) environment with four interconnected processes communicating over TCP. The attack progresses as follows:

1. **Initial Connection Attempt:**  
   - The victim process attempts to connect to the rogue network but lacks the malicious CA required to establish trust.

2. **Malicious CA Installation:**  
   - The rogue network prompts the victim to download and install the malicious CA. Once installed, the victim retries the connection.

3. **DNS Resolution Manipulation:**  
   - The victim process requests DNS resolution for a target URL through the rogue network.  
   - The rogue network forwards this request to a DNS process and intercepts the response.  
   - The DNS response is edited to redirect the victim to a rogue IP controlled by the attacker.

4. **HTTPS Session Hijacking:**  
   - The victim attempts to establish an HTTPS session with the malicious IP.  
   - The rogue server presents a fake SSL certificate signed by the malicious CA.  
   - The victim's system accepts the certificate as authentic due to the previously installed malicious CA.

At this point, the victim is securely connected to the rogue server, which is impersonating the legitimate URL. The victim is unable to distinguish the rogue server from the genuine service, enabling the attacker to intercept sensitive data or hijack authentication mechanisms.

---

<br>

#### **Internet-Scale Demonstration**

After confirming the success of the L-PoC, we extended the attack to a real-world internet environment:

1. **Website Setup:**  
   - We registered the domain `http://donotconnect.org` and hosted it on a free Amazon EC2 instance running Apache2.  
   - The server was configured to present two distinct SSL certificates:
     - One for `https://donotconnect.org`, claiming to be `donotconnect.org`.
     - One for `https://demo.donotconnect.org`, falsely claiming to be `login.microsoft.com`.

2. **Rogue Wi-Fi Network:**  
   - A rogue wireless access point was configured to intercept DNS requests for `login.microsoft.com` and redirect them to the IP of `demo.donotconnect.org`.

3. **Attack Execution:**  
   - A victim device connected to the rogue network and downloaded the malicious CA.  
   - When the victim navigated to `login.microsoft.com`, DNS spoofing redirected the connection to `demo.donotconnect.org`.  
   - The rogue server presented a fake certificate for `login.microsoft.com`, validated using the malicious CA.  
   - The victim’s browser and dependent processes accepted the fake certificate, completing the attack.

---

<br>

#### **Impact Analysis**

The attack highlights significant vulnerabilities in the MFA ecosystem, especially where external dependencies like root CAs are involved. Even hardware MFA solutions like FIDO2, which are designed to resist phishing, can be undermined when their trust model is compromised.

We conducted a detailed analysis to estimate the potential impact of this vulnerability, focusing on:

1. **Remediation Costs:**  
   - The financial, resource, and time investments required for recovery after such an attack.  
   - The possible reputational damage to organizations whose systems are compromised.

2. **Proposed Security Enhancements:**  
   - Strengthening browser and operating system protections against rogue CAs.  
   - Enhancing DNS security with mechanisms like DNSSEC to prevent spoofing.  
   - Incorporating additional environmental checks in MFA protocols to validate authenticity.

---

<br>

The *SSL Swap via Rogue Access Point Attack* serves as a proof-of-concept demonstrating the potential exploitation of dependencies in MFA mechanisms. By identifying and addressing these vulnerabilities, organizations can improve the resilience of their systems against sophisticated phishing and AITM attacks.
