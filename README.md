# Search Past UBC Courses by Professor

### Description
Search UBC profs by name, and find out what previous courses
they have taught. Provides average, and UBCGrades link.


### Technical Details

Uses Bootstrap framework for styling, jQuery to allow for search, and
Flask as server to handle requests. Didn't really want to use a database
engine for this, so pandas and some CSV handles the query.


### Deployment

Install Docker, and Docker Compose v2.

Create a new `.env` file with the line `CLOUDFLARED_TUNNEL_TOKEN=<token>`.
For example, if your token is `abcd`, the file
should be:

```
CLOUDFLARED_TUNNEL_TOKEN=abcd
```

Then run `docker compose up` to bring up the services. `docker compose up -d`
run the services in detached mode.