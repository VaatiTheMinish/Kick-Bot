# How to setup and connect to the database

## Step 1: Sign Up for MongoDB Atlas

1. Go to the [MongoDB Atlas website](https://www.mongodb.com/cloud/atlas).

2. Click the "Get started free" button or "Try Free" to begin the sign-up process.

3. Log in or create a MongoDB account if you don't have one.

## Step 2: Choose a Cluster Configuration

1. After logging in, click the "Build a New Cluster" button.

2. Select a cloud provider (e.g., AWS, Azure, or Google Cloud) for your cluster. Choose "Shared" for a free option.

3. Choose a region for the cluster based on your target audience or location.

4. Configure cluster settings (use default settings for now).

5. Click the "Create Cluster" button to provision your cluster.

## Step 3: Whitelist IP Addresses

1. In the Atlas dashboard, click on "Security" in the left sidebar.

2. Under the "IP Whitelist" tab, click "Add IP Address" to specify allowed IP addresses.

3. Add your current IP address for development or use `0.0.0.0/0` to allow access from any IP address (not recommended for production).

## Step 4: Create a Database User

1. In the "Security" section, click on "Database Access."

2. Click "Add New Database User."

3. Enter a username and a strong password.

4. Assign appropriate database privileges, such as "Atlas Admin" or "Read and Write to Any Database."

5. Click "Add User" to create the database user.

## Step 5: Connect to Your Cluster

1. In the Atlas dashboard, click on "Clusters" in the left sidebar.

2. Find your cluster and click "Connect."

3. Choose "Connect Your Application."

4. Copy the connection string provided, replacing `<username>`, `<password>`, `<clustername>`, and `<database>` with your actual credentials and details:
