# Hetzner-Pulumi-Template

The project aimed to train machine learning models for the medbot application. Due to the insufficient compute power of my local laptop, I designed a solution leveraging cloud infrastructure.
Therefore, a Hetzner Cloud server was set up using an Infrastructure as Code (IaC) script in Pulumi (Python). The server is designed to be spun up only when needed. This way costs can be minimized.  

Infrastructure as Code (IaC) is a practice where you define and manage your IT infrastructure (e.g., servers, networks, databases) using code instead of manual processes. With IaC, infrastructure configurations are written in code files and can be versioned, automated, and reused, just like software code.

Pulumi is an open-source Infrastructure as Code tool that allows you to define, deploy, and manage cloud infrastructure using general-purpose programming languages like Python, JavaScript, TypeScript, Go, or C# (<https://www.pulumi.com/>).

In the script the deployment process is automated. The following steps are executed:

- The SSH key is uploaded to the Hetzner Cloud to ensure secure access
- A Hetzner Cloud server is provisioned with specific configurations
- The server is configured:
  - the private SSH key is uploaded
  - initialization scripts are run to update the system
  - Git is configured
  - medbot repository is cloned
  - dependencies are installed
- The server is added to the local SSH configuration file
- If the server gets destroyed again, the server will be removed from the local SSH configuration file
