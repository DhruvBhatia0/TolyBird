list of things to do to set this up:

## X account:

you're gonna want a developer account https://developer.x.com/en, specifically, a paid dev account (Free -> Basic). Free teir has a pretty limited amount of tweet reads and writes. 

-> https://developer.x.com/en/portal/dashboard

-> Go to project apps, make a project, under that make an app. each app has it's own key/access token. The recommended way to format this is, project is the org, app is the specific application (twitter account)

-> Under tokens, you should see a keys and tokesn section. Make a bearer token, api key + secret, access token + secret, client id + secret. All of these are needed to fully operate an X account from code.

-> You Access token MUST be created with READ AND WRITE permissions (or higher). It defaults to just read. Fix this by clicking on the gear icon on the app in the projects and apps section, go into "User authentication settings", and set the access level. 


## how to host:

## How to Host on AWS EC2

Hosting your application on AWS EC2 can be straightforward if you follow these specific steps. Below are detailed instructions to get your application up and running.

### Recommended Instance Type:
- **Instance Type**: `t2.micro` (eligible for the AWS Free Tier)
- **Operating System**: **Ubuntu Server 20.04 LTS** (recommended for ease of use and community support)

### Steps to Host:

1. **Launch an EC2 Instance**:

2. **Choose an Amazon Machine Image (AMI)**:
   - Select **Ubuntu Server 20.04 LTS** from the list of available AMIs.

3. **Select Instance Type**:
   - Choose **t2.micro** and click **Next: Configure Instance Details**.

4. **Configure Instance Details**:
   - Leave the default settings for the number of instances and network.
   - Ensure **Auto-assign Public IP** is set to **Enable**.

5. **Add Storage**:
   - Use the default storage settings (8 GB General Purpose SSD) 

6. **Configure Security Group**:
   - Create a new security group with the following rules:
     - **Type**: SSH | **Protocol**: TCP | **Port Range**: 22 | **Source**: My IP (to allow SSH access)
     - **Type**: HTTP | **Protocol**: TCP | **Port Range**: 80 | **Source**: Anywhere (0.0.0.0/0)
     - **Type**: HTTPS | **Protocol**: TCP | **Port Range**: 443 | **Source**: Anywhere (0.0.0.0/0)
     - **Type**: Custom TCP | **Protocol**: TCP | **Port Range**: 6000 | **Source**: Anywhere (0.0.0.0/0) (for your application)

7. **Connect to Your Instance**:
    - Open a terminal (or use PuTTY on Windows).
    - Navigate to the directory where your key pair is stored.
    - Run the following command to connect (replace `your-public-ip` with the public IP of your instance):
      ```bash
      chmod 400 my-key-pair.pem
      ssh -i "my-key-pair.pem" ubuntu@your-public-ip
      ```

8. **Install basic software**:
    - Once connected, run the following commands to update the package manager and install necessary software:
      ```bash
      sudo apt update && sudo apt upgrade -y
      sudo apt install -y nodejs npm
      sudo apt install -y python3 python3-pip
      ```

9. **Clone Your Application Repository**:
    - Install Git if not already installed:
      ```bash
      sudo apt install -y git
      ```
    - Clone your application repository:
      ```bash
      git clone {}
      cd your-repo
      ```

10. **Install Application Dependencies**:
    - For a Node.js application, run:
      ```bash
      npm install
      ```
    - For a Python application, run:
      ```bash
      pip3 install -r requirements.txt
      ```

11. **Start Your Application**:
    - For a Node.js application, run:
      ```bash
      npm run dev
      ```
    - For a Python application, run:
      ```bash
      python3 app.py
      ```

12. **Access Your Application**:
    - Open a web browser and navigate to `http://your-public-ip` to see your application running.


