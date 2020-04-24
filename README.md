# NVISNx – Backend Developer Test

## Setup the tech stack 
- [X] Python 3.6
- [X] Elasticsearch 6.0.0

## How to setup the application
1. Build the docker-compose
- Run `docker-compose build`

2. Run the application (ES, Kibana, Python)
- Run `docker-compose up`

## API Endpoints
- You can download the Postman [here](https://www.getpostman.com/collections/16aa23fc0e398c701d52)

## Guidelines
1. Create a single file housing a single class that contains all related work, and pick the proper REST method that you think should be used.

2. Each REST method should contain only one function call, which should be wrapped in a try/except statement.

3. For each function that you make, make an in-line comment explaining why it was necessary to make that function.

4. For each of the functions you create outside of the REST method, create unit tests to show that they work as expected.

## Questions
1. Using MongoDB, say we had a set of documents that contained “user_id”, “password”, and “display_name”. What query would you make if we wanted to collect all display names that start with the letter “a”? Make sure the password doesn’t show up in the results.
- **Answer**: `db.users.find( {display_name: /^a/}, { password: 0 } )`

2. Using Linux, what would the command or set of commands look like to connect to an NFS system?

3. Say we have 30GB worth of data we need to ingest. For either MongoDB or Elasticsearch, what would your strategy be to tackle the ingestion efficiently?
- **Answer**: `Logstash would be the best tool handle such huge amount of data for ingesting to multiple destinations either MongoDB/ES`